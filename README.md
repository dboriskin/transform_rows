# Transform Rows Project

## Описание

Этот модуль предназначен для преобразования строк из базы данных, в которых OLD_VALUE и NEW_VALUE хранятся в формате JSON.

## Как работает

- Принимает список строк (кортежей) с данными.
- OLD_VALUE и NEW_VALUE ожидаются в полях с индексами 5 и 6.
- Если JSON некорректный в NEW_VALUE, вместо данных будет записано `"Error - Bad JSON"`.
- Строки JSON в OLD_VALUE и NEW_VALUE обрезаются до 690 символов.
- Все остальные поля передаются без изменений.
- Возвращается список словарей.

## Corner Cases

| Сценарий | Что будет |
|:---|:---|
| OLD_VALUE или NEW_VALUE = None | Пропускается или обрабатывается как пустой |
| Неверный JSON в NEW_VALUE | Записывается "Error - Bad JSON" |
| Длинные строки JSON | Обрезаются до 690 символов |

## Пример использования

```python
from transform_rows.transform import transform_rows

example_rows = [
    (42, '2025-04-01', 'extra1', 'extra2', 'extra3', '{"status": "Новая"}', '{"status": "В работе"}')
]

results = transform_rows(example_rows)
for row in results:
    print(row)
```