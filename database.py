"""
Модуль для работы с базой данных шаблонов форм.
"""
from tinydb import TinyDB, Query
from typing import Dict, List, Optional


class FormDatabase:
    """Класс для работы с базой данных шаблонов форм."""
    
    def __init__(self, db_path: str = 'test_db.json'):
        """
        Инициализирует подключение к базе данных.
        
        Args:
            db_path: Путь к файлу базы данных
        """
        self.db = TinyDB(db_path)
        self.forms = self.db.table('forms')
        self.db_path = db_path
    
    def close(self):
        """Закрывает соединение с базой данных."""
        self.db.close()
    
    def add_form(self, form_template: Dict) -> None:
        """
        Добавляет шаблон формы в базу данных.
        
        Args:
            form_template: Словарь с шаблоном формы
        """
        self.forms.insert(form_template)
    
    def find_matching_form(self, fields: Dict[str, str]) -> Optional[str]:
        """
        Находит шаблон формы, все поля которого присутствуют в запросе.
        Если найдено несколько подходящих форм, возвращает форму с наибольшим количеством полей.
        
        Args:
            fields: Словарь с полями запроса (имя_поля: значение)
            
        Returns:
            Имя найденной формы или None, если форма не найдена
        """
        # Определяем типы полей из запроса
        from validators import detect_field_type
        field_types = {name: detect_field_type(value) for name, value in fields.items()}
        
        # Получаем все формы из базы данных
        all_forms = self.forms.all()
        
        best_match = None
        best_match_field_count = 0
        
        # Ищем подходящую форму
        for form in all_forms:
            form_name = form.get('name')
            if not form_name:
                continue
            
            # Проверяем, что все поля шаблона присутствуют в запросе
            form_fields = {k: v for k, v in form.items() if k != 'name'}
            is_match = True
            
            for field_name, field_type in form_fields.items():
                # Проверяем наличие поля в запросе
                if field_name not in field_types:
                    is_match = False
                    break
                
                # Проверяем совпадение типа
                if field_types[field_name] != field_type:
                    is_match = False
                    break
            
            if is_match:
                # Выбираем форму с наибольшим количеством полей
                field_count = len(form_fields)
                if field_count > best_match_field_count:
                    best_match = form_name
                    best_match_field_count = field_count
        
        return best_match
    
    def get_all_forms(self) -> List[Dict]:
        """
        Возвращает все шаблоны форм из базы данных.
        
        Returns:
            Список всех шаблонов форм
        """
        return self.forms.all()
    
    def clear(self) -> None:
        """Очищает базу данных."""
        self.forms.truncate()

