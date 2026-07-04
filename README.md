# Garden Inventory — Система учёта садового инвентаря

Приложение для управления базой данных садового инвентаря с использованием Python, SQLAlchemy и PostgreSQL. Реализовано на основе курсовой работы по базам данных.

## 🎯 Цель проекта

Разработать систему для учёта садового инвентаря с возможностью:
- Хранения информации о товарах, производителях и поставщиках
- Выполнения сложных SQL-запросов через SQLAlchemy
- Анализа данных: статистика, фильтрация, поиск
- Автоматического создания и заполнения базы данных тестовыми данными

## 🏗 Архитектура проекта

```
garden_inventory/
├── src/
│   ├── db_setup.py      # Создание БД, таблиц и заполнение данными
│   ├── db_func.py       # Функции для работы с БД (запросы)
│   └── main.py          # Консольное меню
├── КР-Ерохина.pdf       # Документация оригинальной курсовой работы
└── README.md
```

## 🗄 Структура базы данных

Схема БД включает 5 связанных таблиц:

```
countries
├── country_id (PK)
└── country_name

manufacturers
├── manufacturer_id (PK)
├── manufacturer_name
└── country_id (FK → countries)

providers
├── provider_id (PK)
├── provider_name
└── country_id (FK → countries)

products
├── product_id (PK)
├── provider_id (FK → providers)
├── manufacturer_id (FK → manufacturers)
├── product_name
├── price
├── is_defective
└── product_type

product_details
├── details_id (PK)
├── product_id (FK → products)
├── release_date
├── sale_date
├── sold_amount
└── customer
```

**Связи:**
- Одна страна → много производителей и поставщиков
- Один производитель/поставщик → много продуктов
- Один продукт → одна запись деталей

## 🛠 Технологии

- **Python 3.x** — основной язык
- **SQLAlchemy 2.x** — ORM для работы с БД
- **PostgreSQL** — реляционная база данных
- **psycopg2** — драйвер для PostgreSQL
- **SQL** — сложные запросы с JOIN, GROUP BY, агрегатными функциями

## 📋 Функциональность

### **1. Управление базой данных**
- Автоматическое создание БД при первом запуске
- Создание всех таблиц с проверкой существования
- Генерация тестовых данных:
  - 20 стран
  - 20 производителей
  - 20 поставщиков
  - 70 продуктов с случайными характеристиками
  - Детали продуктов с датами выпуска и продажи

### **2. Запросы к базе данных**

#### **Информация о продуктах**
```python
product_information()
```
Выводит полную информацию о каждом виде инвентаря: название, дата выпуска, поставщик, цена, дата продажи, тип, производитель.

#### **Сортировка по цене**
```python
sort_by_price()
```
Список всего инвентаря, отсортированный по убыванию цены.

#### **Статистика по ценам**
```python
average_price()
```
- Общая средняя стоимость всех товаров
- Средняя стоимость по каждому типу товара
- Количество товаров каждого типа

#### **Поиск по диапазону цен**
```python
products_by_price_range()
```
Находит все товары с ценой в заданном диапазоне (интерактивный ввод).

#### **Поиск по производителю**
```python
products_by_manufacturer()
```
Находит весь инвентарь заданного производителя (поддержка частичного совпадения через ILIKE).

#### **Поиск по дате выпуска**
```python
products_by_release_date()
```
Находит все товары с указанной датой выпуска.

#### **Поиск по диапазону дат продажи**
```python
products_by_sale_date_range()
```
Находит товары, проданные в заданный период времени.

#### **Средняя цена за период**
```python
avg_price_by_sale_period()
```
- Средняя стоимость товаров, проданных за указанный период
- Статистика по типам товаров за этот период
- Общее количество проданных товаров

#### **Поиск бракованных товаров**
```python
defective_items_by_manufacturer()
```
Находит все бракованные товары заданного производителя.

#### **История покупок клиента**
```python
items_sold_to_customer_last_6_months()
```
Находит все товары, проданные указанному клиенту за последние 6 месяцев.

## 🚀 Запуск

### **Требования:**
- Python 3.8+
- PostgreSQL 12+
- Установленный PostgreSQL сервер

### **Установка зависимостей:**
```bash
pip install sqlalchemy psycopg2-binary
```

### **Настройка PostgreSQL:**
Убедитесь, что PostgreSQL запущен и доступен с параметрами:
- Host: `localhost`
- Port: `5432`
- User: `postgres`
- Password: `admin` (или измените в `main.py`)

### **Запуск приложения:**

