def analyze_responses(responses):
    # создаём переменные для хранения статистики
    total_requests = 0
    failed_requests = []
    unauthorized_requests = []
    forbidden_requests = []
    ip_stats = {}
    suspicious_ips = []
    attacked_endpoints = []
    endpoint_stats = {}
    result = {}

    # перебираем все запросы
    for response in responses:
        total_requests += 1

        # сохраняем неуспешные запросы
        if 400 <= response["status"] <= 599:
            failed_requests.append(response)

        # сохраняем запросы с кодами 401 и 403
        if response["status"] == 401:
            unauthorized_requests.append(response)
        if response["status"] == 403:
            forbidden_requests.append(response)

        # собираем статистику по ip
        if response["ip"]:
            ip = response["ip"]

            # создаём статистику для нового ip
            if ip not in ip_stats:
                ip_stats[ip] = {
                    "total": 0,
                    "unauthorized": 0,
                    "forbidden": 0,
                }

            # считаем запросы и ошибки ip
            ip_stats[ip]["total"] += 1
            if response["status"] == 401:
                ip_stats[ip]["unauthorized"] += 1
            if response["status"] == 403:
                ip_stats[ip]["forbidden"] += 1

        # собираем статистику по эндпоинтам
        if response["endpoint"]:
            endpoint = response["endpoint"]

            # создаём статистику для нового эндпоинта
            if endpoint not in endpoint_stats:
                endpoint_stats[endpoint] = {
                    "total": 0,
                    "errors": 0
                }

            # считаем запросы и ошибки эндпоинта
            endpoint_stats[endpoint]["total"] += 1
            if 400 <= response["status"] <= 599:
                endpoint_stats[endpoint]["errors"] += 1

    # ищем подозрительные ip
    for ip, stats in ip_stats.items():
        if stats["unauthorized"] >= 3 or stats["forbidden"] >= 3:
            suspicious_ips.append(ip)

    # ищем атакуемые эндпоинты
    for endpoint, stats in endpoint_stats.items():
        if stats["errors"] >= 3:
            attacked_endpoints.append(endpoint)

    # собираем итоговую статистику
    result["total_requests"] = total_requests
    result["failed_requests"] = failed_requests
    result["unauthorized_requests"] = unauthorized_requests
    result["forbidden_requests"] = forbidden_requests
    result["ip_stats"] = ip_stats
    result["endpoint_stats"] = endpoint_stats
    result["suspicious_ips"] = suspicious_ips
    result["attacked_endpoints"] = attacked_endpoints

    return result


# создаём тестовые запросы
responses = [
    {"ip": "192.168.1.10", "endpoint": "/login", "status": 401, "method": "POST"},
    {"ip": "192.168.1.10", "endpoint": "/login", "status": 401, "method": "POST"},
    {"ip": "192.168.1.10", "endpoint": "/login", "status": 401, "method": "POST"},
    {"ip": "192.168.1.10", "endpoint": "/login", "status": 200, "method": "POST"},
    {"ip": "192.168.1.15", "endpoint": "/users", "status": 200, "method": "GET"},
    {"ip": "192.168.1.15", "endpoint": "/admin", "status": 403, "method": "GET"},
    {"ip": "10.0.0.5", "endpoint": "/admin", "status": 403, "method": "GET"},
    {"ip": "10.0.0.5", "endpoint": "/admin", "status": 403, "method": "GET"},
    {"ip": "10.0.0.5", "endpoint": "/admin", "status": 403, "method": "GET"},
    {"ip": "10.0.0.5", "endpoint": "/admin", "status": 200, "method": "GET"},
    {"ip": "172.16.0.3", "endpoint": "/products", "status": 200, "method": "GET"},
    {"ip": "172.16.0.3", "endpoint": "/products", "status": 200, "method": "GET"},
    {"ip": "172.16.0.3", "endpoint": "/orders", "status": 500, "method": "POST"},
    {"ip": "172.16.0.3", "endpoint": "/orders", "status": 500, "method": "POST"},
]


def print_security_report(data):
    # выводим общую статистику
    print("=" * 60)
    print("                     ОБЩАЯ СТАТИСТИКА")
    print("=" * 60)
    print(f"Всего запросов:       {data['total_requests']}")
    print(f"Ошибок (4xx/5xx):  {len(data['failed_requests'])}")
    print(f"401 Unauthorized:     {len(data['unauthorized_requests'])}")
    print(f"403 Forbidden:       {len(data['forbidden_requests'])}")

    # выводим подозрительные ip
    print("\n" + "=" * 60)
    print("                 ПОДОЗРИТЕЛЬНЫЕ IP-АДРЕСА")
    print("=" * 60)

    if data["suspicious_ips"]:
        for ip in data["suspicious_ips"]:
            stats = data["ip_stats"][ip]
            print(f"[ALERT] {ip}")
            print(f"        Всего запросов: {stats['total']}")
            print(f"        401: {stats['unauthorized']}")
            print(f"        403: {stats['forbidden']}")
    else:
        print("подозрительных ip не обнаружено")

    # выводим атакуемые эндпоинты
    print("\n" + "=" * 60)
    print("                   АТАКУЕМЫЕ ЭНДПОИНТЫ")
    print("=" * 60)

    if data["attacked_endpoints"]:
        for endpoint in data["attacked_endpoints"]:
            stats = data["endpoint_stats"][endpoint]
            print(f"[WARNING] {endpoint}")
            print(f"         Всего запросов: {stats['total']}")
            print(f"         Ошибок: {stats['errors']}")
    else:
        print("подозрительных endpoint не обнаружено")


# запускаем анализ и выводим отчёт
result = analyze_responses(responses)
print_security_report(result)