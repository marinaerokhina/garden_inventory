from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import sys


def get_engine():
    """Получить подключение к базе данных в зависимости от роли пользователя"""
    # В реальном проекте здесь должна быть логика определения роли пользователя
    # Для примера использую стандартные настройки
    return create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/inventory_db")


def product_information():
    """Для каждого вида садового инвентаря указать сведения о нем"""
    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT 
                p.product_name,
                pd.release_date,
                pr.provider_name,
                p.price,
                pd.sale_date,
                p.product_type,
                m.manufacturer_name
            FROM products p
            JOIN product_details pd ON p.product_id = pd.product_id
            JOIN providers pr ON p.provider_id = pr.provider_id
            JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
            ORDER BY p.product_type, p.product_name
        """)
        result = conn.execute(query)

        print("\nProduct Information:")
        print("-" * 140)
        print(
            f"{'Product Type':<20} {'Product Name':<30} {'Manufacturer':<25} {'Provider':<25} {'Price':<10} {'Release Date':<15} {'Sale Date':<15}")
        print("-" * 140)

        for row in result:
            sale_date = row[4].strftime('%Y-%m-%d') if row[4] else 'Not sold'
            print(
                f"{row[5]:<20} {row[0]:<30} {row[6]:<25} {row[2]:<25} {row[3]:<10.2f} {row[1].strftime('%Y-%m-%d'):<15} {sale_date:<15}")


def sort_by_price():
    """Получить список садового инвентаря, отсортированный по стоимости"""
    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT 
                p.product_name,
                p.price,
                p.product_type,
                m.manufacturer_name
            FROM products p
            JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
            ORDER BY p.price DESC
        """)
        result = conn.execute(query)

        print("\nProducts Sorted by Price (descending):")
        print("-" * 100)
        print(f"{'Product Name':<40} {'Type':<20} {'Manufacturer':<25} {'Price':<10}")
        print("-" * 100)

        for row in result:
            print(f"{row[0]:<40} {row[2]:<20} {row[3]:<25} {row[1]:<10.2f}")


def average_price():
    """Найти среднюю стоимость"""
    engine = get_engine()
    with engine.connect() as conn:
        # Общая статистика
        query = text("""
            SELECT 
                AVG(price) as avg_price
            FROM products
        """)
        result = conn.execute(query).fetchone()

        # Статистика по типам
        query_by_type = text("""
            SELECT 
                product_type,
                AVG(price) as avg_price,
                COUNT(*) as count
            FROM products
            GROUP BY product_type
            ORDER BY avg_price DESC
        """)
        result_by_type = conn.execute(query_by_type)

        print("\nPrice Statistics:")
        print("-" * 60)
        print(f"{'Overall Statistics':<30} {'Value':<15}")
        print("-" * 60)
        print(f"{'Average price':<30} {result[0]:<15.2f}")

        print("\nPrice Statistics by Product Type:")
        print("-" * 95)
        print(f"{'Product Type':<25} {'Average':<15} {'Count':<10}")
        print("-" * 95)

        for row in result_by_type:
            print(f"{row[0]:<25} {row[1]:<15.2f} {row[2]:<15.2f}")


