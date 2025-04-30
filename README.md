
# transform_rows_project

Python-модуль для преобразования результатов выборки из базы данных (fetchall) с раскруткой изменений внутри полей OLD_VALUE и NEW_VALUE.

## Как работает

- На вход подается список словарей.
- OLD_VALUE и NEW_VALUE должны быть строками, содержащими JSON-объекты.
- Если строка не является корректным JSON, будет зафиксирована ошибка ("Error - Bad JSON").
- Все остальные поля сохраняются без изменений.
- На выходе возвращается список новых строк: одна строка на каждое измененное поле.

---

## Corner-кейсы, которые обрабатываются

### 1. Корректный JSON с несколькими полями
**OLD_VALUE**: `{"status": "Новая", "priority": "низкий"}`  
**NEW_VALUE**: `{"status": "В работе", "priority": "высокий"}`  

**Результат**:
- Поле `status`: `Новая -> В работе`
- Поле `priority`: `низкий -> высокий`

---

### 2. Ошибка в JSON в OLD_VALUE

**OLD_VALUE**: `{"wrong_json": "missing_quote}` (нет закрывающей кавычки)

**NEW_VALUE**: `{"correct_json": "value"}`

**Результат**:
- Для всех полей из корректного NEW_VALUE:
  - значение в OLD_VALUE будет равно "Error - Bad JSON"
  - значение в NEW_VALUE будет подставлено из JSON

---

### 3. Ошибка в JSON в NEW_VALUE

**OLD_VALUE**: `{"field1": "old_value"}`

**NEW_VALUE**: `{"broken_json": "value}` (нет закрытия кавычки)

**Результат**:
- Для всех полей из корректного OLD_VALUE:
  - значение в OLD_VALUE будет подставлено как есть
  - значение в NEW_VALUE будет равно "Error - Bad JSON"

---

### 4. Ошибка в JSON в обеих строках

**OLD_VALUE**: `{"bad": value}` (нет кавычек вокруг value)

**NEW_VALUE**: `{"also_bad": }` (нет значения)

**Результат**:
- Поле "unknown" будет возвращено с ошибками:
  - OLD_VALUE = "Error - Bad JSON"
  - NEW_VALUE = "Error - Bad JSON"

---

### 5. Когда OLD_VALUE и NEW_VALUE одинаковые

**OLD_VALUE**: `{"status": "Новая"}`

**NEW_VALUE**: `{"status": "Новая"}`

**Результат**:
- Всё равно будет возвращена строка с одинаковыми значениями ("Новая", "Новая").

---

## Ограничения
- Строки с JSON в OLD_VALUE и NEW_VALUE автоматически обрезаются до 2000 символов.
- Вложенные JSON-объекты остаются как строки, без рекурсивной обработки.

---

## Пример использования

```python
from transform_rows import transform_rows

# Ваши входные данные (например, после fetchall)
input_rows = [
    {
        "ID": 42,
        "DATE": "2025-04-01",
        "COL3": "extra1",
        "COL4": "extra2",
        "COL5": "extra3",
        "OLD_VALUE": '{"status": "Новая", "priority": "низкий"}',
        "NEW_VALUE": '{"status": "В работе", "priority": "высокий"}'
    },
    ...
]

result = transform_rows(input_rows)

for row in result:
    print(row)
```

---

## Требования

- Python 3.6+
- Нет сторонних зависимостей (только стандартная библиотека)

---

Проект готов к интеграции в ETL пайплайны DWH.

