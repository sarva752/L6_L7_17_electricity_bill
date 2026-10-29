import pytest
from electricity_bill import energy_charge, late_fee, subsidy


def test_low_usage_domestic():
    assert energy_charge(50, "domestic") == 200


def test_unknown_connection_raises():
    with pytest.raises(ValueError):
        energy_charge(100, "industrial")


def test_negative_units_raises():
    with pytest.raises(ValueError):
        energy_charge(-1, "domestic")


def test_mid_usage_domestic():
    assert energy_charge(200, "domestic") == 850


def test_high_usage_commercial():
    assert energy_charge(400, "commercial") == 4350


def test_paid_on_time():
    assert late_fee(500, 0) == 0


def test_slightly_late():
    assert late_fee(500, 10) == 50


def test_very_late_large_bill():
    assert late_fee(3000, 20) == 250


def test_senior_low_usage():
    assert subsidy(50, True, False) == 50


def test_solar_high_usage_loses_subsidy():
    assert subsidy(400, False, True) == 0