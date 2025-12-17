import sys

from src.db_setup import *
from src.db_func import *

database_name = "inventory_db"
User = "postgres"
Password = "admin"
Host = "localhost"
Port = "5432"
DB_url = f"postgresql+psycopg2://{User}:{Password}@{Host}:{Port}/{database_name}"
Engine = setup_database(database_name, User, Password, Host, Port)
try:
    with Engine.connect() as conn:
        Result = conn.execute(text("SELECT 1"))
        print(f"Connection detected: {str(Result.first()[0])}")
except Exception as e:
    print("Connection error: ", e)

print("What func do you want to use? Enter the func number:\n"
      "1. product_information()\n"
      "2. sort_by_price()\n"
      "3. average_price()\n"
      "4. products_by_price_range(min_price FLOAT, max_price FLOAT)\n"
      "5. products_by_manufacturer(manufacturer__name STRING)\n"
      "6. products_by_release_date(release__date DATE)\n"
      "7. products_by_sale_date_range(start_date DATE, end_date DATE)\n"
      "8. avg_price_by_sale_period(start_date DATE, end_date DATE)\n"
      "9. defective_items_by_manufacturer(manufacturer__name STRING)\n"
      "10. items_sold_to_customer_last_6_months(customer__name STRING)\n")
num = 0
try:
    n = input()
    num = int(n)
except Exception as e:
    print("Invalid input. Please, be careful, you need to input number. Now you need to restart program")
    sys.exit()
match num:
    case 1:
        product_information()
    case 2:
        sort_by_price()
    case 3:
        average_price()
    case 4:
        products_by_price_range()
    case 5:
        products_by_manufacturer()
    case 6:
        products_by_release_date()
    case 7:
        products_by_sale_date_range()
    case 8:
        avg_price_by_sale_period()
    case 9:
        defective_items_by_manufacturer()
    case 10:
        items_sold_to_customer_last_6_months()
    case _:
        print("Non-existent func chose.")
        sys.exit()

