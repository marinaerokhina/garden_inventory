from datetime import datetime, timedelta
import random as rand

import psycopg2
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, \
    String, Float, Boolean, Date, ForeignKey, inspect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.orm import declarative_base

"""
    Cоздает базу данных, если таковая не существует
    @db_name: имя базы данных, котору создает/подключается
    @user: имя пользователя базы данных
    @password: пароль пользователя
"""


def create_db_if_not_exist(db_name, user='postgres', password='admin', host='localhost', port='5432'):
    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/postgres"
    engine = create_engine(
        url=db_url,
        echo=False
    )
    exists = False
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT EXISTS(SELECT FROM pg_database WHERE datname = '{db_name}')"))
        exists = result.scalar()
    if not exists:
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(f'CREATE DATABASE "{db_name}"')
        cursor.close()
        conn.close()
        print("Database created")
    else:
        print("Database already exists")


def create_tables_if_not_exist(engine):
    """Создает таблицы, если они не существуют"""
    Base = declarative_base()

    class Country(Base):
        __tablename__ = 'countries'
        country_id = Column(Integer, primary_key=True)
        country_name = Column(String(100), nullable=False, unique=True)

    class Manufacturer(Base):
        __tablename__ = 'manufacturers'
        manufacturer_id = Column(Integer, primary_key=True)
        manufacturer_name = Column(String(100), nullable=False)
        country_id = Column(Integer, ForeignKey('countries.country_id'), nullable=False)

    class Provider(Base):
        __tablename__ = 'providers'
        provider_id = Column(Integer, primary_key=True)
        provider_name = Column(String(100), nullable=False)
        country_id = Column(Integer, ForeignKey('countries.country_id'), nullable=False)

    class Product(Base):
        __tablename__ = 'products'
        product_id = Column(Integer, primary_key=True)
        provider_id = Column(Integer, ForeignKey('providers.provider_id'), nullable=False)
        manufacturer_id = Column(Integer, ForeignKey('manufacturers.manufacturer_id'), nullable=False)
        product_name = Column(String(100), nullable=False)
        price = Column(Float, nullable=False)
        is_defective = Column(Boolean, default=False)
        product_type = Column(String(50))

    class ProductDetail(Base):
        __tablename__ = 'product_details'
        details_id = Column(Integer, primary_key=True)
        product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
        release_date = Column(Date)
        sale_date = Column(Date)
        sold_amount = Column(Integer)
        customer = Column(String(100))

    # Проверяем существование таблиц
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    required_tables = ['countries', 'manufacturers', 'providers', 'products', 'product_details']
    tables_exist = all(table in existing_tables for table in required_tables)

    if not tables_exist:
        print("Creating tables...")
        Base.metadata.create_all(engine)
        print("Tables created successfully")
        return False
    else:
        print("All tables already exist")
        return True


