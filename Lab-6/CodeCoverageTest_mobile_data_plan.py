import pytest
from mobile_data_plan import overage_charge, recharge_allowed, validity_status


@pytest.mark.parametrize("plan,data,roaming,loyal,expected", [
    ("basic", 2, False, False, 0),
    ("standard", 6, False, True, 0),
    ("premium", 10, False, True, 0),
    ("basic", 5, False, False, 45),
    ("standard", 8, True, False, 120),
    ("basic", 13, False, False, 275),
    ("basic", 13, True, False, 605),
])
def test_overage_charge_valid_scenarios(plan, data, roaming, loyal, expected):
    assert overage_charge(plan, data, roaming, loyal) == expected


@pytest.mark.parametrize("plan,data", [
    ("gold", 1),
    ("basic", -1),
])
def test_overage_charge_invalid_inputs(plan, data):
    with pytest.raises(ValueError):
        overage_charge(plan, data, False, False)


@pytest.mark.parametrize("amount,pending,kyc,expected", [
    (200, 0, True, True),
    (201, 0, True, False),
    (500, 2, False, True),
    (500, 3, False, False),
    (2001, 0, False, False),
])
def test_recharge_allowed_scenarios(amount, pending, kyc, expected):
    assert recharge_allowed(amount, pending, kyc) is expected


@pytest.mark.parametrize("days,prepaid,addon,expected", [
    (0, True, False, "active"),
    (-1, True, False, "grace"),
    (-16, True, False, "expired"),
    (3, False, False, "active"),
    (2, False, False, "grace"),
    (-13, False, False, "expired"),
    (2, True, True, "active"),
    (1, True, True, "grace"),
])
def test_validity_status_scenarios(days, prepaid, addon, expected):
    assert validity_status(days, prepaid, addon) == expected
