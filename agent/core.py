"""
Remote Area Health Info Agent — Core Logic
Provides health guidance, hospital info, and emergency contacts for remote/hilly regions.
"""
import os
import json
from typing import Optional
from agent.tools import (
    get_health_guidance,
    find_nearest_hospitals,
    get_emergency_contacts,
    get_disease_info,
    get_ambulance_info,
    get_pharmacy_info,
    get_health_schemes,
    get_altitude_health_tips,
)

SYSTEM_PROMPT = """You are Seva Doctor (सेवा डॉक्टर), a compassionate and knowledgeable health information agent for people in remote and hilly regions of India.

Your capabilities:
- Provide basic health guidance for common ailments
- Help find nearest hospitals, PHCs, and health centres
- Share emergency contact numbers
- Explain common diseases and symptoms
- Provide first-aid guidance
- Share information about government health schemes
- Give altitude sickness and mountain health advice (especially relevant for Ladakh, Northeast, Uttarakhand)

IMPORTANT RULES:
1. ALWAYS respond in the same language the user writes in. Support Hindi, English, and regional languages.
2. For EMERGENCY situations, ALWAYS first provide emergency numbers (108, 102) before any other advice.
3. Never diagnose or prescribe medicine. You are an information agent, not a doctor.
4. Always recommend visiting a qualified doctor for serious symptoms.
5. Be empathetic and reassuring. Many users in remote areas have limited access to healthcare.
6. Provide practical, actionable steps — what to do RIGHT NOW and where to go.
7. Include specific hospital names, distances, and phone numbers when available.
8. For altitude-related issues (Ladakh, Spiti, etc.), provide region-specific advice.

You have access to tools that provide:
- Health guidance for common conditions
- Hospital/PHC databases with locations and contacts
- Emergency numbers by state
- Disease information
- Ambulance services
- Pharmacy locations
- Government health schemes

Use these tools to give accurate, data-backed answers. Always prioritize safety."""


class HealthAgent:
    """Main agent for health information queries."""

    def __init__(self, api_key: Optional[str] = None, provider: str = "openai"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
        self.provider = provider
        self.conversation_history = []

    def _get_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_health_guidance",
                    "description": "Get health guidance for a common condition or symptom.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "condition": {
                                "type": "string",
                                "description": "Health condition or symptom (e.g., fever, diarrhea, headache, chest pain)"
                            }
                        },
                        "required": ["condition"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "find_nearest_hospitals",
                    "description": "Find hospitals and health centres near a location.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City, district, or area name"
                            },
                            "facility_type": {
                                "type": "string",
                                "description": "Type: hospital, phc, chc, or all"
                            }
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_emergency_contacts",
                    "description": "Get emergency contact numbers for a state or region.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "state": {
                                "type": "string",
                                "description": "Indian state name"
                            }
                        },
                        "required": ["state"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_disease_info",
                    "description": "Get information about a disease — symptoms, prevention, when to see a doctor.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "disease": {
                                "type": "string",
                                "description": "Disease name (e.g., dengue, malaria, tuberculosis, diabetes)"
                            }
                        },
                        "required": ["disease"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_altitude_health_tips",
                    "description": "Get altitude sickness and high-altitude health advice for mountain regions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "region": {
                                "type": "string",
                                "description": "High-altitude region (e.g., Ladakh, Spiti, Sikkim)"
                            }
                        },
                        "required": ["region"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_health_schemes",
                    "description": "Get government health scheme information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "What the person is looking for (e.g., free treatment, insurance, hospital card)"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
        ]

    def _execute_tool(self, tool_name: str, arguments: dict) -> str:
        tools_map = {
            "get_health_guidance": get_health_guidance,
            "find_nearest_hospitals": find_nearest_hospitals,
            "get_emergency_contacts": get_emergency_contacts,
            "get_disease_info": get_disease_info,
            "get_altitude_health_tips": get_altitude_health_tips,
            "get_health_schemes": get_health_schemes,
        }
        if tool_name in tools_map:
            result = tools_map[tool_name](**arguments)
            return json.dumps(result, ensure_ascii=False)
        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    def process_query(self, user_message: str) -> str:
        try:
            import openai
        except ImportError:
            return "Error: Please install openai package: pip install openai"

        client = openai.OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1" if self.provider == "groq" else None,
        )

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(self.conversation_history[-10:])
        messages.append({"role": "user", "content": user_message})

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile" if self.provider == "groq" else "gpt-4o-mini",
                messages=messages,
                tools=self._get_tools(),
                tool_choice="auto",
                temperature=0.5,
                max_tokens=1024,
            )

            assistant_message = response.choices[0].message

            if assistant_message.tool_calls:
                messages.append(assistant_message)
                for tool_call in assistant_message.tool_calls:
                    arguments = json.loads(tool_call.function.arguments)
                    result = self._execute_tool(tool_call.function.name, arguments)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })

                final_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile" if self.provider == "groq" else "gpt-4o-mini",
                    messages=messages,
                    temperature=0.5,
                    max_tokens=1024,
                )
                answer = final_response.choices[0].message.content
            else:
                answer = assistant_message.content

            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": answer})
            return answer

        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}. If this is an emergency, call 108 (ambulance) or 102 (health helpline) immediately."
