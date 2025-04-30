import json

MAX_STR_LENGTH = 2000

def transform_rows(rows):
    """
    Преобразует список строк (кортежей или словарей) в список словарей с развернутыми полями OLD_VALUE и NEW_VALUE.
    
    Правила:
    - OLD_VALUE (индекс 5) и NEW_VALUE (индекс 6) должны быть строками в формате JSON.
    - Если парсинг JSON в OLD_VALUE или NEW_VALUE невозможен, в соответствующем NEW_VALUE будет записано "Error - Bad JSON".
    - Если в OLD_VALUE не строка, а что-то другое — оставляем значение как есть.
    - Обрезаем строки JSON в OLD_VALUE и NEW_VALUE до MAX_STR_LENGTH символов, если они длиннее.
    
    Аргументы:
        rows: список кортежей или список словарей
    
    Возвращает:
        Список словарей с полями:
        - Все поля из оригинала кроме OLD_VALUE и NEW_VALUE
        - FIELD (имя измененного поля)
        - OLD_VALUE (старое значение)
        - NEW_VALUE (новое значение)
    """
    results = []

    for row in rows:
        # Если это кортеж, конвертим в словарь
        if isinstance(row, tuple):
            row = {f"COL{i}": val for i, val in enumerate(row)}

        # Общие поля кроме OLD и NEW
        common_fields = {k: v for k, v in row.items() if k not in ('COL5', 'COL6')}
        old_json_str = row.get('COL5')
        new_json_str = row.get('COL6')

        try:
            old_json = json.loads(old_json_str) if isinstance(old_json_str, str) else {}
        except Exception:
            old_json = {}
        
        try:
            new_json = json.loads(new_json_str) if isinstance(new_json_str, str) else {}
        except Exception:
            new_json = "Error - Bad JSON"

        if isinstance(new_json, str) and new_json == "Error - Bad JSON":
            for key in old_json.keys():
                results.append({
                    **common_fields,
                    "FIELD": key,
                    "OLD_VALUE": old_json.get(key),
                    "NEW_VALUE": "Error - Bad JSON"
                })
            continue

        for key in set(old_json.keys()).union(new_json.keys()):
            old_value = old_json.get(key)
            new_value = new_json.get(key)

            # Обрезка больших JSON строк
            if isinstance(old_value, str) and len(old_value) > MAX_STR_LENGTH:
                old_value = old_value[:MAX_STR_LENGTH]
            if isinstance(new_value, str) and len(new_value) > MAX_STR_LENGTH:
                new_value = new_value[:MAX_STR_LENGTH]

            results.append({
                **common_fields,
                "FIELD": key,
                "OLD_VALUE": old_value,
                "NEW_VALUE": new_value,
            })
    return results