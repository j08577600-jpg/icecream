"""Tests for data models and database operations."""

import sqlite3
from decimal import Decimal

from icecream.models import Flavor, add_flavor, get_flavor, list_flavors, update_stock


def test_add_and_get_flavor(conn: sqlite3.Connection) -> None:
    flavor = Flavor(id=None, name="Vanilla", price=Decimal("3.50"), stock=10)
    fid = add_flavor(conn, flavor)
    assert fid is not None

    result = get_flavor(conn, fid)
    assert result is not None
    assert result.name == "Vanilla"
    assert result.price == Decimal("3.50")
    assert result.stock == 10


def test_list_flavors(conn: sqlite3.Connection) -> None:
    add_flavor(conn, Flavor(id=None, name="Chocolate", price=Decimal("4.00"), stock=5))
    add_flavor(conn, Flavor(id=None, name="Strawberry", price=Decimal("3.75"), stock=8))

    flavors = list_flavors(conn)
    assert len(flavors) == 2
    names = {f.name for f in flavors}
    assert names == {"Chocolate", "Strawberry"}


def test_update_stock(conn: sqlite3.Connection) -> None:
    fid = add_flavor(conn, Flavor(id=None, name="Mint", price=Decimal("3.00"), stock=10))
    update_stock(conn, fid, -3)

    flavor = get_flavor(conn, fid)
    assert flavor is not None
    assert flavor.stock == 7


def test_get_flavor_not_found(conn: sqlite3.Connection) -> None:
    assert get_flavor(conn, 999) is None
