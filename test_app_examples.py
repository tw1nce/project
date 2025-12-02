# -*- coding: utf-8 -*-
"""
Скрипт для тестирования примеров использования приложения.
"""
import subprocess
import sys
import os
import io

# Настраиваем вывод для правильной работы с UTF-8 в Windows
if sys.platform == 'win32':
    # Устанавливаем переменную окружения
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # Настраиваем stdout для UTF-8
    if hasattr(sys.stdout, 'buffer'):
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        except:
            pass


def safe_print(text):
    """Безопасный вывод текста с правильной кодировкой."""
    try:
        print(text, end='')
        sys.stdout.flush()
    except UnicodeEncodeError:
        # Если не удалось вывести, пробуем через buffer
        try:
            sys.stdout.buffer.write(text.encode('utf-8', errors='replace'))
            sys.stdout.buffer.flush()
        except:
            print(text.encode('ascii', errors='replace').decode('ascii', errors='replace'), end='')


def run_command(cmd):
    """Запускает команду и выводит результат."""
    safe_print(f"\nВыполняется: {' '.join(cmd)}\n")
    safe_print("-" * 60 + "\n")
    try:
        # Устанавливаем переменные окружения для правильной работы с UTF-8
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # Используем UTF-8 для чтения вывода
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=False,  # Получаем байты, не текст
            env=env
        )
        
        # Декодируем вывод из UTF-8
        if result.stdout:
            try:
                output = result.stdout.decode('utf-8', errors='replace')
                safe_print(output)
            except:
                safe_print(result.stdout.decode('cp1251', errors='replace'))
        
        if result.stderr:
            try:
                error_output = result.stderr.decode('utf-8', errors='replace')
                if error_output.strip() and 'UnicodeDecodeError' not in error_output:
                    safe_print("Ошибки: " + error_output)
            except:
                pass
        
        return result.returncode == 0
    except Exception as e:
        safe_print(f"Ошибка выполнения: {e}\n")
        return False


def main():
    """Запускает тестовые примеры."""
    print("=" * 60)
    print("Тестирование примеров использования приложения")
    print("=" * 60)
    
    examples = [
        # Пример 1: Поиск формы "Проба"
        ['python', 'app.py', 'get_tpl', '--f_name1=vasya@pukin.ru', '--f_name2=27.05.2025'],
        
        # Пример 2: Поиск формы "Форма заказа"
        ['python', 'app.py', 'get_tpl', '--customer=John', '--order_id=123', '--дата_заказа=27.05.2025', '--contact=+7 903 123 45 78'],
        
        # Пример 3: Форма не найдена
        ['python', 'app.py', 'get_tpl', '--tumba=27.05.2025', '--yumba=+7 903 123 45 78'],
        
        # Пример 4: Поиск формы "Данные пользователя"
        ['python', 'app.py', 'get_tpl', '--login=test@example.com', '--tel=+7 999 888 77 66'],
    ]
    
    success_count = 0
    for i, example in enumerate(examples, 1):
        print(f"\nПример {i}:")
        if run_command(example):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"Успешно выполнено: {success_count}/{len(examples)}")
    print("=" * 60)


if __name__ == '__main__':
    main()

