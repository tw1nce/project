"""
Скрипт для инициализации тестовой базы данных с примерами шаблонов форм.
"""
from database import FormDatabase


def init_test_database():
    """Инициализирует тестовую базу данных с примерами шаблонов форм."""
    db = FormDatabase('test_db.json')
    
    # Очищаем базу данных перед заполнением
    db.clear()
    
    # Пример 1: Форма "Данные пользователя"
    db.add_form({
        "name": "Данные пользователя",
        "login": "email",
        "tel": "phone"
    })
    
    # Пример 2: Форма "Форма заказа"
    db.add_form({
        "name": "Форма заказа",
        "customer": "text",
        "order_id": "text",
        "дата_заказа": "date",
        "contact": "phone"
    })
    
    # Пример 3: Форма "Проба"
    db.add_form({
        "name": "Проба",
        "f_name1": "email",
        "f_name2": "date"
    })
    
    # Дополнительные примеры для тестирования
    db.add_form({
        "name": "Простая форма",
        "user_name": "text",
        "user_email": "email"
    })
    
    db.add_form({
        "name": "Форма с датой",
        "event_date": "date",
        "event_name": "text"
    })
    
    db.add_form({
        "name": "Контактная форма",
        "phone": "phone",
        "email": "email",
        "message": "text"
    })
    
    print("Тестовая база данных успешно инициализирована!")
    print(f"Добавлено шаблонов форм: {len(db.get_all_forms())}")


if __name__ == '__main__':
    init_test_database()

