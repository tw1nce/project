"""
CLI приложение для поиска шаблонов форм в базе данных.
"""
import sys
import json
import io
from typing import Dict
from database import FormDatabase
from validators import detect_field_type

# Устанавливаем правильную кодировку для вывода в Windows
if sys.platform == 'win32':
    # Проверяем, не перенаправлен ли вывод
    if hasattr(sys.stdout, 'buffer'):
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        except (AttributeError, ValueError):
            # Если не удалось перенастроить, пробуем установить через переменную окружения
            import os
            os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stderr, 'buffer'):
        try:
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        except (AttributeError, ValueError):
            pass


def parse_arguments(args: list) -> Dict[str, str]:
    """
    Парсит аргументы командной строки в формате --имя_поля=значение.
    
    Args:
        args: Список аргументов командной строки
        
    Returns:
        Словарь с полями (имя_поля: значение)
    """
    fields = {}
    
    for arg in args:
        if arg.startswith('--'):
            # Убираем '--' и разделяем на имя и значение
            arg_part = arg[2:]
            if '=' in arg_part:
                field_name, field_value = arg_part.split('=', 1)
                fields[field_name] = field_value
            else:
                # Если нет значения, пропускаем
                continue
    
    return fields


def main():
    """Основная функция приложения."""
    if len(sys.argv) < 2:
        print("Использование: app.py get_tpl --имя_поля=значение --имя_поля=значение")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command != 'get_tpl':
        print(f"Неизвестная команда: {command}")
        print("Использование: app.py get_tpl --имя_поля=значение --имя_поля=значение")
        sys.exit(1)
    
    # Парсим аргументы
    fields = parse_arguments(sys.argv[2:])
    
    if not fields:
        print("Ошибка: не указаны поля для поиска")
        sys.exit(1)
    
    # Ищем подходящий шаблон
    db = FormDatabase()
    try:
        form_name = db.find_matching_form(fields)
        
        if form_name:
            # Если форма найдена, выводим её имя
            print(form_name, flush=True)
        else:
            # Если форма не найдена, выводим JSON с типами полей
            field_types = {name: detect_field_type(value) for name, value in fields.items()}
            # Форматируем вывод как в примере (без кавычек вокруг ключей)
            result = "{\n"
            items = []
            for name, ftype in field_types.items():
                items.append(f"  {name}: {ftype}")
            result += ",\n".join(items)
            result += "\n}"
            print(result, flush=True)
    finally:
        db.close()


if __name__ == '__main__':
    main()

