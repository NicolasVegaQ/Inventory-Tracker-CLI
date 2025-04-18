# invemtory-Tracker-CLI

## Description:
Inventory is a CLI app that allows to manage inventory, allows to add products to the database, update the database and has user control where the admin user is the only one who can add products, allows to filter the database and list the database.

## Features

Inventory offers a range of functionalities that enable users to manage their product effectively:

- **Add a prodct**: Users can add a new product to their name, quantity, category, price an user. Each product is assigned a unique ID and is initially set to the "in-stock" status.
- **Delete a prodct**: product can be removed from the list by specifying their unique ID.
- **Update a prodct**: each product can be updated with the options of name, price, quantity and category. there is no need to update each field, you can update the column you want and the others without applying any changes.
- **List prodct**: Users can list all product or filter them by status, category, user.
- **low stock prodcut**: Users can filter by low stock with quantity thershod.

## Project Structure
- `main()`: The entry point of the application that handles command-line arguments and invokes the appropriate functions.
  - `load_database(path: str)`: Loads the task database from a JSON file.
  - `save_database(database: dict, path: str)`: Saves the task database to a JSON file.
  - `get_supported_queries()`: Returns a dictionary of supported commands and their configurations.
  - `get_querie(supported_queries: dict)`: Parses command-line arguments and returns the corresponding query function and arguments.
  - `add_product(database: dict[str, dict], name: str, quantity: int, category: str, price: float, user: str)`: Add a new prodcut with name, quantity, category, price, user, date time created and update.
  - `def list_product(database: dict[str, dict], status: "in-stock", user: = "all", category = "all")`: allows listing the database, filtering the product by status, user and category
 - `delete_product(database: dict[str,dict], id: str)`: Deleted product from databases
 - `update_product(database: dict[str, dict],id: str, name: str, quantity: int, category: str, price: float, status: str)`: Update product from databases, can be update name, quantity, category, price and status.
 - `low_stock(database: dict[str, dict], threshold: int)`: Allow filter databases by quantity threshold.
 -`positive(valor: str)`: Throws error if the threshold is less than zero.

## **Usage**: You can now run inventory from command line. Here are some example

- **Add a prodcut**
```bash
 inventory add -n "plato" -q 9 -c "concina y hogar" -p 1500 -u "bodega"
╭──────┬────────┬────────────┬─────────────────┬──────────────┬────────┬──────────┬─────────────────────┬─────────────────────╮
│   Id │ Name   │   Quantity │ Category        │   Unit Price │ user   │ Status   │ Created At          │ Updated At          │
├──────┼────────┼────────────┼─────────────────┼──────────────┼────────┼──────────┼─────────────────────┼─────────────────────┤
│    4 │ plato  │          9 │ concina y hogar │         1500 │ bodega │ in-stock │ 17/04/2025 20:00:36 │ 17/04/2025 20:00:36 │
╰──────┴────────┴────────────┴─────────────────┴──────────────┴────────┴──────────┴─────────────────────┴─────────────────────╯
  ```

- **Delete a Product**
```bash
inventory del 4 -u "admin"
╭──────┬────────┬────────────┬─────────────────┬──────────────┬────────┬──────────┬─────────────────────┬─────────────────────╮
│   Id │ Name   │   Quantity │ Category        │   Unit Price │ user   │ Status   │ Created At          │ Updated At          │
├──────┼────────┼────────────┼─────────────────┼──────────────┼────────┼──────────┼─────────────────────┼─────────────────────┤
│    4 │ plato  │          9 │ concina y hogar │         1500 │ bodega │ in-stock │ 17/04/2025 20:00:36 │ 17/04/2025 20:00:36 │
╰──────┴────────┴────────────┴─────────────────┴──────────────┴────────┴──────────┴─────────────────────┴─────────────────────╯
``` 

- **Update a product**
```bash
inventory update 1 -q 3
╭──────┬─────────────┬────────────┬──────────────┬──────────────┬────────┬──────────┬─────────────────────┬─────────────────────╮
│   Id │ Name        │   Quantity │ Category     │   Unit Price │ user   │ Status   │ Created At          │ Updated At          │
├──────┼─────────────┼────────────┼──────────────┼──────────────┼────────┼──────────┼─────────────────────┼─────────────────────┤
│    1 │ bateria 300 │          9 │ electronicos │         1500 │ admin  │ in-stock │ 17/04/2025 18:33:11 │ 17/04/2025 18:33:11 │
╰──────┴─────────────┴────────────┴──────────────┴──────────────┴────────┴──────────┴─────────────────────┴─────────────────────╯
╭──────┬─────────────┬────────────┬──────────────┬──────────────┬────────┬──────────┬─────────────────────┬─────────────────────╮
│   Id │ Name        │   Quantity │ Category     │   Unit Price │ user   │ Status   │ Created At          │ Updated At          │
├──────┼─────────────┼────────────┼──────────────┼──────────────┼────────┼──────────┼─────────────────────┼─────────────────────┤
│    1 │ bateria 300 │          3 │ electronicos │         1500 │ admin  │ in-stock │ 17/04/2025 18:33:11 │ 17/04/2025 20:06:37 │
╰──────┴─────────────┴────────────┴──────────────┴──────────────┴────────┴──────────┴─────────────────────┴─────────────────────╯
```

- **List products**
``` bash
inventory list -u "bodega"
╭──────┬────────────┬────────────┬──────────────┬──────────────┬────────┬──────────┬─────────────────────┬─────────────────────╮
│   Id │ Name       │   Quantity │ Category     │   Unit Price │ user   │ Status   │ Created At          │ Updated At          │
├──────┼────────────┼────────────┼──────────────┼──────────────┼────────┼──────────┼─────────────────────┼─────────────────────┤
│    3 │ bateria AA │          9 │ electronicos │         1500 │ bodega │ in-stock │ 17/04/2025 18:33:35 │ 17/04/2025 18:33:35 │
╰──────┴────────────┴────────────┴──────────────┴──────────────┴────────┴──────────┴─────────────────────┴─────────────────────╯
``` 

- **Filtr by quantity threshold**
```bash 
inventory low-stock -th 5
╭──────┬─────────────┬────────────┬──────────────┬──────────────┬────────┬──────────┬─────────────────────┬─────────────────────╮
│   Id │ Name        │   Quantity │ Category     │   Unit Price │ user   │ Status   │ Created At          │ Updated At          │
├──────┼─────────────┼────────────┼──────────────┼──────────────┼────────┼──────────┼─────────────────────┼─────────────────────┤
│    1 │ bateria 300 │          3 │ electronicos │         1500 │ admin  │ in-stock │ 17/04/2025 18:33:11 │ 17/04/2025 20:06:37 │
╰──────┴─────────────┴────────────┴──────────────┴──────────────┴────────┴──────────┴─────────────────────┴─────────────────────╯
``` 



