"""Tests for sales reporting."""

import sqlite3
from decimal import Decimal

from icecream.reports import sales_by_flavor, top_flavor, total_revenue
from icecream.shop import create_flavor, place_order


def test_total_revenue_empty(conn: sqlite3.Connection) -> None:
    assert total_revenue(conn) == Decimal("0")


def test_total_revenue(conn: sqlite3.Connection) -> None:
    f1 = create_flavor(conn, "Vanilla", Decimal("3.00"), stock=20)
    f2 = create_flavor(conn, "Chocolate", Decimal("4.00"), stock=20)
    place_order(conn, f1.id, scoops=2)  # 6.00
    place_order(conn, f2.id, scoops=3)  # 12.00
    assert total_revenue(conn) == Decimal("18.0")


def test_sales_by_flavor(conn: sqlite3.Connection) -> None:
    f1 = create_flavor(conn, "Vanilla", Decimal("3.00"), stock=20)
    f2 = create_flavor(conn, "Chocolate", Decimal("4.00"), stock=20)
    place_order(conn, f1.id, scoops=1)
    place_order(conn, f2.id, scoops=5)

    report = sales_by_flavor(conn)
    assert len(report) == 2
    assert report[0]["flavor"] == "Chocolate"  # higher revenue first
    assert report[0]["scoops_sold"] == 5


def test_top_flavor_no_sales(conn: sqlite3.Connection) -> None:
    create_flavor(conn, "Vanilla", Decimal("3.00"), stock=10)
    assert top_flavor(conn) is None


def test_top_flavor(conn: sqlite3.Connection) -> None:
    f1 = create_flavor(conn, "Vanilla", Decimal("3.00"), stock=20)
    f2 = create_flavor(conn, "Chocolate", Decimal("4.00"), stock=20)
    place_order(conn, f1.id, scoops=1)
    place_order(conn, f2.id, scoops=5)
    assert top_flavor(conn) == "Chocolate"
