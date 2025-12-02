"""
Модуль для валидации типов полей форм.
"""
import re
from datetime import datetime


def validate_email(value: str) -> bool:
    """
    Проверяет, является ли значение валидным email адресом.
    
    Args:
        value: Строка для проверки
        
    Returns:
        True если значение является валидным email, иначе False
    """
    # Проверка на двойные точки и точки в начале/конце локальной части
    if '..' in value or value.startswith('.') or value.endswith('.'):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, value))


def validate_phone(value: str) -> bool:
    """
    Проверяет, является ли значение валидным телефоном в формате +7 ХХХ ХХХ ХХ ХХ.
    
    Args:
        value: Строка для проверки
        
    Returns:
        True если значение является валидным телефоном, иначе False
    """
    pattern = r'^\+7 \d{3} \d{3} \d{2} \d{2}$'
    return bool(re.match(pattern, value))


def validate_date(value: str) -> bool:
    """
    Проверяет, является ли значение валидной датой в формате DD.MM.YYYY или YYYY-MM-DD.
    
    Args:
        value: Строка для проверки
        
    Returns:
        True если значение является валидной датой, иначе False
    """
    # Формат DD.MM.YYYY
    pattern1 = r'^\d{2}\.\d{2}\.\d{4}$'
    if re.match(pattern1, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except ValueError:
            return False
    
    # Формат YYYY-MM-DD
    pattern2 = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(pattern2, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    return False


def detect_field_type(value: str) -> str:
    """
    Определяет тип поля на основе валидации.
    Проверка производится в порядке: date, phone, email, text.
    
    Args:
        value: Значение поля
        
    Returns:
        Тип поля: 'date', 'phone', 'email' или 'text'
    """
    if validate_date(value):
        return 'date'
    if validate_phone(value):
        return 'phone'
    if validate_email(value):
        return 'email'
    return 'text'

