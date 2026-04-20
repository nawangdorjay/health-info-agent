"""Tests for Health Info Agent tools."""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent.tools import (
    get_health_guidance,
    find_nearest_hospitals,
    get_emergency_contacts,
    get_disease_info,
    get_altitude_health_tips,
    get_health_schemes,
)


def test_health_guidance():
    result = get_health_guidance("fever")
    assert result["found"] is True
    assert result["condition"] == "fever"
    assert "what_to_do" in result
    assert len(result["what_to_do"]) > 0
    print("✅ test_health_guidance passed")


def test_health_guidance_fuzzy():
    result = get_health_guidance("cough")
    assert result["found"] is True
    print("✅ test_health_guidance_fuzzy passed")


def test_health_guidance_unknown():
    result = get_health_guidance("unknownconditionxyz")
    assert result["found"] is False
    assert "general_advice" in result
    print("✅ test_health_guidance_unknown passed")


def test_hospitals_leh():
    result = find_nearest_hospitals("leh ladakh")
    assert len(result["facilities"]) > 0
    names = [f["name"] for f in result["facilities"]]
    assert any("SNM" in n for n in names)
    print("✅ test_hospitals_leh passed")


def test_hospitals_nubra():
    result = find_nearest_hospitals("nubra")
    assert len(result["facilities"]) > 0
    print("✅ test_hospitals_nubra passed")


def test_hospitals_type():
    result = find_nearest_hospitals("leh", facility_type="phc")
    for f in result["facilities"]:
        assert f["type"] == "phc"
    print("✅ test_hospitals_type passed")


def test_emergency_ladakh():
    result = get_emergency_contacts("ladakh")
    assert "contacts" in result
    assert "ambulance" in result["contacts"]
    assert result["contacts"]["ambulance"] == "108"
    print("✅ test_emergency_ladakh passed")


def test_emergency_national():
    result = get_emergency_contacts("national")
    assert result["contacts"]["ambulance"] == "108"
    assert result["contacts"]["emergency"] == "112"
    print("✅ test_emergency_national passed")


def test_disease_dengue():
    result = get_disease_info("dengue")
    assert result["found"] is True
    assert "symptoms" in result
    assert "prevention" in result
    print("✅ test_disease_dengue passed")


def test_disease_malaria():
    result = get_disease_info("malaria")
    assert result["found"] is True
    print("✅ test_disease_malaria passed")


def test_disease_tb():
    result = get_disease_info("tuberculosis")
    assert result["found"] is True
    assert "govt_program" in result
    print("✅ test_disease_tb passed")


def test_altitude_ladakh():
    result = get_altitude_health_tips("ladakh")
    assert result["region"] == "Ladakh"
    assert "altitude_sickness" in result
    assert "what_to_carry" in result
    assert len(result["altitude_sickness"]["prevention"]) > 0
    print("✅ test_altitude_ladakh passed")


def test_altitude_spiti():
    result = get_altitude_health_tips("spiti valley")
    assert "key_advice" in result
    print("✅ test_altitude_spiti passed")


def test_health_schemes():
    result = get_health_schemes("insurance")
    assert len(result["schemes"]) > 0
    names = [s["name"] for s in result["schemes"]]
    assert any("Ayushman" in n for n in names)
    print("✅ test_health_schemes passed")


def test_health_schemes_medicine():
    result = get_health_schemes("medicine")
    assert len(result["schemes"]) > 0
    print("✅ test_health_schemes_medicine passed")


if __name__ == "__main__":
    tests = [
        test_health_guidance,
        test_health_guidance_fuzzy,
        test_health_guidance_unknown,
        test_hospitals_leh,
        test_hospitals_nubra,
        test_hospitals_type,
        test_emergency_ladakh,
        test_emergency_national,
        test_disease_dengue,
        test_disease_malaria,
        test_disease_tb,
        test_altitude_ladakh,
        test_altitude_spiti,
        test_health_schemes,
        test_health_schemes_medicine,
    ]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("All tests passed! 🎉")
