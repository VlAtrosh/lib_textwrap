"""
Модуль для работы с файлами.
"""

import os
from pathlib import Path
from typing import List, Optional


class FileHandler:
    """Класс для чтения и записи текстовых файлов."""
    
    def __init__(self, encoding: str = "utf-8"):
        """
        Инициализация обработчика файлов.
        
        Args:
            encoding: Кодировка файлов
        """
        self.encoding = encoding
    
    def read_file(self, file_path: str) -> str:
        """
        Прочитать содержимое текстового файла.
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            Содержимое файла как строка
            
        Raises:
            FileNotFoundError: Если файл не найден
            PermissionError: Если нет прав на чтение
            UnicodeDecodeError: Если файл не в UTF-8
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        
        if not path.is_file():
            raise ValueError(f"Путь указывает не на файл: {file_path}")
        
        try:
            with open(path, 'r', encoding=self.encoding) as f:
                return f.read()
        except PermissionError:
            raise PermissionError(f"Нет прав на чтение файла: {file_path}")
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(
                f"Ошибка декодирования файла {file_path}. "
                f"Убедитесь, что файл в кодировке {self.encoding}"
            )
    
    def write_file(self, file_path: str, content: str) -> None:
        """
        Записать содержимое в текстовый файл.
        
        Args:
            file_path: Путь к файлу
            content: Содержимое для записи
            
        Raises:
            PermissionError: Если нет прав на запись
            OSError: При ошибках записи
        """
        path = Path(file_path)
        
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding=self.encoding) as f:
                f.write(content)
        except PermissionError:
            raise PermissionError(f"Нет прав на запись в файл: {file_path}")
        except OSError as e:
            raise OSError(f"Ошибка записи файла {file_path}: {e}")
    
    def find_text_files(self, directory: str, extensions: List[str] = None) -> List[str]:
        """
        Найти все текстовые файлы в директории.
        
        Args:
            directory: Путь к директории
            extensions: Список расширений файлов (по умолчанию .txt)
            
        Returns:
            Список путей к найденным файлам
            
        Raises:
            NotADirectoryError: Если путь не является директорией
        """
        if extensions is None:
            extensions = ['.txt']
        
        path = Path(directory)
        
        if not path.exists():
            raise FileNotFoundError(f"Директория не найдена: {directory}")
        
        if not path.is_dir():
            raise NotADirectoryError(f"Путь не является директорией: {directory}")
        
        files = []
        for ext in extensions:
            files.extend(path.glob(f"*{ext}"))
        
        return sorted([str(f) for f in files if f.is_file()])
    
    def get_output_path(self, input_path: str, output_dir: Optional[str] = None, suffix: str = "_formatted") -> str:
        """
        Сформировать путь для выходного файла.
        
        Args:
            input_path: Путь к входному файлу
            output_dir: Директория для выходных файлов (опционально)
            suffix: Суффикс для имени файла
            
        Returns:
            Путь к выходному файлу
        """
        input_path_obj = Path(input_path)
        stem = input_path_obj.stem
        extension = input_path_obj.suffix
        
        if output_dir:
            output_path_obj = Path(output_dir)
            output_path_obj.mkdir(parents=True, exist_ok=True)
            return str(output_path_obj / f"{stem}{suffix}{extension}")
        else:
            return str(input_path_obj.parent / f"{stem}{suffix}{extension}")
