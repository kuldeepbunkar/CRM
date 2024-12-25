#!/usr/bin/env python
import click
from src.crm import CRM
from src.utils.database import Database

@click.group()
def cli():
    pass

@cli.command()
def init_db():
    """Initialize the database"""
    db = Database()
    click.echo("Database initialized successfully")

@cli.command()
@click.option('--year', type=int, required=True)
@click.option('--month', type=int, required=True)
def generate_monthly_report(year, month):
    """Generate monthly sales report"""
    crm = CRM()
    report = crm.get_monthly_sales_report(year, month)
    click.echo(f"Report generated for {year}-{month}")
    click.echo(report)

if __name__ == '__main__':
    cli() 