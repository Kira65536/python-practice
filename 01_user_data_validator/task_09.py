from pprint import pprint

def validate_users(users):
    # создаём списки и словари для результатов
    valid_users = []
    invalid_users = []
    errors = {}
    result = {}

    # перебираем пользователей и присваиваем каждому индекс
    for i, user in enumerate(users):
        user_errors = []

        # проверяем тип данных пользователя
        if not isinstance(user, dict):
            invalid_users.append(user)
            errors[i] = ["User data must be a dictionary"]
            continue

        # проверяем username
        username = user.get("username", "")
        if not isinstance(username, str) or not username.strip():
            user_errors.append("Username is required")

        # проверяем email
        email = user.get("email", "")
        if not isinstance(email, str) or "@" not in email or "." not in email.split("@")[-1]:
            user_errors.append("Invalid email")

        # проверяем возраст
        try:
            age = user["age"]

            # проверяем тип и значение возраста
            if isinstance(age, bool) or not isinstance(age, int):
                user_errors.append("Age must be an integer")
            elif age < 18:
                user_errors.append("Age must be at least 18")

        # проверяем наличие возраста
        except KeyError:
            user_errors.append("Age is required")

        # распределяем пользователей по результатам проверки
        if user_errors:
            invalid_users.append(user)
            errors[i] = user_errors
        else:
            valid_users.append(user)

    # собираем итоговый результат
    result["valid_users"] = valid_users
    result["invalid_users"] = invalid_users
    result["errors"] = errors

    return result


# создаём тестовые данные
users = [
    {"username": "Kira", "email": "kira@mail.com", "age": 20},
    {"username": "", "email": "alexmail.com", "age": 17},
    {"username": "Masha", "email": "masha@mail.com", "age": 25},
    {"username": "Oleg", "email": "", "age": 22},
    {"username": "Anna", "email": "anna@mail.com", "age": -5},
    {"username": "Max", "email": "max@mail.com", "age": 16},
    {"username": "Dima", "email": "dima@mail.com", "age": 30}
]

# запускаем проверку и выводим результат
result = validate_users(users)
pprint(result, sort_dicts=False)