def fill_database_with_test_data(engine):
    """Заполняет базу данных тестовыми данными"""
    print("Populating database with initial data...")

    with engine.connect() as conn:
        # Добавление стран
        countries = [
            "USA", "China", "Germany", "Japan", "UK", "France", "Italy",
            "Canada", "Australia", "Brazil", "Russia", "India", "Mexico",
            "South Korea", "Spain", "Netherlands", "Sweden", "Poland", "Turkey", "Switzerland"
        ]

        for country in countries:
            conn.execute(
                text("INSERT INTO countries (country_name) VALUES (:name)"),
                {"name": country}
            )

        # Получение ID стран
        result = conn.execute(text("SELECT country_id, country_name FROM countries"))
        country_data = result.fetchall()
        country_dict = {name: id for id, name in country_data}

        # Добавление производителей
        manufacturers = [
            {"name": "GreenThumb Tools", "country": "USA"},
            {"name": "GardenPro Manufacturing", "country": "Germany"},
            {"name": "LawnMaster Industries", "country": "UK"},
            {"name": "EarthMover Tools", "country": "Canada"},
            {"name": "NatureCare Equipment", "country": "Australia"},
            {"name": "SoilMaster Tools", "country": "France"},
            {"name": "GardenGear International", "country": "Italy"},
            {"name": "PlantGuard Manufacturing", "country": "Japan"},
            {"name": "EcoGrow Tools", "country": "Netherlands"},
            {"name": "GreenLife Equipment", "country": "Sweden"},
            {"name": "OutdoorMaster", "country": "USA"},
            {"name": "GardenElite", "country": "Germany"},
            {"name": "LawnCraft", "country": "Canada"},
            {"name": "BloomTools", "country": "Australia"},
            {"name": "RootMaster", "country": "France"},
            {"name": "NaturePro", "country": "Italy"},
            {"name": "GreenScape Tools", "country": "Japan"},
            {"name": "GardenArtisan", "country": "Spain"},
            {"name": "EarthWorks", "country": "Brazil"},
            {"name": "BotanicTools", "country": "Switzerland"}
        ]

        for m in manufacturers:
            country_id = country_dict[m["country"]]
            conn.execute(
                text("INSERT INTO manufacturers (manufacturer_name, country_id) VALUES (:name, :country_id)"),
                {"name": m["name"], "country_id": country_id}
            )

        # Получение ID производителей
        result = conn.execute(text("SELECT manufacturer_id, manufacturer_name FROM manufacturers"))
        manufacturer_data = result.fetchall()
        manufacturer_dict = {name: id for id, name in manufacturer_data}

        # Добавление поставщиков
        providers = [
            {"name": "GardenSupplies Inc", "country": "USA"},
            {"name": "EuroGarden Distributors", "country": "Germany"},
            {"name": "UK Garden Wholesale", "country": "UK"},
            {"name": "NorthStar Garden Supply", "country": "Canada"},
            {"name": "Aussie Garden Providers", "country": "Australia"},
            {"name": "French Garden Network", "country": "France"},
            {"name": "Italian Garden Solutions", "country": "Italy"},
            {"name": "Tokyo Garden Supplies", "country": "Japan"},
            {"name": "Dutch Garden Distributors", "country": "Netherlands"},
            {"name": "Scandinavian Garden Supply", "country": "Sweden"},
            {"name": "Global Garden Partners", "country": "USA"},
            {"name": "Continental Garden Source", "country": "Germany"},
            {"name": "British Garden Merchants", "country": "UK"},
            {"name": "Canadian Garden Network", "country": "Canada"},
            {"name": "Pacific Garden Alliance", "country": "Australia"},
            {"name": "Mediterranean Garden Supply", "country": "France"},
            {"name": "Alpine Garden Distributors", "country": "Switzerland"},
            {"name": "Iberian Garden Partners", "country": "Spain"},
            {"name": "Asian Garden Imports", "country": "China"},
            {"name": "Eastern European Garden Supply", "country": "Poland"}
        ]

        for p in providers:
            country_id = country_dict[p["country"]]
            conn.execute(
                text("INSERT INTO providers (provider_name, country_id) VALUES (:name, :country_id)"),
                {"name": p["name"], "country_id": country_id}
            )

        # Получение ID поставщиков
        result = conn.execute(text("SELECT provider_id, provider_name FROM providers"))
        provider_data = result.fetchall()
        provider_dict = {name: id for id, name in provider_data}

        # Добавление продуктов
        product_types = [
            'Lawn Mower', 'Shovel', 'Rake', 'Hoe', 'Pruning Shears',
            'Garden Fork', 'Wheelbarrow', 'Garden Hose', 'Sprinkler',
            'Gloves', 'Trowel', 'Hand Pruners', 'Hedge Trimmer',
            'Leaf Blower', 'Garden Saw', 'Watering Can', 'Secateurs',
            'Garden Scissors', 'Weeder', 'Spade'
        ]

        product_names = {
            'Lawn Mower': ['Turbine 3000', 'GrassMaster Pro', 'LawnWhisper X5', 'EcoCut 200', 'TurboMow 9000'],
            'Shovel': ['DigMaster Pro', 'EarthMover 500', 'GardenForce Shovel', 'ProDigger Deluxe', 'SoilMaster X'],
            'Rake': ['LeafCollector Pro', 'GardenGroom Deluxe', 'LawnSweeper 3000', 'NatureRake Premium',
                     'EcoSweep Master'],
            'Hoe': ['WeedDestroyer Pro', 'SoilAerator Deluxe', 'GardenMaster Hoe', 'RootRemover X',
                    'EarthCultivator Pro'],
            'Pruning Shears': ['BranchCutter Pro', 'PrecisionPruner Deluxe', 'HedgeMaster 2000', 'GardenSnip Elite',
                               'TreeTrim Pro'],
            'Garden Fork': ['SoilTurner Pro', 'AeratorMaster', 'EarthPiercer Deluxe', 'RootLifter X',
                            'GardenCultivator Pro'],
            'Wheelbarrow': ['LoadMaster 200', 'GardenHauler Pro', 'EarthMover X5', 'YardCart Deluxe',
                            'SoilTransporter Pro'],
            'Garden Hose': ['WaterFlow 500', 'GardenSpray Pro', 'FlexiHose Deluxe', 'AquaMaster X', 'HoseMaster 3000'],
            'Sprinkler': ['LawnMister Pro', 'WaterDistributor Deluxe', 'GardenSprayer X', 'AutoIrrigator Pro',
                          'EcoWater 2000'],
            'Gloves': ['GripMaster Pro', 'ThornProof Deluxe', 'GardenGuard X', 'ComfortGrip Pro', 'DuraGrip Elite'],
            'Trowel': ['SoilScooper Pro', 'PlantMaster Deluxe', 'GardenDigger X', 'RootExtractor Pro',
                       'MiniScoop Elite'],
            'Hand Pruners': ['PrecisionCutter Pro', 'BranchSnip Deluxe', 'GardenShear X', 'HedgeTrimmer Pro',
                             'BudPruner Elite'],
            'Hedge Trimmer': ['HedgeMaster 3000', 'BushShaper Pro', 'GreenSculptor Deluxe', 'HedgeWizard X',
                              'TrimMaster Elite'],
            'Leaf Blower': ['WindMaster Pro', 'LeafVac 2000', 'StormBlower Deluxe', 'GardenHurricane X',
                            'AirSweeper Pro'],
            'Garden Saw': ['BranchCutter Pro', 'TimberMaster Deluxe', 'WoodRipper X', 'TreeSaw Pro',
                           'PruningSaw Elite'],
            'Watering Can': ['WaterMaster Pro', 'GardenPour Deluxe', 'AquaPour X', 'RainMaker Pro',
                             'PlantWaterer Elite'],
            'Secateurs': ['PrecisionCut Pro', 'BudSnip Deluxe', 'FlowerTrimmer X', 'GardenShear Pro',
                          'BranchCutter Elite'],
            'Garden Scissors': ['FlowerSnip Pro', 'HerbCutter Deluxe', 'PlantTrimmer X', 'GardenSnip Pro',
                                'BudShear Elite'],
            'Weeder': ['RootPuller Pro', 'WeedDestroyer Deluxe', 'SoilCleaner X', 'GardenExtractor Pro',
                       'PlantGuard Elite'],
            'Spade': ['EarthDigger Pro', 'SoilMover Deluxe', 'GardenSpader X', 'TrenchMaster Pro', 'DigMaster Elite']
        }

        # Получение всех ID для случайного выбора
        manufacturer_ids = list(manufacturer_dict.values())
        provider_ids = list(provider_dict.values())

        # Добавление 70 продуктов
        for i in range(1, 71):
            ptype = rand.choice(product_types)
            pname = rand.choice(product_names[ptype])
            price = round(rand.uniform(15.0, 850.0), 2)
            is_defective = rand.random() < 0.05  # 5% шанс брака
            manufacturer_id = rand.choice(manufacturer_ids)
            provider_id = rand.choice(provider_ids)

            conn.execute(text("""
                INSERT INTO products (provider_id, manufacturer_id, product_name, price, is_defective, product_type)
                VALUES (:provider_id, :manufacturer_id, :product_name, :price, :is_defective, :product_type)
            """), {
                "provider_id": provider_id,
                "manufacturer_id": manufacturer_id,
                "product_name": pname,
                "price": price,
                "is_defective": is_defective,
                "product_type": ptype
            })

        # Получение ID продуктов
        result = conn.execute(text("SELECT product_id FROM products"))
        product_ids = [row[0] for row in result.fetchall()]

        # Добавление деталей продуктов
        # Генерация случайных имен клиентов
        first_names = ['John', 'Michael', 'Robert', 'David', 'James', 'William', 'Richard', 'Joseph', 'Thomas',
                       'Charles',
                       'Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Mia', 'Charlotte', 'Amelia', 'Harper', 'Evelyn']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez',
                      'Wilson',
                      'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia',
                      'Martinez']

        # Текущая дата для генерации дат выпуска и продажи
        today = datetime.now().date()

        # Добавление 70 деталей продуктов
        for i in range(1, 71):
            product_id = product_ids[i - 1]
            # Дата выпуска: от 1 года до 1 месяца назад
            release_days_ago = rand.randint(30, 365)
            release_date = today - timedelta(days=release_days_ago)

            # Дата продажи: от 1 месяца назад до 1 месяца вперед (None если не продан)
            sale_date = None
            sold_amount = None
            customer = None

            # 75% вероятность, что товар был продан
            if rand.random() < 0.75:
                sale_days_offset = rand.randint(-30, 30)
                sale_date = today + timedelta(days=sale_days_offset)
                # Если дата продажи раньше даты выпуска, корректируем
                if sale_date < release_date:
                    sale_date = release_date + timedelta(days=rand.randint(1, 30))

                sold_amount = rand.randint(1, 10)
                customer = f"{rand.choice(first_names)} {rand.choice(last_names)}"

            conn.execute(text("""
                INSERT INTO product_details (product_id, release_date, sale_date, sold_amount, customer)
                VALUES (:product_id, :release_date, :sale_date, :sold_amount, :customer)
            """), {
                "product_id": product_id,
                "release_date": release_date,
                "sale_date": sale_date,
                "sold_amount": sold_amount,
                "customer": customer
            })

        conn.commit()
        print("Database populated successfully with test data")


def setup_database(db_name, user='postgres', password='admin', host='localhost', port='5432'):
    """Полная настройка базы данных: создание БД, таблиц и заполнение данными"""
    # Создаем базу данных, если не существует
    db_exists = create_db_if_not_exist(db_name, user, password, host, port)

    # Подключаемся к базе данных
    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(url=db_url, echo=False)

    # Создаем таблицы, если не существуют
    tables_exist = create_tables_if_not_exist(engine)

    # Заполняем данными, если таблицы были созданы
    if not tables_exist:
        fill_database_with_test_data(engine)

    return engine
