def analyze_users(users):
    # создаём переменные для хранения статистики
    total_users = 0
    total_orders = 0
    total_revenue = 0
    user_revenue = {}
    city_revenue = {}
    category_revenue = {}
    top_user = []
    result = {}

    # перебираем пользователей
    for user in users:
        total_users += 1
        usere = user["name"]
        cityy = user["city"]

        # перебираем заказы каждого пользователя
        for order in user["orders"]:
            total_orders += 1
            total_revenue += order["price"]

            # считаем выручку пользователей
            if usere not in user_revenue:
                user_revenue[usere] = 0
            user_revenue[usere] += order["price"]

            # считаем выручку по городам
            if cityy not in city_revenue:
                city_revenue[cityy] = 0
            city_revenue[cityy] += order["price"]

            # считаем выручку по категориям
            category = order["category"]
            if category not in category_revenue:
                category_revenue[category] = 0
            category_revenue[category] += order["price"]

    # определяем пользователя с наибольшими расходами
    top_user = max(user_revenue, key=lambda user: user_revenue[user])

    # собираем результаты
    result["total_users"] = total_users
    result["total_orders"] = total_orders
    result["total_revenue"] = total_revenue
    result["user_revenue"] = user_revenue
    result["city_revenue"] = city_revenue
    result["category_revenue"] = category_revenue
    result["top_user"] = top_user

    return result


# создаём тестовые данные
users = [
    {
        "name": "Kira",
        "city": "Moscow",
        "orders": [
            {"product": "Laptop", "category": "Electronics", "price": 80000},
            {"product": "Phone", "category": "Electronics", "price": 30000},
            {"product": "T-shirt", "category": "Clothes", "price": 3000}
        ]
    },
    {
        "name": "Alex",
        "city": "Kazan",
        "orders": [
            {"product": "Laptop", "category": "Electronics", "price": 90000},
            {"product": "Jeans", "category": "Clothes", "price": 5000}
        ]
    },
    {
        "name": "Masha",
        "city": "Moscow",
        "orders": [
            {"product": "Book", "category": "Books", "price": 2000},
            {"product": "Phone", "category": "Electronics", "price": 25000}
        ]
    },
    {
        "name": "Oleg",
        "city": "Kazan",
        "orders": [
            {"product": "Book", "category": "Books", "price": 1500},
            {"product": "T-shirt", "category": "Clothes", "price": 2500}
        ]
    }
]

# запускаем анализ
data = analyze_users(users)

# выводим общий отчёт
print("\n" + "=" * 52)
print("          АНАЛИТИКА ИНТЕРНЕТ-МАГАЗИНА")
print("=" * 52)

print(f"\nВсего пользователей: {data['total_users']}")
print(f"Всего заказов:       {data['total_orders']}")
print(f"Общая выручка:       {data['total_revenue']:,} ₽".replace(",", " "))

print("\n" + "-" * 52)
print("ПОКУПКИ ПОЛЬЗОВАТЕЛЕЙ")
print("-" * 52)

for name, revenue in data["user_revenue"].items():
    print(f"{name:<18} {revenue:>15,} ₽".replace(",", " "))

print("\n" + "-" * 52)
print("ВЫРУЧКА ПО ГОРОДАМ")
print("-" * 52)

for city, revenue in data["city_revenue"].items():
    print(f"{city:<18} {revenue:>15,} ₽".replace(",", " "))

print("\n" + "-" * 52)
print("ВЫРУЧКА ПО КАТЕГОРИЯМ")
print("-" * 52)

for category, revenue in data["category_revenue"].items():
    print(f"{category:<18} {revenue:>15,} ₽".replace(",", " "))

print("\n" + "=" * 52)
print(f"ЛУЧШИЙ ПОКУПАТЕЛЬ: {data['top_user']}")
print(f"ПОТРАТИЛ: {data['user_revenue'][data['top_user']]:,} ₽".replace(",", " "))
print("=" * 52)