"""Sales reporting for the ice cream shop."""

import sqlite3
from decimal import Decimal


def total_revenue(conn: sqlite3.Connection) -> Decimal:
    """Calculate total revenue from all orders."""
    row = conn.execute("SELECT COALESCE(SUM(CAST(total AS REAL)), 0) FROM orders").fetchone()
    return Decimal(str(row[0]))


def sales_by_flavor(conn: sqlite3.Connection) -> list[dict]:
    """Get total scoops sold and revenue per flavor."""
    rows = conn.execute("""
        SELECT f.name, COALESCE(SUM(o.scoops), 0), COALESCE(SUM(CAST(o.total AS REAL)), 0)
        FROM flavors f
        LEFT JOIN orders o ON f.id = o.flavor_id
        GROUP BY f.id, f.name
        ORDER BY SUM(CAST(o.total AS REAL)) DESC
    """).fetchall()
    return [
        {"flavor": r[0], "scoops_sold": r[1], "revenue": Decimal(str(r[2]))}
        for r in rows
    ]


def top_flavor(conn: sqlite3.Connection) -> str | None:
    """Return the name of the best-selling flavor by revenue, or None if no sales."""
    rankings = sales_by_flavor(conn)
    if not rankings or rankings[0]["revenue"] == 0:
        return None
    return rankings[0]["flavor"]
