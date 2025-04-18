from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime
from tabulate import tabulate
from typing import Literal, Callable, Generator
import json
import os
import sys

USERS = ["admin","bodega","comercial","all"]
STATUS =  ["in-stock", "out-of-stock", "reserved", "all"]
CATEGORY = [
    "electronicos",
    "ferreteria",
    "plasticos",
    "limpieza e higiene",
    "concina y hogar",
    "alimentos y bebidas",
    "papeleria y oficina",
    "seguridad industrial",
    "all"
    ]
USERS_IN = [u for u in USERS if u != "all"]
CATEGORY_IN = [c for c in CATEGORY if c != "all"]


def load_database(path: str) -> dict[str, dict]:
    try:
        with open(path) as f:
            database = json.load(f)

    except FileNotFoundError:
        database = {}
    
    return database


def save_database(database: dict[str, dict], path: str) -> None:
    with open(path, "w") as f:
        database = json.dump(database, f)


def get_supported_queries() -> dict[str, dict]:
    return {
        "add": {
            "target": add_product,
            "help": "Add a new product to inventory",
            "args": [
                {
                    "name_or_flags": ["--name", "-n"], 
                    "help": "Name product in inventory",
                    "required": True
                 },
                 {
                     "name_or_flags":["--quantity","-q"],
                     "help": "Quantity product in inventory",
                     "required": True,
                     "type": int
                 },
                {
                     "name_or_flags":["--category","-c"],
                     "help": "Category product in inventory",
                     "choices": CATEGORY_IN,
                     "required": True
                 },
                 {
                     "name_or_flags":["--price","-p"],
                     "help": "Unit price product in inventory",
                     "required": True,
                     "type": float
                 },
                 {
                     "name_or_flags":["--user","-u"],
                     "help": "Product entered by the user in the inventory",
                     "choices": ["admin","bodega"],
                     "required": True
                 }
            ]
        },
        "del":{
            "target": delete_product,
            "help": "Remove product from inventory",
            "args":[
                {
                    "name_or_flags":["id"],
                    "help": "ID of product to remove from inventory"
                },
                 {
                     "name_or_flags":["--user","-u"],
                     "help": "User can delete product",
                     "choices": ["admin","bodega"],
                     "required": True
                 }
            ]
        },
        "list":{
            "target":list_product,
            "help": "Filter inventory by status a user",
            "args":[
                    {
                        "name_or_flags": ["--status", "-s"],
                        "help": "Filter inventory by status (default is 'all)",
                        "choices": STATUS,
                        "type": str.lower,
                        "default": "all"
                    },
                    {
                        "name_or_flags": ["--user", "-u"],
                        "help": "Filter inventory by user (default is 'all')",
                        "choices": USERS,
                        "type": str.lower,
                        "default": "all"
                    },
                    {
                        "name_or_flags": ["--category", "-c"],
                        "help": "Filter inventory by category (default is 'all')",
                        "choices": CATEGORY,
                        "type": str.lower,
                        "default": "all"
                    }
            ]
        },
        "update":{
            "target":update_product,
            "help": "Update inventory by id, name, category adn price",
            "args":[
                {
                    "name_or_flags": ["id"],
                    "help": "ID of product to update form inventory",
                },
                {
                    "name_or_flags": ["--name", "-n"], 
                    "help": "Name product in inventory to be update",
                },
                {
                     "name_or_flags":["--quantity","-q"],
                     "help": "Quantity product in inventory to be update",
                     "type": int
                },
                {
                     "name_or_flags":["--category","-c"],
                     "help": "Category product in inventory to be update",
                     "choices": CATEGORY_IN,
                 },
                 {
                     "name_or_flags":["--price","-p"],
                     "help": "Unit price product in inventory to be update",
                     "type": float
                 },
                {
                    "name_or_flags": ["--status", "-s"],
                    "help": "Update status of the product",
                    "choices": STATUS,
                    "type": str.lower,
                },
            ]
        },
        "low-stock":{
            "target":low_stock,
            "help": "filters out low stock products from a quantity threshold",
            "args": [
                {
                     "name_or_flags":["--threshold","-th"],
                     "help": "Products can be listed by quantity threshold ",
                     "type": positive,
                     "required": True                    
                }
            ]
        }
    }


