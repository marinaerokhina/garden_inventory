# Garden Inventory

**Python · PostgreSQL · SQLAlchemy · SQL**

Garden Inventory is a command-line inventory and sales reporting application developed from a university database coursework project. It demonstrates relational database design, database initialization, SQL querying, and Python–PostgreSQL integration.

> **Project status:** Educational CLI application. It is not a web API or a production service.

## Highlights

- **Five related PostgreSQL tables** with primary and foreign keys: `countries`, `manufacturers`, `providers`, `products`, and `product_details`.
- **Ten interactive operations** for inventory listings, filtering, and sales statistics.
- **Automated setup** of a local development database, tables, and approximately 70 synthetic inventory items.
- SQL techniques: multi-table `JOIN`, aggregation (`AVG`, `COUNT`), `GROUP BY`, `ILIKE`, and parameterized queries.
- Environment-based database configuration; no application password needs to be committed to the repository.

## What it does

| Functionality | Examples |
| --- | --- |
| Inventory catalogue | List products with manufacturer, supplier, price, and dates |
| Search | Find items by price range, manufacturer, or release date |
| Sales reports | View sales in a date range; list a customer's recent purchases |
| Statistics | Calculate overall and category-level average prices |
| Quality | Find defective inventory by manufacturer |

## Tech stack

- Python **3.10+** (uses `match` / `case`)
- PostgreSQL (tested version not specified)
- SQLAlchemy 2.x
- psycopg2
- python-dotenv

## Data model

```text
countries
 ├── manufacturers (country_id → countries.country_id)
 └── providers     (country_id → countries.country_id)

products
 ├── manufacturer_id → manufacturers.manufacturer_id
 └── provider_id     → providers.provider_id

product_details
 └── product_id → products.product_id
```

## Run locally

Requires **Python 3.10+** and a running **PostgreSQL** server. Copy `.env.example` to `.env` and enter your local database credentials.

From the project root:

```bash
pip install -r requirements.txt
python -m src.main
```

On first run, the application creates its development database and sample data. Your PostgreSQL user needs permission to create a database.

## Project structure

```text
garden_inventory/
├── src/
│   ├── config.py       # Environment-based database configuration
│   ├── db_setup.py     # Database/schema creation and synthetic test records
│   ├── db_func.py      # Inventory queries and reports
│   └── main.py         # CLI entry point
├── .env.example        # Example configuration; no real credentials
├── .gitignore
├── requirements.txt
├── КР-Ерохина.pdf      # Original university coursework (Russian)
└── README.md
```

## Implementation notes

- Schema relationships connect products to their manufacturers and suppliers, plus a separate table of sale-related details.
- User-provided query parameters are passed as bound values rather than concatenated into SQL.
- Database creation quotes the database identifier and checks for an existing database using a parameterized query.
- Synthetic inventory records are used rather than real customer data.

## Limitations and next steps

This is a local **educational** application. It has not yet been validated in an automated PostgreSQL integration test in a clean environment, and it currently has no test suite, Docker setup, REST API, or continuous integration.

Possible improvements: add integration tests, refactor CLI/error handling, offer a reproducible PostgreSQL setup with Docker Compose, and optionally expose selected operations through FastAPI.

## Background

Based on a university database coursework project. The original Russian documentation is included as `КР-Ерохина.pdf`.

**Author:** Marina Erokhina
