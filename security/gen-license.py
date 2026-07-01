#!/usr/bin/env python3
"""
GP Trading — Generador de Licencias (CLI)
Uso: python gen-license.py --account sim-12345678 --product tradesyncer [--email cliente@email.com] [--name "Cliente Name"]
"""

import hashlib
import sqlite3
import argparse
import os
from datetime import datetime

MASTER_SECRET = "__MASTER_SECRET__"

PRODUCTS = {
    "tradesyncer": "TradeSyncer PRO v2.0",
    "firmcopier": "GP Firm Copier Pro",
    "riskreward": "GPRiskReward",
    "gflowpro": "OmniFlow GFlow PRO v2.0",
    "gflowx": "OmniFlow GFlow X",
    "quantumprime": "OmniFlow Quantum Prime",
    "gflowpremium": "GFlow Pro Premium",
    "vpwap": "GP VWAP Clásico",
    "nexus": "Nexus Trend Engine",
    "specter": "Specter Trend Cloud",
    "gpcuantum": "GPCuantum X",
}

DB_PATH = os.path.join(os.path.dirname(__file__), "licencias.db")


def generate_key(account_id: str, product_id: str) -> str:
    data = f"{account_id}|{product_id}|{MASTER_SECRET}"
    h = hashlib.sha256(data.encode()).hexdigest().upper()
    return f"GPTR-{h[0:5]}-{h[5:10]}-{h[10:15]}-{h[15:20]}"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS licencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_key TEXT UNIQUE NOT NULL,
            producto TEXT NOT NULL,
            product_id TEXT NOT NULL,
            nt8_account_id TEXT NOT NULL,
            customer_email TEXT,
            customer_name TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            revocada INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    return conn


def save_to_db(conn, key: str, product_name: str, product_id: str,
               account_id: str, email: str, name: str):
    conn.execute(
        "INSERT INTO licencias (license_key, producto, product_id, nt8_account_id, customer_email, customer_name) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (key, product_name, product_id, account_id, email or "", name or email or ""),
    )
    conn.commit()


def save_lic_file(key: str, product_id: str, output_dir: str = None):
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), "licencias_generadas")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{product_id}.lic")
    with open(filepath, "w") as f:
        f.write(key + "\n")
    return filepath


def list_licenses(conn):
    rows = conn.execute(
        "SELECT id, license_key, producto, nt8_account_id, customer_name, created_at, revocada "
        "FROM licencias ORDER BY created_at DESC"
    ).fetchall()

    if not rows:
        print("\nNo hay licencias registradas.")
        return

    print(f"\n{'ID':<4} {'License Key':<30} {'Producto':<30} {'Account ID':<20} {'Cliente':<20} {'Fecha':<20} {'Estado':<10}")
    print("-" * 140)
    for row in rows:
        estado = "Revocada" if row[6] else "Activa"
        print(f"{row[0]:<4} {row[1]:<30} {row[2]:<30} {row[3]:<20} {row[4][:18]:<20} {row[5][:18]:<20} {estado:<10}")


def revoke_license(conn, license_id: int):
    conn.execute("UPDATE licencias SET revocada = 1 WHERE id = ?", (license_id,))
    conn.commit()
    if conn.total_changes:
        print(f"Licencia ID {license_id} revocada.")
    else:
        print(f"No se encontró licencia con ID {license_id}.")


def main():
    parser = argparse.ArgumentParser(
        description="GP Trading — Generador de Licencias NT8",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python gen-license.py --account sim-12345678 --product tradesyncer
  python gen-license.py --account real-87654321 --product firmcopier --email cliente@email.com --name "Juan Perez"
  python gen-license.py --list
  python gen-license.py --revoke 5
        """,
    )
    parser.add_argument("--account", help="NT8 Account ID del cliente")
    parser.add_argument("--product", choices=list(PRODUCTS.keys()), help="ID del producto")
    parser.add_argument("--email", help="Email del cliente (opcional)")
    parser.add_argument("--name", help="Nombre del cliente (opcional)")
    parser.add_argument("--output", help="Directorio para guardar el archivo .lic")
    parser.add_argument("--list", action="store_true", help="Listar todas las licencias")
    parser.add_argument("--revoke", type=int, help="Revocar licencia por ID")
    parser.add_argument("--no-save", action="store_true", help="No guardar en BD ni archivo (solo mostrar)")
    parser.add_argument("--secret", help="Override del MASTER_SECRET (variable de entorno GPT_LICENSE_SECRET)")

    args = parser.parse_args()

    global MASTER_SECRET
    if args.secret:
        MASTER_SECRET = args.secret
    elif os.environ.get("GPT_LICENSE_SECRET"):
        MASTER_SECRET = os.environ["GPT_LICENSE_SECRET"]

    conn = init_db()

    if args.list:
        list_licenses(conn)
        conn.close()
        return

    if args.revoke is not None:
        revoke_license(conn, args.revoke)
        conn.close()
        return

    if not args.account or not args.product:
        parser.print_help()
        print("\nERROR: Debes especificar --account y --product")
        conn.close()
        return

    account_id = args.account.strip()
    product_id = args.product
    product_name = PRODUCTS[product_id]
    email = (args.email or "").strip()
    name = (args.name or "").strip()

    key = generate_key(account_id, product_id)

    print("\n" + "=" * 60)
    print("  GP TRADING — Licencia Generada")
    print("=" * 60)
    print(f"  Producto:     {product_name}")
    print(f"  Product ID:   {product_id}")
    print(f"  Account ID:   {account_id}")
    print(f"  Cliente:      {name or email or '(no especificado)'}")
    print(f"  Email:        {email or '(no especificado)'}")
    print("-" * 60)
    print(f"  LICENSE KEY:  {key}")
    print("=" * 60)

    if not args.no_save:
        save_to_db(conn, key, product_name, product_id, account_id, email, name)
        filepath = save_lic_file(key, product_id, args.output)
        print(f"\n  Archivo .lic: {filepath}")
        print(f"  BD auditoría: {DB_PATH}")
        print(f"\n  Instrucciones para el cliente:")
        print(f"  1. Copiar {product_id}.lic a:")
        print(f"     Documents\\NinjaTrader 8\\bin\\Custom\\Licenses\\")
        print(f"  2. Copiar la DLL a:")
        print(f"     Documents\\NinjaTrader 8\\bin\\Custom\\")
    else:
        print("\n  (modo --no-save: no se guardó en BD ni archivo)")

    conn.close()


if __name__ == "__main__":
    main()
