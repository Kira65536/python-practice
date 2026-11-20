def analyze_responses(responses):
    # создаём переменные для хранения статистики
    total_requests = 0
    successful_requests = []
    client_errors = []
    server_errors = []
    repeated_requests = []
    error_endpoints = []
    endpoint_stats = {}
    result = {}

    # перебираем все запросы
    for response in responses:
        total_requests += 1
        status = response["status"]
        endpoint = response["endpoint"]

        # сохраняем успешные запросы
        if 200 <= status <= 299:
            successful_requests.append(response)

        # сохраняем клиентские ошибки
        if 400 <= status <= 499:
            client_errors.append(response)

        # сохраняем серверные ошибки
        if 500 <= status <= 599:
            server_errors.append(response)

        # ищем повторные запросы
        if response["attempts"] > 1:
            repeated_requests.append(response)

        # собираем статистику по эндпоинтам
        if endpoint not in endpoint_stats:
            endpoint_stats[endpoint] = {
                "total": 0,
                "successful": 0,
                "errors": 0,
                "repeated": 0
            }

        # считаем общее количество запросов
        endpoint_stats[endpoint]["total"] += 1

        # считаем успешные запросы
        if 200 <= status <= 299:
            endpoint_stats[endpoint]["successful"] += 1

        # считаем ошибки
        if 400 <= status <= 599:
            endpoint_stats[endpoint]["errors"] += 1

        # считаем повторные запросы
        if response["attempts"] > 1:
            endpoint_stats[endpoint]["repeated"] += 1

    # ищем эндпоинты с ошибками
    for endpoint, stats in endpoint_stats.items():
        if stats["errors"] > 0:
            error_endpoints.append(endpoint)

    # собираем итоговую статистику
    result["total_requests"] = total_requests
    result["successful_requests"] = successful_requests
    result["client_errors"] = client_errors
    result["server_errors"] = server_errors
    result["repeated_requests"] = repeated_requests
    result["error_endpoints"] = error_endpoints
    result["endpoint_stats"] = endpoint_stats

    return result


# создаём тестовые данные
responses = [
    {"endpoint": "/users", "status": 200, "attempts": 1},
    {"endpoint": "/users", "status": 200, "attempts": 2},
    {"endpoint": "/users", "status": 500, "attempts": 3},
    {"endpoint": "/login", "status": 200, "attempts": 1},
    {"endpoint": "/login", "status": 401, "attempts": 2},
    {"endpoint": "/login", "status": 401, "attempts": 1},
    {"endpoint": "/products", "status": 200, "attempts": 1},
    {"endpoint": "/products", "status": 404, "attempts": 1},
    {"endpoint": "/products", "status": 500, "attempts": 2},
    {"endpoint": "/orders", "status": 201, "attempts": 1},
    {"endpoint": "/orders", "status": 201, "attempts": 1},
    {"endpoint": "/orders", "status": 503, "attempts": 4},
]


def print_api_report(data):
    # выводим общую статистику
    print("=" * 60)
    print("                  API RESPONSE STATISTICS")
    print("=" * 60)
    print(f"всего запросов:       {data['total_requests']}")
    print(f"успешных запросов:   {len(data['successful_requests'])}")
    print(f"клиентских ошибок:    {len(data['client_errors'])}")
    print(f"серверных ошибок:     {len(data['server_errors'])}")
    print(f"повторных запросов:   {len(data['repeated_requests'])}")

    # выводим эндпоинты с ошибками
    print("\n" + "=" * 60)
    print("                   ENDPOINTS WITH ERRORS")
    print("=" * 60)

    if data["error_endpoints"]:
        for endpoint in data["error_endpoints"]:
            stats = data["endpoint_stats"][endpoint]
            print(f"[ERROR] {endpoint}")
            print(f"        всего запросов: {stats['total']}")
            print(f"        успешных: {stats['successful']}")
            print(f"        ошибок: {stats['errors']}")
            print(f"        повторных: {stats['repeated']}")
    else:
        print("эндпоинтов с ошибками не обнаружено")

    # выводим статистику по всем эндпоинтам
    print("\n" + "=" * 60)
    print("                    ENDPOINT STATISTICS")
    print("=" * 60)

    for endpoint, stats in data["endpoint_stats"].items():
        print(f"[INFO] {endpoint}")
        print(f"       всего запросов: {stats['total']}")
        print(f"       успешных: {stats['successful']}")
        print(f"       ошибок: {stats['errors']}")
        print(f"       повторных: {stats['repeated']}")


# запускаем анализ и выводим отчёт
result = analyze_responses(responses)
print_api_report(result)