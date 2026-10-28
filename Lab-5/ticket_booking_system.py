
"""Movie theater ticket booking and seating management module."""

import hashlib
import secrets

THEATER_SEATS = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}


def reserve_seat(seat_id, customer, order_history=None):
    """Reserve an available seat and record the booking."""
    if order_history is None:
        order_history = []

    if seat_id not in THEATER_SEATS or THEATER_SEATS[seat_id]["is_sold"]:
        return False

    THEATER_SEATS[seat_id]["is_sold"] = True
    order_history.append(f"Reserved seat {seat_id} for customer {customer}")
    return True


def cancel_seat(seat_id):
    """Cancel a reservation if the seat exists."""
    if seat_id not in THEATER_SEATS:
        return False

    THEATER_SEATS[seat_id]["is_sold"] = False
    return True


def check_seat_status(seat_id):
    """Return True when a seat exists and is available."""
    seat = THEATER_SEATS.get(seat_id)
    return seat is not None and not seat["is_sold"]


def compute_discounted_price(seat_id, discount_rate):
    """Calculate a discounted seat price using a rate between 0 and 1."""
    if seat_id not in THEATER_SEATS:
        raise ValueError(f"Unknown seat: {seat_id}")
    if not isinstance(discount_rate, (int, float)):
        raise TypeError("Discount rate must be numeric.")
    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    base_price = THEATER_SEATS[seat_id]["price"]
    return round(base_price * (1 - discount_rate), 2)


def generate_ticket_hash(ticket_code):
    """Return a SHA-256 digest for a ticket code."""
    return hashlib.sha256(ticket_code.encode("utf-8")).hexdigest()


def generate_booking_pin():
    """Generate a four-digit booking PIN using a secure random source."""
    return f"{secrets.randbelow(9000) + 1000}"


def export_seating_chart(filename="seating_chart.txt"):
    """Write the current seating chart to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as seating_file:
        seating_file.write(str(THEATER_SEATS))

    print(f"Seating chart exported to: {filename}")


def get_theater_summary(seats):
    """Return the number of sold seats."""
    return sum(1 for details in seats.values() if details["is_sold"])


def main():
    """Run a demonstration of the ticket-booking system."""
    reserve_seat("A1", "Sarah Connor")
    cancel_seat("A2")

    print("Is B1 available:", check_seat_status("B1"))
    print("Promo price:", compute_discounted_price("B1", 0.20))
    print("Ticket Hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())

    export_seating_chart()
    print("Sold count:", get_theater_summary(THEATER_SEATS))


if __name__ == "__main__":
    main()