При первом запуске приложение автоматически:
1. Создаст базу данных `inventory_db`
2. Создаст все необходимые таблицы
3. Заполнит базу тестовыми данными

### **Использование:**
После запуска выберите номер функции из меню (1-10) и следуйте инструкциям.

## 💡 Ключевые особенности реализации

### **1. Автоматическая настройка БД**
```python
def setup_database(db_name, user, password, host, port):
    # Создаёт БД если не существует
    db_exists = create_db_if_not_exist(db_name, user, password, host, port)
    
    # Создаёт таблицы если не существуют
    tables_exist = create_tables_if_not_exist(engine)
    
    # Заполняет данными если таблицы были созданы
    if not tables_exist:
        fill_database_with_test_data(engine)
    
    return engine
```

### **2. Декларативное описание моделей**
```python
class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey('providers.provider_id'))
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.manufacturer_id'))
    product_name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    is_defective = Column(Boolean, default=False)
    product_type = Column(String(50))
```

### **3. Сложные SQL-запросы с JOIN**
```python
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
```

### **4. Агрегатные функции и группировка**
```python
query_by_type = text("""
    SELECT
        product_type,
        AVG(price) as avg_price,
        COUNT(*) as count
    FROM products
    GROUP BY product_type
    ORDER BY avg_price DESC
""")
```

### **5. Параметризованные запросы**
```python
result = conn.execute(query, {
    "min_price": min_price,
    "max_price": max_price
})
```

### **6. Обработка дат**
```python
# Вычисление даты 6 месяцев назад
today = datetime.now().date()
six_months_ago = today - timedelta(days=180)

# Форматирование дат для вывода
sale_date = row[4].strftime('%Y-%m-%d') if row[4] else 'Not sold'
```

### **7. Генерация тестовых данных**
```python
# 70 продуктов с случайными характеристиками
for i in range(1, 71):
    ptype = rand.choice(product_types)
    pname = rand.choice(product_names[ptype])
    price = round(rand.uniform(15.0, 850.0), 2)
    is_defective = rand.random() < 0.05  # 5% шанс брака
```

## 📊 Примеры вывода

### **Информация о продуктах:**
```
Product Information:
------------------------------------------------------------------------------------------------------------------------------------------------
Product Type          Product Name                  Manufacturer               Provider                   Price     Release Date   Sale Date      
------------------------------------------------------------------------------------------------------------------------------------------------
Garden Fork           SoilTurner Pro                GardenPro Manufacturing    EuroGarden Distributors    456.78    2025-03-15     2025-06-20     
Garden Hose           WaterFlow 500                 GreenThumb Tools           GardenSupplies Inc         234.50    2025-01-10     2025-04-15     
Lawn Mower            Turbine 3000                  LawnMaster Industries      UK Garden Wholesale        789.99    2024-12-01     Not sold       
```

### **Статистика по ценам:**
```
Price Statistics:
------------------------------------------------------------
Metric                          Value          
------------------------------------------------------------
Average price                   423.56         

Price Statistics by Product Type:
-----------------------------------------------------------------------------------------------
Product Type               Average            Count      
-----------------------------------------------------------------------------------------------
Lawn Mower                 678.90             5         
Garden Hose                512.34             4         
Wheelbarrow                489.12             3         
```

## 📚 Чему научилась

✅ Проектирование реляционных баз данных  
✅ Нормализация таблиц (1NF, 2NF, 3NF)  
✅ Работа с SQLAlchemy ORM  
✅ Создание сложных SQL-запросов с JOIN  
✅ Агрегатные функции: AVG, COUNT, SUM  
✅ Группировка данных: GROUP BY, ORDER BY  
✅ Параметризованные запросы для безопасности  
✅ Работа с датами в SQL и Python  
✅ Автоматизация создания и заполнения БД  
✅ Обработка ошибок и валидация ввода  
✅ Консольный интерфейс пользователя  

## 🔮 Возможные улучшения

- [ ] Графический интерфейс (Tkinter/PyQt)
- [ ] REST API для веб-доступа
- [ ] Экспорт данных в CSV/Excel
- [ ] Импорт данных из файлов
- [ ] Система авторизации пользователей
- [ ] Логирование всех операций
- [ ] Unit-тесты (pytest)
- [ ] Docker-контейнеризация
- [ ] Пагинация для больших выборок
- [ ] Кэширование частых запросов

## 📝 Примечание

Проект разработан на основе курсовой работы по предмету "Базы данных". Документация оригинальной курсовой работы доступна в файле `КР-Ерохина.pdf`. Огригинальная 
КР выполнялась на PostgreSQL.

---

**Автор:** Марина Ерохина  
