# 🏥 Seva Doctor — Remote Area Health Info Agent

An AI-powered health information agent providing guidance, hospital locations, emergency contacts, and altitude health advice for remote and hilly regions of India.

Built by [Nawang Dorjay](https://github.com/nawangdorjay) — from Ladakh, for **GSSoC 2026** (Agents for India Track).

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 💊 **Health Guidance** | First-aid advice for common conditions — fever, diarrhea, burns, injuries |
| 🏥 **Hospital Finder** | Nearest hospitals, PHCs, CHCs with phone numbers and services |
| 🚨 **Emergency Contacts** | State-wise emergency numbers — 108, 102, 112, helplines |
| 🏔️ **Altitude Health** | AMS prevention & treatment for Ladakh, Spiti, Sikkim, Uttarakhand |
| 🏛️ **Health Schemes** | Ayushman Bharat, Jan Aushadhi, JSY — free treatment & cheap medicines |
| 🦠 **Disease Info** | Dengue, malaria, TB, typhoid — symptoms, prevention, when to get help |
| 🌐 **Multilingual** | Responds in Hindi, English, and regional languages |

---

## 🎯 Why This Matters

> In remote and hilly regions of India — Ladakh, Northeast, Uttarakhand, Himachal — the nearest hospital can be 5-10 hours away by road. People need reliable health information *right now*, not after a long journey.

**Real scenarios this agent helps with:**
- Tourist in Leh with altitude sickness on Day 1 → what to do NOW
- Farmer in Nubra Valley with child's fever → where is the nearest PHC?
- Villager in Spiti with chest pain → is this an emergency? Call 108
- Pregnant woman in remote Sikkim → government scheme for free delivery
- Someone in Northeast with dengue symptoms → home care vs hospital

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **OpenAI / Groq API** — LLM backbone
- **Streamlit** — Interactive chat UI
- **JSON** — Structured health data (hospitals, diseases, contacts, schemes)

---

## 📦 Installation

```bash
# Clone
git clone https://github.com/nawangdorjay/health-info-agent.git
cd health-info-agent

# Install
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your API key:
# GROQ_API_KEY=gsk_xxxxx  (free at console.groq.com)

# Run
streamlit run app.py
```

---

## 📁 Project Structure

```
health-info-agent/
├── app.py                    # Streamlit chat UI
├── agent/
│   ├── __init__.py
│   ├── core.py               # Agent logic + tool orchestration
│   └── tools.py              # Tool functions
├── data/
│   ├── conditions.json       # Health guidance (fever, diarrhea, burns, etc.)
│   ├── diseases.json         # Disease info (dengue, malaria, TB, typhoid, etc.)
│   ├── emergency_contacts.json # State-wise emergency numbers
│   ├── hospitals.json        # Hospital/PHC database with phone numbers
│   ├── altitude_tips.json    # Altitude sickness advice (Ladakh, Spiti, Sikkim)
│   └── health_schemes.json   # Government health schemes
├── tests/
│   └── test_tools.py         # 15 tool validation tests
├── .github/workflows/
│   └── ci.yml                # GitHub Actions CI
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🧪 Testing

```bash
python tests/test_tools.py
```

15 tests covering: health guidance, hospital lookup, emergency contacts, disease info, altitude tips, and health schemes.

---

## 🏔️ Regions Covered

| Region | Hospitals | Altitude Advice | Emergency Contacts |
|--------|-----------|-----------------|-------------------|
| **Ladakh** | SNM Hospital Leh, PHC Diskit (Nubra), PHC Tangtse (Pangong), Kargil | ✅ AMS, HAPE, HACE | ✅ State-specific |
| **Spiti Valley** | CHC Kaza, PHC Tabo | ✅ Remote advice | ✅ |
| **Sikkim** | STNM Gangtok, North Sikkim facilities | ✅ Gurudongmar Lake | ✅ |
| **Northeast** | GMCH Guwahati, JNIMS Imphal, etc. | — | ✅ All 7 states |
| **Uttarakhand** | AIIMS Rishikesh | ✅ Char Dham | ✅ |
| **J&K** | SMHS Srinagar, GMC Jammu | ✅ | ✅ |

---

## 📋 Health Conditions Covered

| Condition | Guidance | When to See Doctor | Warning Signs |
|-----------|----------|-------------------|---------------|
| Fever | ✅ | ✅ | ✅ |
| Diarrhea | ✅ + ORS recipe | ✅ | ✅ |
| Cough & Cold | ✅ | ✅ | — |
| Headache | ✅ | ✅ | ✅ |
| Stomach Pain | ✅ | ✅ | — |
| Chest Pain | ✅ | ✅ | 🚨 Emergency |
| Skin Rash | ✅ | ✅ | — |
| Burns | ✅ | ✅ | — |
| Breathing Difficulty | ✅ | ✅ | 🚨 Emergency |
| Malaria Symptoms | ✅ | ✅ | ✅ |
| Dengue Symptoms | ✅ | ✅ | ✅ |
| Typhoid | ✅ | ✅ | ✅ |
| Chickenpox | ✅ | ✅ | — |
| Diabetes | ✅ Management | ✅ | ✅ |
| Hypertension | ✅ Management | ✅ | ✅ |
| TB | ✅ | ✅ | ✅ + Govt program |

---

## 🏛️ Government Health Schemes

- **Ayushman Bharat (PM-JAY)** — Free ₹5L insurance, 1900+ procedures
- **Janani Suraksha Yojana** — Cash assistance for institutional delivery
- **Jan Aushadhi** — Generic medicines at 50-90% cheaper
- **NTEP (TB)** — Free testing, treatment, ₹500/month nutrition support
- **NACP (HIV)** — Free testing and ART
- **Immunization Programme** — Free vaccines for children and pregnant women

---

## ⚠️ Disclaimer

This is an **information agent**, not a medical professional. It provides general health guidance based on structured data. For any serious health concern:

1. **Call 108** for ambulance in emergencies
2. **Call 102** for health helpline
3. **Visit your nearest PHC or hospital**

Always consult a qualified doctor for diagnosis and treatment.

---

## 🔮 Future Improvements

- [ ] Integration with eSanjeevani (telemedicine) for remote consultations
- [ ] Voice-based interface for low-literacy users
- [ ] Offline mode with local LLM for areas without internet
- [ ] Integration with Bhashini for better multilingual support
- [ ] Expand hospital database to all districts
- [ ] Add mental health helpline resources
- [ ] WhatsApp bot integration

---

## 📄 License

MIT

---

## 👨‍💻 Author

**Nawang Dorjay** — B.Tech CSE (Data Science), MAIT Delhi
From Nubra Valley, Leh, Ladakh 🏔️

- [GitHub](https://github.com/nawangdorjay)
- [Email](mailto:nawangdorjay09@gmail.com)

Built for **GSSoC 2026** — Agents for India Track.

---

## 🤖 AI-Assisted Development

This project was built with AI assistance as part of a transparent human-AI collaboration workflow. AI helped with code generation, structure, and documentation — while domain expertise, data accuracy, and architectural decisions were human-driven.

> **See [BUILDING.md](BUILDING.md) for full transparency on AI usage, roles, and workflow.**

