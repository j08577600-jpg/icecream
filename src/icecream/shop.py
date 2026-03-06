"""Core business logic for the ice cream shop."""

import sqlite3
from decimal import Decimal

from icecream.models import (
    Flavor,
    Order,
    add_flavor,
    get_flavor,
    insert_order,
    update_stock,
)


class ShopError(Exception):
    """Raised when a shop operation fails."""


def create_flavor(conn: sqlite3.Connection, name: str, price: Decimal, stock: int) -> Flavor:
    """Add a new ice cream flavor to the shop."""
    if price <= 0:
        raise ShopError("Price must be positive")
    if stock < 0:
        raise ShopError("Stock cannot be negative")
    flavor = Flavor(id=None, name=name, price=price, stock=stock)
    flavor.id = add_flavor(conn, flavor)
    return flavor


def place_order(conn: sqlite3.Connection, flavor_id: int, scoops: int) -> Order:
    """Place an order for scoops of a given flavor."""
    if scoops < 1:
        raise ShopError("Must order at least 1 scoop")

    flavor = get_flavor(conn, flavor_id)
    if flavor is None:
        raise ShopError(f"Flavor {flavor_id} not found")
    if flavor.stock < scoops:
        raise ShopError(f"Not enough stock: {flavor.stock} available, {scoops} requested")

    total = flavor.price * scoops
    order = Order(id=None, flavor_id=flavor_id, scoops=scoops, total=total)
    order.id = insert_order(conn, order)
    update_stock(conn, flavor_id, -scoops)
    return order


def restock(conn: sqlite3.Connection, flavor_id: int, amount: int) -> Flavor:
    """Add stock to a flavor."""
    if amount < 1:
        raise ShopError("Restock amount must be at least 1")
    flavor = get_flavor(conn, flavor_id)
    if flavor is None:
        raise ShopError(f"Flavor {flavor_id} not found")
    update_stock(conn, flavor_id, amount)
    flavor.stock += amount
    return flavor
