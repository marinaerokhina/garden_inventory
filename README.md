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

## Getting started

### 1. Prerequisites

Install **Python 3.10+** and **PostgreSQL**. Start your PostgreSQL server. Your development PostgreSQL user must be allowed to create a database if `inventory_db` does not yet exist.

### 2. Install

```bash
git clone https://github.com/marinaerokhina/garden_inventory.git
cd garden_inventory
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS / Linux: `source .venv/bin/activate`

Then:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure PostgreSQL

Copy `.env.example` to `.env` (in the repository root) and fill in your **own local** PostgreSQL credentials:

```dotenv
DB_NAME=inventory_db
DB_USER=postgres
DB_PASSWORD=your-local-password
DB_HOST=localhost
DB_PORT=5432
```

**Never commit the real `.env` file.** It is excluded by `.gitignore`. If you change the database name or user, adjust the values to match your PostgreSQL installation.

### 4. Run

From the **repository root**:

```bash
python -m src.main
```

On first initialization, the application creates the development database if needed, creates missing tables, and inserts synthetic sample records. Select a menu option from 1 to 10 to run a query or report.

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