def products_by_price_range():
    """Найти садовый инвентарь с ценой в заданных пределах"""
    try:
        min_price = float(input("Enter minimum price: "))
        max_price = float(input("Enter maximum price: "))
    except ValueError:
        print("Invalid price format. Please enter numeric values.")
        return

    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT 
                p.product_name,
                p.price,
                p.product_type,
                m.manufacturer_name,
                pr.provider_name
            FROM products p
            JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
            JOIN providers pr ON p.provider_id = pr.provider_id
            WHERE p.price BETWEEN :min_price AND :max_price
            ORDER BY p.price
        """)
        result = conn.execute(query, {"min_price": min_price, "max_price": max_price})

        print(f"\nProducts with price between {min_price} and {max_price}:")
        print("-" * 115)
        print(f"{'Product Name':<40} {'Type':<20} {'Manufacturer':<25} {'Provider':<25} {'Price':<10}")
        print("-" * 115)

        found = False
        for row in result:
            found = True
            print(f"{row[0]:<40} {row[2]:<20} {row[3]:<25} {row[4]:<25} {row[1]:<10.2f}")

        if not found:
            print("No products found in the specified price range.")


def products_by_manufacturer():
    """Найти весь садовый инвентарь заданного производителя"""
    manufacturer_name = input("Enter manufacturer name: ")

    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT 
                p.product_name,
                p.price,
                p.product_type,
                pd.release_date,
                pd.sale_date,
                m.manufacturer_name
            FROM products p
            JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
            JOIN product_details pd ON p.product_id = pd.product_id
            WHERE m.manufacturer_name ILIKE :manufacturer_name
            ORDER BY p.product_type, p.product_name
        """)
        result = conn.execute(query, {"manufacturer_name": f"%{manufacturer_name}%"})

        print(f"\nProducts by manufacturer '{manufacturer_name}':")
        print("-" * 120)
        print(
            f"{'Product Name':<40} {'Type':<20} {'Price':<10} {'Release Date':<15} {'Sale Date':<15} {'Manufacturer':<25}")
        print("-" * 120)

        found = False
        for row in result:
            found = True
            sale_date = row[4].strftime('%Y-%m-%d') if row[4] else 'Not sold'
            print(
                f"{row[0]:<40} {row[2]:<20} {row[1]:<10.2f} {row[3].strftime('%Y-%m-%d'):<15} {sale_date:<15} {row[5]:<25}")

        if not found:
            print(f"No products found for manufacturer '{manufacturer_name}'.")


def products_by_release_date():
    """Найти весь садовый инвентарь с заданной датой выпуска"""
    release_date_str = input("Enter release date (YYYY-MM-DD): ")

    try:
        release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return

    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT 
                p.product_name,
                p.price,
                p.product_type,
                m.manufacturer_name,
                pd.release_date
            FROM products p
            JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
            JOIN product_details pd ON p.product_id = pd.product_id
            WHERE pd.release_date = :release_date
            ORDER BY p.product_type, p.product_name
        """)
        result = conn.execute(query, {"release_date": release_date})

        print(f"\nProducts released on {release_date}:")
        print("-" * 110)
        print(f"{'Product Name':<40} {'Type':<20} {'Manufacturer':<25} {'Price':<10} {'Release Date':<15}")
        print("-" * 110)

        found = False
        for row in result:
            found = True
            print(f"{row[0]:<40} {row[2]:<20} {row[3]:<25} {row[1]:<10.2f} {row[4].strftime('%Y-%m-%d'):<15}")

        if not found:
            print(f"No products found released on {release_date}.")


def products_by_sale_date_range():
    """Найти садовый инвентарь с датой продажи в заданных пределах"""
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    end_date_str = input("Enter end date (YYYY-MM-DD): ")

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return

    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT 
                p.product_name,
                p.price,
                p.product_type,
                pd.sale_date,
                pd.customer,
                m.manufacturer_name
            FROM products p
            JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
            JOIN product_details pd ON p.product_id = pd.product_id
            WHERE pd.sale_date BETWEEN :start_date AND :end_date
            ORDER BY pd.sale_date
        """)
        result = conn.execute(query, {"start_date": start_date, "end_date": end_date})

        print(f"\nProducts sold between {start_date} and {end_date}:")
        print("-" * 130)
        print(
            f"{'Product Name':<40} {'Type':<20} {'Manufacturer':<25} {'Price':<10} {'Sale Date':<15} {'Customer':<25}")
        print("-" * 130)

        found = False
        for row in result:
            found = True
            print(
                f"{row[0]:<40} {row[2]:<20} {row[5]:<25} {row[1]:<10.2f} {row[3].strftime('%Y-%m-%d'):<15} {row[4]:<25}")

        if not found:
            print(f"No products found sold between {start_date} and {end_date}.")


