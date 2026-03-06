"""Data models and database operations for the ice cream shop."""

import sqlite3
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

DB_PATH = Path("icecream.db")


@dataclass
class Flavor:
    id: int | None
    name: str
    price: Decimal
    stock: int

    def to_row(self) -> tuple:
        return (self.name, str(self.price), self.stock)


@dataclass
class Order:
    id: int | None
    flavor_id: int
    scoops: int
    total: Decimal


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Create or open a SQLite connection and ensure tables exist."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    _create_tables(conn)
    return conn


def _create_tables(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS flavors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            price TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flavor_id INTEGER NOT NULL REFERENCES flavors(id),
            scoops INTEGER NOT NULL,
            total TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)


def add_flavor(conn: sqlite3.Connection, flavor: Flavor) -> int:
    """Insert a new flavor and return its id."""
    cursor = conn.execute(
        "INSERT INTO flavors (name, price, stock) VALUES (?, ?, ?)",
        flavor.to_row(),
    )
    conn.commit()
    return cursor.lastrowid  # type: ignore[return-value]


def list_flavors(conn: sqlite3.Connection) -> list[Flavor]:
    """Return all available flavors."""
    rows = conn.execute("SELECT id, name, price, stock FROM flavors").fetchall()
    return [Flavor(id=r[0], name=r[1], price=Decimal(r[2]), stock=r[3]) for r in rows]


def get_flavor(conn: sqlite3.Connection, flavor_id: int) -> Flavor | None:
    """Fetch a single flavor by id."""
    row = conn.execute(
        "SELECT id, name, price, stock FROM flavors WHERE id = ?", (flavor_id,)
    ).fetchone()
    if row is None:
        return None
    return Flavor(id=row[0], name=row[1], price=Decimal(row[2]), stock=row[3])


def update_stock(conn: sqlite3.Connection, flavor_id: int, delta: int) -> None:
    """Adjust stock for a flavor by delta (positive to add, negative to subtract)."""
    conn.execute(
        "UPDATE flavors SET stock = stock + ? WHERE id = ?", (delta, flavor_id)
    )
    conn.commit()


def insert_order(conn: sqlite3.Connection, order: Order) -> int:
    """Record an order and return its id."""
    cursor = conn.execute(
        "INSERT INTO orders (flavor_id, scoops, total) VALUES (?, ?, ?)",
        (order.flavor_id, order.scoops, str(order.total)),
    )
    conn.commit()
    return cursor.lastrowid  # type: ignore[return-value]


def list_orders(conn: sqlite3.Connection) -> list[dict]:
    """Return all orders with flavor names."""
    rows = conn.execute("""
        SELECT o.id, f.name, o.scoops, o.total, o.created_at
        FROM orders o JOIN flavors f ON o.flavor_id = f.id
        ORDER BY o.created_at DESC
    """).fetchall()
    return [
        {"id": r[0], "flavor": r[1], "scoops": r[2], "total": Decimal(r[3]), "created_at": r[4]}
        for r in rows
    ]
