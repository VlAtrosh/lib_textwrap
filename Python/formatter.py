"""
Модуль форматирования текста с использованием textwrap.
"""

import textwrap
from typing import Optional


class TextFormatter:
    """Класс для форматирования текста с использованием textwrap."""
    
    def __init__(
        self,
        width: int = 80,
        initial_indent: str = "",
        subsequent_indent: str = "",
        expand_tabs: bool = True,
        replace_whitespace: bool = True,
        fix_sentence_endings: bool = False,
        break_long_words: bool = True,
        break_on_hyphens: bool = True,
    ):
        """
        Инициализация форматтера с заданными параметрами.
        
        Args:
            width: Максимальная ширина строки
            initial_indent: Отступ для первой строки
            subsequent_indent: Отступ для последующих строк
            expand_tabs: Заменять ли табуляции на пробелы
            replace_whitespace: Нормализовать ли пробелы
            fix_sentence_endings: Исправлять ли окончания предложений
            break_long_words: Разрывать ли длинные слова
            break_on_hyphens: Разрывать ли по дефисам
        """
        self.wrapper = textwrap.TextWrapper(
            width=width,
            initial_indent=initial_indent,
            subsequent_indent=subsequent_indent,
            expand_tabs=expand_tabs,
            replace_whitespace=replace_whitespace,
            fix_sentence_endings=fix_sentence_endings,
            break_long_words=break_long_words,
            break_on_hyphens=break_on_hyphens,
        )
    
    def wrap(self, text: str) -> list[str]:
        """
        Разбить текст на строки заданной ширины.
        
        Args:
            text: Исходный текст
            
        Returns:
            Список отформатированных строк
        """
        if not text.strip():
            return []
        return self.wrapper.wrap(text)
    
    def fill(self, text: str) -> str:
        """
        Отформатировать текст в одну строку с переносами.
        
        Args:
            text: Исходный текст
            
        Returns:
            Отформатированный текст
        """
        if not text.strip():
            return ""
        return self.wrapper.fill(text)
    
    def dedent_text(self, text: str) -> str:
        """
        Удалить общий начальный отступ из многострочного текста.
        
        Args:
            text: Исходный текст с отступами
            
        Returns:
            Текст с нормализованными отступами
        """
        return textwrap.dedent(text)
    
    def shorten(self, text: str, width: int = 70, placeholder: str = "...") -> str:
        """
        Обрезать текст до заданной длины с добавлением placeholder.
        
        Args:
            text: Исходный текст
            width: Максимальная длина
            placeholder: Строка, добавляемая в конце
            
        Returns:
            Обрезанный текст
        """
        return textwrap.shorten(text, width=width, placeholder=placeholder)
    
    def format_with_prefix(self, text: str, prefix: str) -> str:
        """
        Отформатировать текст с добавлением префикса к каждой строке.
        
        Args:
            text: Исходный текст
            prefix: Префикс для каждой строки
            
        Returns:
            Отформатированный текст с префиксами
        """
        formatter = TextFormatter(
            width=self.wrapper.width,
            initial_indent=prefix,
            subsequent_indent=prefix,
            expand_tabs=self.wrapper.expand_tabs,
            replace_whitespace=self.wrapper.replace_whitespace,
            break_long_words=self.wrapper.break_long_words,
            break_on_hyphens=self.wrapper.break_on_hyphens,
        )
        return formatter.fill(text)
    
    def format_paragraphs(self, text: str) -> str:
        """
        Отформатировать текст, сохраняя параграфы.
        
        Args:
            text: Исходный текст с параграфами
            
        Returns:
            Отформатированный текст с сохранёнными параграфами
        """
        paragraphs = text.split('\n\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            if para.strip():
                formatted_para = self.fill(para.strip())
                formatted_paragraphs.append(formatted_para)
            else:
                formatted_paragraphs.append("")
        
        return '\n\n'.join(formatted_paragraphs)
