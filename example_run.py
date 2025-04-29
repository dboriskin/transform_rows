from transform_rows.transform import transform_rows

if __name__ == "__main__":
    example_rows = [
        (42, '2025-04-01', 'extra1', 'extra2', 'extra3', '{"status": "Новая", "priority": "низкий"}', '{"status": "В работе", "priority": "высокий"}'),
        (43, '2025-04-02', 'extra1', 'extra2', 'extra3', '{"planCount": {"capacityShift": {"id":4628,"value":1020}}}', '{"planCount": {"capacityShift": {"id":4628,"value":1021}}}'),
        (44, '2025-04-03', 'extra1', 'extra2', 'extra3', '{"bad_json": "missing_end_quote}', '{"still_bad": "another"}'),
        (45, '2025-04-04', 'extra1', 'extra2', 'extra3', None, '{"field": "value"}'),
        (46, '2025-04-05', 'extra1', 'extra2', 'extra3', '{"field": "value"}', None),
    ]

    results = transform_rows(example_rows)

    for row in results:
        print(row)