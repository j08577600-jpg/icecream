"""Tests for core business logic."""

import sqlite3
from decimal import Decimal

import pytest

from icecream.shop import ShopError, create_flavor, place_order, restock


def test_create_flavor(conn: sqlite3.Connection) -> None:
    flavor = create_flavor(conn, "Vanilla", Decimal("3.50"), stock=10)
    assert flavor.id is not None
    assert flavor.name == "Vanilla"


def test_create_flavor_invalid_price(conn: sqlite3.Connection) -> None:
    with pytest.raises(ShopError, match="Price must be positive"):
        create_flavor(conn, "Bad", Decimal("0"), stock=1)


def test_create_flavor_negative_stock(conn: sqlite3.Connection) -> None:
    with pytest.raises(ShopError, match="Stock cannot be negative"):
        create_flavor(conn, "Bad", Decimal("1.00"), stock=-1)


def test_place_order(conn: sqlite3.Connection) -> None:
    flavor = create_flavor(conn, "Chocolate", Decimal("4.00"), stock=10)
    order = place_order(conn, flavor.id, scoops=3)
    assert order.total == Decimal("12.00")
    assert order.scoops == 3


def test_place_order_insufficient_stock(conn: sqlite3.Connection) -> None:
    flavor = create_flavor(conn, "Mango", Decimal("5.00"), stock=2)
    with pytest.raises(ShopError, match="Not enough stock"):
        place_order(conn, flavor.id, scoops=5)


def test_place_order_unknown_flavor(conn: sqlite3.Connection) -> None:
    with pytest.raises(ShopError, match="not found"):
        place_order(conn, 999, scoops=1)


def test_place_order_zero_scoops(conn: sqlite3.Connection) -> None:
    flavor = create_flavor(conn, "Lemon", Decimal("3.00"), stock=5)
    with pytest.raises(ShopError, match="at least 1 scoop"):
        place_order(conn, flavor.id, scoops=0)


def test_restock(conn: sqlite3.Connection) -> None:
    flavor = create_flavor(conn, "Pistachio", Decimal("4.50"), stock=3)
    updated = restock(conn, flavor.id, amount=10)
    assert updated.stock == 13


def test_restock_invalid_amount(conn: sqlite3.Connection) -> None:
    flavor = create_flavor(conn, "Coffee", Decimal("4.00"), stock=5)
    with pytest.raises(ShopError, match="at least 1"):
        restock(conn, flavor.id, amount=0)
