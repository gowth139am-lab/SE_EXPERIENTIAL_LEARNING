import pytest
from hypothesis import given, strategies as st

from mobile_data_plan import parse_plan, usage_average, payable_bill


# parse_plan: valid generated inputs
@given(
    plan=st.text(min_size=1).filter(
        lambda value: ":" not in value and bool(value.strip())
    ),
    gb=st.floats(
        min_value=0,
        max_value=1000,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_parse_plan_valid(plan, gb):
    result = parse_plan(f"{plan}:{gb}")
    assert result == (plan.strip().title(), float(gb))


@given(
    st.one_of(
        st.none(),
        st.sampled_from(["", "standard", ":5", "standard:", "a:1:2",
                         "standard:abc", "standard:-1", "standard:nan",
                         "standard:inf"]),
    )
)
def test_parse_plan_rejects_invalid_input(value):
    with pytest.raises((ValueError, TypeError)):
        parse_plan(value)


# usage_average: valid generated CSV inputs
@given(st.lists(st.integers(min_value=0, max_value=100000), min_size=1))
def test_usage_average_valid(values):
    csv_input = ",".join(str(value) for value in values)
    assert usage_average(csv_input) == sum(values) // len(values)


@given(
    st.one_of(
        st.none(),
        st.sampled_from(["", " ", "abc", "1,,2", ",1", "1,",
                         "1.5,2", "-1,2"]),
    )
)
def test_usage_average_rejects_invalid_input(value):
    with pytest.raises((ValueError, TypeError)):
        usage_average(value)


# payable_bill: valid generated inputs
@given(
    bill=st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False,
    ),
    discount=st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_payable_bill_valid(bill, discount):
    result = payable_bill(f"{bill}|{discount}")
    assert result == max(float(bill) * 1.18 - float(discount), 0)


@given(
    st.one_of(
        st.none(),
        st.sampled_from(["", "399", "|50", "399|", "1|2|3",
                         "abc|50", "399|xyz", "-1|5", "399|-5",
                         "nan|5", "inf|5"]),
    )
)
def test_payable_bill_rejects_invalid_input(value):
    with pytest.raises((ValueError, TypeError)):
        payable_bill(value)