def avg_price_by_sale_period():
    """Найти среднюю стоимость садового инвентаря, проданного за определенный промежуток времени"""
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    end_date_str = input("Enter end date (YYYY-MM-DD): ")

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return

    engine = get_engine()
    with engine.connect() as conn:
        # Средняя цена за период
        query_avg = text("""
            SELECT 
                AVG(p.price) as avg_price,
                COUNT(*) as total_items
            FROM products p
            JOIN product_details pd ON p.product_id = pd.product_id
            WHERE pd.sale_date BETWEEN :start_date AND :end_date
        """)
        result_avg = conn.execute(query_avg, {"start_date": start_date, "end_date": end_date}).fetchone()

        # Средняя цена по типам
        query_by_type = text("""
            SELECT 
                p.product_type,
                AVG(p.price) as avg_price,
                COUNT(*) as count
            FROM products p
            JOIN product_details pd ON p.product_id = pd.product_id
            WHERE pd.sale_date BETWEEN :start_date AND :end_date
            GROUP BY p.product_type
            ORDER BY avg_price DESC
        """)
        result_by_type = conn.execute(query_by_type, {"start_date": start_date, "end_date": end_date})

        print(f"\nAverage Price for Products Sold Between {start_date} and {end_date}:")
        print("-" * 60)
        print(f"{'Metric':<30} {'Value':<15}")
        print("-" * 60)
        if result_avg[0] is not None:
            print(f"{'Average price':<30} {result_avg[0]:<15.2f}")
            print(f"{'Total items sold':<30} {result_avg[1]:<15}")
        else:
            print("No products were sold in the specified period.")
            return

        print("\nAverage Price by Product Type:")
        print("-" * 70)
        print(f"{'Product Type':<25} {'Average Price':<20} {'Count':<10}")
        print("-" * 70)

        for row in result_by_type:
            print(f"{row[0]:<25} {row[1]:<20.2f} {row[2]:<10}")


def defective_items_by_manufacturer():
    """Найти весь садовый инвентарь с браком от заданного производителя"""
    manufacturer_name = input("Enter manufacturer name: ")

    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT 
                p.product_name,
                p.price,
                p.product_type,
                pd.release_date,
                m.manufacturer_name
            FROM products p
            JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
            JOIN product_details pd ON p.product_id = pd.product_id
            WHERE m.manufacturer_name ILIKE :manufacturer_name
            AND p.is_defective = TRUE
            ORDER BY p.product_type, p.product_name
        """)
        result = conn.execute(query, {"manufacturer_name": f"%{manufacturer_name}%"})

        print(f"\nDefective products by manufacturer '{manufacturer_name}':")
        print("-" * 110)
        print(f"{'Product Name':<40} {'Type':<20} {'Manufacturer':<25} {'Price':<10} {'Release Date':<15}")
        print("-" * 110)

        found = False
        for row in result:
            found = True
            print(f"{row[0]:<40} {row[2]:<20} {row[4]:<25} {row[1]:<10.2f} {row[3].strftime('%Y-%m-%d'):<15}")

        if not found:
            print(f"No defective products found for manufacturer '{manufacturer_name}'.")


def items_sold_to_customer_last_6_months():
    """Найти садовый инвентарь, проданный заданному клиенту за последние полгода"""
    customer_name = input("Enter customer name: ")

    # Вычисляем дату 6 месяцев назад
    today = datetime.now().date()
    six_months_ago = today - timedelta(days=180)

    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT 
                p.product_name,
                p.price,
                p.product_type,
                pd.sale_date,
                pd.sold_amount,
                m.manufacturer_name
            FROM products p
            JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
            JOIN product_details pd ON p.product_id = pd.product_id
            WHERE pd.customer ILIKE :customer_name
            AND pd.sale_date >= :six_months_ago
            ORDER BY pd.sale_date DESC
        """)
        result = conn.execute(query, {"customer_name": f"%{customer_name}%", "six_months_ago": six_months_ago})

        print(f"\nProducts sold to customer '{customer_name}' in the last 6 months (since {six_months_ago}):")
        print("-" * 140)
        print(f"{'Product Name':<40} {'Type':<20} {'Manufacturer':<25} {'Price':<10} {'Sale Date':<15} {'Amount':<10}")
        print("-" * 140)

        found = False
        for row in result:
            found = True
            print(
                f"{row[0]:<40} {row[2]:<20} {row[5]:<25} {row[1]:<10.2f} {row[3].strftime('%Y-%m-%d'):<15} {row[4]:<10}")

        if not found:
            print(f"No products found sold to customer '{customer_name}' in the last 6 months.")