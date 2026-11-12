import math

def parse_plan(text):
    """Parse a plan description in the format 'plan:data_gb'."""
    if not isinstance(text, str):
        raise TypeError("plan input must be a string")

    if text.count(":") != 1:
        raise ValueError("expected format 'plan:data_gb'")

    plan, gb_text = text.split(":")
    plan = plan.strip()
    if not plan:
        raise ValueError("plan name cannot be empty")

    try:
        gb = float(gb_text.strip())
    except ValueError as exc:
        raise ValueError("data amount must be a number") from exc

    if not math.isfinite(gb) or gb < 0:
        raise ValueError("data amount must be a finite, non-negative number")

    return plan.title(), gb


def usage_average(usage_csv):
    """Return the integer average of comma-separated daily usage values."""
    if not isinstance(usage_csv, str):
        raise TypeError("usage input must be a string")

    if not usage_csv.strip():
        raise ValueError("usage list cannot be empty")

    parts = usage_csv.split(",")
    try:
        values = [int(part.strip()) for part in parts]
    except ValueError as exc:
        raise ValueError("usage values must be integers") from exc

    if any(value < 0 for value in values):
        raise ValueError("usage values cannot be negative")

    return sum(values) // len(values)


def payable_bill(text):
    """Calculate the bill including 18% tax, less a discount."""
    if not isinstance(text, str):
        raise TypeError("bill input must be a string")

    if text.count("|") != 1:
        raise ValueError("expected format 'bill|discount'")

    bill_text, discount_text = text.split("|")
    try:
        bill = float(bill_text.strip())
        discount = float(discount_text.strip())
    except ValueError as exc:
        raise ValueError("bill and discount must be numbers") from exc

    if not math.isfinite(bill) or not math.isfinite(discount):
        raise ValueError("bill and discount must be finite numbers")
    if bill < 0 or discount < 0:
        raise ValueError("bill and discount cannot be negative")

    total = bill * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_plan ====")
    user_input = input("Enter plan:data in GB (e.g. standard:5): ")
    try:
        result = parse_plan(user_input)
        print("Plan and Data:", result)
    except (ValueError, TypeError) as exc:
        print("Invalid plan input:", exc)
        return

    print("\n==== Running usage_average ====")
    user_input = input("Enter daily usage in MB as CSV (e.g. 300,450,800): ")
    try:
        result = usage_average(user_input)
        print("Average Usage:", result)
    except (ValueError, TypeError) as exc:
        print("Invalid usage input:", exc)
        return

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 399|50): ")
    try:
        result = payable_bill(user_input)
        print("Payable Bill:", result)
    except (ValueError, TypeError) as exc:
        print("Invalid bill input:", exc)


if __name__ == "__main__":
    main()