def get_querie(supported_queries: dict[str, dict]) -> tuple[Callable, dict]:
    """
    ArgumentParser (parser)
    └── sub_parsers = parser.add_subparsers(...)  ← agrupa subcomandos
            ├── p = sub_parsers.add_parser("add") ← comando específico
            │      └── p.add_argument(...)        ← argumentos del comando
            ├── p = sub_parsers.add_parser("list")
            │      └── p.add_argument(...)
            └── etc...
    """
    parser: ArgumentParser = ArgumentParser(
        description="A CLI application to efficiently manage your inventory"
    )
    sub_parsers = parser.add_subparsers(title="commands", dest="command", required=True)
    for name, properties in supported_queries.items():
        #construye el el ArgumentParse con todos los usbcomando y su descripcion
        p = sub_parsers.add_parser(name, help=properties["help"])
        for arg in properties["args"]:
            p.add_argument(*arg.pop("name_or_flags"), **arg)

    # Namespace(command='add', description='tarea urgente')
    args: dict = parser.parse_args().__dict__ #captura lo que escriben en consola y lo convierte en diccionario
    querie: Callable = supported_queries[args.pop("command")]["target"]

    return querie, args


def add_product(database: dict[str, dict], name: str, quantity: int, category: str, price: float, user: str) -> None:
    if dict(filter(lambda item: item[1].get("name", "") == name, database.items())):
        raise ArgumentTypeError("There is already a product with the name to be saved")
        
    today: str = datetime.today().isoformat()
    id: str = str(int(max("0", *database.keys())) + 1)
    database[id] = {
        "name": name,
        "quantity": quantity,
        "category": category,
        "unit_price": price,
        "user":user,
        "status": "in-stock",
        "created-at": today,
        "updated-at": today,
    }
    list_product({id: database[id]})


def list_product(
    database: dict[str, dict],
    status: Literal["in-stock", "out-of-stock", "reserved"] = "in-stock",
    user: Literal["admin", "bodega", "comercial","all"] = "all",
    category = "all"
) -> None:
    DATETIME_FORMAT: str = "%d/%m/%Y %H:%M:%S"

    table: Generator = (
        {
            "Id": id,
            "Name": properties["name"],
            "Quantity": properties["quantity"],
            "Category": properties["category"],
            "Unit Price": properties["unit_price"],
            "user": properties["user"],
            "Status": properties["status"],
            "Created At": datetime.fromisoformat(properties["created-at"]).strftime(
                DATETIME_FORMAT
            ),
            "Updated At": datetime.fromisoformat(properties["updated-at"]).strftime(
                DATETIME_FORMAT
            ),
        }
        for id, properties in sorted(database.items(), key=lambda t: t[0])
        if (status == "all" or status == properties["status"]) and (user == "all" or user == properties["user"]) and (category == "all" or category == properties["category"])
    )

    print(
        tabulate(table, tablefmt="rounded_grid", headers="keys") or "Nothing to display"
    )


def delete_product(database: dict[str,dict], id: str, user: str) -> None:
    list_product({id: database[id]})
    del database[id]


def update_product(database: dict[str, dict],id: str, name: str, quantity: int, category: str, price: float, status: str) -> None:
    list_product({id: database[id]})
    updated = False
    for key, value in locals().items():
        if key not in ("database", "id") and value:
            if key == "price":
                key = "unit_price"
            database[id][key] = value
            updated = True
    if updated:
        database[id]["updated-at"] = datetime.today().isoformat()
    list_product({id: database[id]})
    

def low_stock(database: dict[str, dict], threshold: int) -> None: 
    database_filter = dict(
    filter(lambda item: item[1].get("quantity", 0) < threshold, database.items())
    )
    list_product(database_filter)


def positive(valor: str) -> int:
    iv = int(valor)
    if iv <= 0:
        raise ArgumentTypeError("Value must be geater than zero")
    return iv


def main () -> None:
    supported_queries: dict[str, dict] = get_supported_queries()
    querie, args = get_querie(supported_queries)
    PATH_DATABASES: str = os.path.expanduser(r"~\dbInventory.json")
    database = load_database(PATH_DATABASES)
    try:
        querie(database,**args)
    except KeyError:
        sys.exit("No product fount with the provide ID")
    save_database(database, PATH_DATABASES)