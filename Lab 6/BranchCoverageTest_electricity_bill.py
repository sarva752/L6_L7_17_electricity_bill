import pytest
from electricity_bill import energy_charge, late_fee, subsidy


def test_unknown_connection_raises():
    with pytest.raises(ValueError, match="unknown connection"):
        energy_charge(100, "industrial")


def test_negative_units_raises():
    with pytest.raises(ValueError, match="invalid units"):
        energy_charge(-1, "domestic")


def test_unknown_connection_checked_before_units():
    with pytest.raises(ValueError, match="unknown connection"):
        energy_charge(-5, "industrial")


def test_low_usage_domestic():
    assert energy_charge(50, "domestic") == 200


def test_zero_units_domestic():
    assert energy_charge(0, "domestic") == 50


def test_slab1_upper_boundary_100():
    assert energy_charge(100, "domestic") == 350


def test_slab2_lower_boundary_101():
    assert energy_charge(101, "domestic") == 355


def test_slab2_upper_boundary_300():
    assert energy_charge(300, "domestic") == 1350


def test_slab3_lower_boundary_301():
    assert energy_charge(301, "domestic") == 1358


def test_slab3_high_usage_domestic():
    assert energy_charge(400, "domestic") == 2150


def test_commercial_slab1():
    assert energy_charge(100, "commercial") == 750


def test_commercial_slab2():
    assert energy_charge(200, "commercial") == 1750


def test_commercial_slab3():
    assert energy_charge(400, "commercial") == 4350


def test_paid_on_time():
    assert late_fee(500, 0) == 0


def test_negative_days_late():
    assert late_fee(500, -5) == 0


def test_late_one_day():
    assert late_fee(500, 1) == 50


def test_late_boundary_15_days():
    assert late_fee(500, 15) == 50


def test_late_boundary_16_days_small_bill():
    assert late_fee(500, 16) == 100


def test_late_bill_exactly_2000_no_surcharge():
    assert late_fee(2000, 16) == 100


def test_late_bill_just_above_2000_surcharge():
    assert late_fee(2001, 16) == 200


def test_very_late_large_bill():
    assert late_fee(3000, 30) == 250


def test_senior_low_usage():
    assert subsidy(50, True, False) == 50


def test_senior_boundary_100_units():
    assert subsidy(100, True, False) == 50


def test_senior_above_100_units_no_subsidy():
    assert subsidy(101, True, False) == 0


def test_non_senior_low_usage_no_subsidy():
    assert subsidy(50, False, False) == 0


def test_solar_only():
    assert subsidy(50, False, True) == 100


def test_senior_and_solar_stack():
    assert subsidy(50, True, True) == 150


def test_solar_boundary_300_units_keeps_subsidy():
    assert subsidy(300, False, True) == 100


def test_solar_above_300_units_loses_subsidy():
    assert subsidy(301, False, True) == 0


def test_senior_solar_above_300_units_loses_subsidy():
    assert subsidy(301, True, True) == 0