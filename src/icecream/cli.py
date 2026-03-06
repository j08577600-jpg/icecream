"""CLI entry points for the ice cream shop."""

from decimal import Decimal

import click

from icecream.models import get_connection, list_flavors, list_orders
from icecream.reports import sales_by_flavor, top_flavor, total_revenue
from icecream.shop import ShopError, create_flavor, place_order, restock


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    """Ice Cream Shop management CLI."""
    ctx.ensure_object(dict)
    ctx.obj["conn"] = get_connection()


@main.command()
@click.argument("name")
@click.argument("price", type=float)
@click.option("--stock", default=0, help="Initial stock quantity")
@click.pass_context
def add(ctx: click.Context, name: str, price: float, stock: int) -> None:
    """Add a new ice cream flavor."""
    try:
        flavor = create_flavor(ctx.obj["conn"], name, Decimal(str(price)), stock)
        click.echo(
            f"Added flavor '{flavor.name}' (id={flavor.id}, ${flavor.price}, stock={flavor.stock})"
        )
    except ShopError as e:
        raise click.ClickException(str(e))


@main.command()
def flavors() -> None:
    """List all available flavors."""
    conn = get_connection()
    for f in list_flavors(conn):
        click.echo(f"  [{f.id}] {f.name} — ${f.price} ({f.stock} in stock)")


@main.command()
@click.argument("flavor_id", type=int)
@click.argument("scoops", type=int)
@click.pass_context
def order(ctx: click.Context, flavor_id: int, scoops: int) -> None:
    """Place an order for scoops of a flavor."""
    try:
        o = place_order(ctx.obj["conn"], flavor_id, scoops)
        click.echo(f"Order #{o.id}: {scoops} scoop(s), total ${o.total}")
    except ShopError as e:
        raise click.ClickException(str(e))


@main.command()
@click.argument("flavor_id", type=int)
@click.argument("amount", type=int)
@click.pass_context
def stock(ctx: click.Context, flavor_id: int, amount: int) -> None:
    """Restock a flavor."""
    try:
        f = restock(ctx.obj["conn"], flavor_id, amount)
        click.echo(f"Restocked '{f.name}' — now {f.stock} in stock")
    except ShopError as e:
        raise click.ClickException(str(e))


@main.command()
def report() -> None:
    """Show sales report."""
    conn = get_connection()
    click.echo(f"Total revenue: ${total_revenue(conn)}")
    click.echo()
    best = top_flavor(conn)
    if best:
        click.echo(f"Top flavor: {best}")
    click.echo()
    click.echo("Sales by flavor:")
    for row in sales_by_flavor(conn):
        click.echo(f"  {row['flavor']}: {row['scoops_sold']} scoops, ${row['revenue']}")


@main.command()
def orders() -> None:
    """List all orders."""
    conn = get_connection()
    for o in list_orders(conn):
        click.echo(f"  #{o['id']} {o['flavor']} x{o['scoops']} — ${o['total']} ({o['created_at']})")
