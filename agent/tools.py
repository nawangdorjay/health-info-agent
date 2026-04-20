"""
Remote Area Health Info Agent — Tool Functions
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def _load_json(filename: str) -> dict:
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_health_guidance(condition: str) -> dict:
    """Get health guidance for a condition."""
    conditions = _load_json("conditions.json")
    key = condition.lower().strip()

    if key in conditions:
        return {"found": True, "condition": key, **conditions[key]}

    # Fuzzy match
    for k in conditions:
        if key in k or k in key:
            return {"found": True, "condition": k, **conditions[k]}

    return {
        "found": False,
        "message": f"I don't have specific guidance for '{condition}'. For any health concern, please visit your nearest PHC or call 108 for emergency.",
        "general_advice": [
            "Visit the nearest Primary Health Centre (PHC)",
            "Call 108 for ambulance if emergency",
            "Call 102 for health helpline",
            "Keep patient comfortable and hydrated",
        ],
    }


def find_nearest_hospitals(location: str, facility_type: str = "all") -> dict:
    """Find hospitals and health centres near a location."""
    hospitals = _load_json("hospitals.json")
    location_lower = location.lower().strip()

    matched = []
    for region, facilities in hospitals.items():
        if location_lower in region or region in location_lower:
            for f in facilities:
                if facility_type == "all" or f.get("type") == facility_type:
                    matched.append(f)

    if not matched:
        # Try partial matching
        for region, facilities in hospitals.items():
            if any(loc_word in region for loc_word in location_lower.split()):
                for f in facilities:
                    if facility_type == "all" or f.get("type") == facility_type:
                        matched.append(f)

    if matched:
        return {"location": location, "facilities": matched[:8]}

    return {
        "location": location,
        "facilities": [],
        "general_advice": [
            "Call 108 — ambulance will take you to nearest hospital",
            "Ask local panchayat/government office for PHC location",
            "Use Google Maps to search 'hospital near me'",
            "Call 104 (health helpline) for guidance",
        ],
    }


def get_emergency_contacts(state: str) -> dict:
    """Get emergency contacts for a state."""
    contacts = _load_json("emergency_contacts.json")
    state_lower = state.lower().strip()

    if state_lower in contacts:
        return {"state": state, "contacts": contacts[state_lower]}

    # Fuzzy
    for k in contacts:
        if state_lower in k or k in state_lower:
            return {"state": k, "contacts": contacts[k]}

    # National emergency contacts
    return {
        "state": "National (default)",
        "contacts": contacts.get("national", {}),
        "note": f"No specific data for '{state}'. Showing national numbers.",
    }


def get_disease_info(disease: str) -> dict:
    """Get disease information."""
    diseases = _load_json("diseases.json")
    key = disease.lower().strip()

    if key in diseases:
        return {"found": True, "disease": key, **diseases[key]}

    for k in diseases:
        if key in k or k in key:
            return {"found": True, "disease": k, **diseases[k]}

    return {
        "found": False,
        "message": f"I don't have specific information about '{disease}'. Please consult a doctor at your nearest health centre.",
    }


def get_altitude_health_tips(region: str) -> dict:
    """Get altitude sickness and mountain health advice."""
    tips = _load_json("altitude_tips.json")
    key = region.lower().strip()

    if key in tips:
        return {"region": region, **tips[key]}

    # Default altitude advice
    return {
        "region": region,
        "altitude_sickness": {
            "symptoms": ["Headache", "Nausea", "Dizziness", "Fatigue", "Loss of appetite", "Difficulty sleeping"],
            "prevention": [
                "Acclimatize for 1-2 days after arriving at high altitude",
                "Drink plenty of water (3-4 litres/day)",
                "Avoid alcohol and smoking",
                "Ascend gradually — don't gain more than 500m altitude per day",
                "Eat light, high-carb meals",
            ],
            "when_to_seek_help": [
                "Severe headache not relieved by paracetamol",
                "Persistent vomiting",
                "Confusion or difficulty walking",
                "Breathing difficulty at rest",
                "Blue lips or fingernails",
            ],
            "emergency_action": "Descend immediately if severe symptoms. Call 108 for evacuation.",
        },
    }


def get_health_schemes(query: str) -> dict:
    """Get government health scheme information."""
    schemes = _load_json("health_schemes.json")
    query_lower = query.lower()

    matched = []
    for scheme in schemes:
        name_lower = scheme.get("name", "").lower()
        desc_lower = scheme.get("description", "").lower()
        keywords = scheme.get("keywords", [])

        if (query_lower in name_lower or
            query_lower in desc_lower or
            any(query_lower in kw for kw in keywords)):
            matched.append(scheme)

    if not matched:
        matched = schemes  # Return all

    return {"query": query, "schemes": matched[:5]}
