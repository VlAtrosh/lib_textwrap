"""
Модуль интерфейса командной строки.
"""

import argparse
import sys
from pathlib import Path
from formatter import TextFormatter
from file_handler import FileHandler


def create_parser() -> argparse.ArgumentParser:
    """Создать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Утилита для форматирования текстовых файлов с использованием textwrap",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s file.txt                    # Отформатировать один файл
  %(prog)s -d data/ -w 60              # Обработать все .txt файлы в папке с шириной 60
  %(prog)s file.txt --prefix "> "      # Добавить префикс к каждой строке
  %(prog)s file.txt --dedent           # Нормализовать отступы
  %(prog)s file.txt -o output/        # Сохранить результат в другую папку
        """
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        help='Путь к входному файлу (если не указан, используется -d)'
    )
    
    parser.add_argument(
        '-d', '--directory',
        metavar='DIR',
        help='Директория с текстовыми файлами для обработки'
    )
    
    parser.add_argument(
        '-w', '--width',
        type=int,
        default=80,
        metavar='N',
        help='Ширина строки (по умолчанию: 80)'
    )
    
    parser.add_argument(
        '--prefix',
        metavar='STR',
        help='Префикс для каждой строки (например, "> " для цитат)'
    )
    
    parser.add_argument(
        '--dedent',
        action='store_true',
        help='Нормализовать отступы в многострочном тексте'
    )
    
    parser.add_argument(
        '--shorten',
        type=int,
        metavar='N',
        help='Обрезать текст до N символов с добавлением "..."'
    )
    
    parser.add_argument(
        '--preserve-paragraphs',
        action='store_true',
        help='Сохранять параграфы при форматировании'
    )
    
    parser.add_argument(
        '-o', '--output',
        metavar='DIR',
        help='Директория для сохранения отформатированных файлов'
    )
    
    parser.add_argument(
        '--output-file',
        metavar='FILE',
        help='Путь к выходному файлу (только для одного входного файла)'
    )
    
    parser.add_argument(
        '--no-break-long-words',
        action='store_true',
        help='Не разрывать длинные слова'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Подробный вывод информации о процессе'
    )
    
    return parser


def format_file(
    file_path: str,
    formatter: TextFormatter,
    file_handler: FileHandler,
    options: argparse.Namespace
) -> str:
    """
    Отформатировать один файл.
    
    Args:
        file_path: Путь к файлу
        formatter: Экземпляр форматтера
        file_handler: Обработчик файлов
        options: Параметры форматирования
        
    Returns:
        Отформатированный текст
    """
    try:
        content = file_handler.read_file(file_path)
        
        if options.dedent:
            content = formatter.dedent_text(content)
        
        if options.shorten:
            content = formatter.shorten(content, width=options.shorten)
        elif options.preserve_paragraphs:
            content = formatter.format_paragraphs(content)
        elif options.prefix:
            content = formatter.format_with_prefix(content, options.prefix)
        else:
            content = formatter.fill(content)
        
        return content
    
    except Exception as e:
        if options.verbose:
            raise
        else:
            print(f"Ошибка при обработке {file_path}: {e}", file=sys.stderr)
            return ""


def main():
    """Главная функция CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.input and not args.directory:
        parser.error("Необходимо указать либо входной файл, либо директорию (-d)")
    
    formatter = TextFormatter(
        width=args.width,
        break_long_words=not args.no_break_long_words
    )
    
    file_handler = FileHandler()
    files_to_process = []
    
    if args.input:
        files_to_process = [args.input]
    elif args.directory:
        try:
            files_to_process = file_handler.find_text_files(args.directory)
            if not files_to_process:
                print(f"В директории {args.directory} не найдено текстовых файлов", file=sys.stderr)
                return 1
        except Exception as e:
            print(f"Ошибка при поиске файлов: {e}", file=sys.stderr)
            return 1
    
    if args.verbose:
        print(f"Найдено файлов для обработки: {len(files_to_process)}")
    
    processed_count = 0
    
    for file_path in files_to_process:
        try:
            if args.verbose:
                print(f"Обработка: {file_path}")
            
            formatted_content = format_file(file_path, formatter, file_handler, args)
            
            if not formatted_content and not args.verbose:
                continue
            
            if args.output_file and len(files_to_process) == 1:
                output_path = args.output_file
            elif args.output:
                output_path = file_handler.get_output_path(file_path, args.output)
            else:
                print(f"\n--- {file_path} ---\n")
                print(formatted_content)
                processed_count += 1
                continue
            
            file_handler.write_file(output_path, formatted_content)
            
            if args.verbose:
                print(f"  -> Сохранено: {output_path}")
            
            processed_count += 1
        
        except KeyboardInterrupt:
            print("\nПрервано пользователем", file=sys.stderr)
            return 130
        except Exception as e:
            if args.verbose:
                import traceback
                traceback.print_exc()
            print(f"Ошибка при обработке {file_path}: {e}", file=sys.stderr)
            continue
    
    if args.verbose:
        print(f"\nОбработано файлов: {processed_count}/{len(files_to_process)}")
    
    return 0 if processed_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
