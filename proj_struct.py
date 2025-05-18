import os
import argparse
from pathlib import Path
from typing import List, Set, Optional

def generate_tree_string(
    dir_path: Path,
    level: int = -1,
    limit_to_directories: bool = False,
    length_limit: int = 1000,
    include_hidden: bool = False,
    ignore_list: Optional[List[str]] = None,
    level_prefix: str = "",
    max_depth: Optional[int] = None,
    current_depth: int = 0,
    file_output: Optional[str] = None
) -> List[str]:
    """
    Generates a directory tree structure as a list of strings.

    Args:
        dir_path (Path): The directory path to start from.
        level (int): Not directly used in this recursive version, kept for compatibility.
        limit_to_directories (bool): If True, only list directories.
        length_limit (int): Maximum number of lines to generate (approximate).
        include_hidden (bool): If True, include hidden files/directories (starting with '.').
        ignore_list (Optional[List[str]]): A list of file/directory names to ignore.
        level_prefix (str): The prefix string for the current level's indentation.
        max_depth (Optional[int]): Maximum depth to traverse.
        current_depth (int): The current depth of recursion.
        file_output (Optional[str]): If provided, the tree will also be written to this file.


    Returns:
        List[str]: A list of strings, where each string is a line in the tree.
    """
    if ignore_list is None:
        ignore_list = []

    tree_lines = []
    if current_depth == 0:
        tree_lines.append(f"{dir_path.name}/")

    if max_depth is not None and current_depth >= max_depth:
        return tree_lines

    try:
        contents = sorted(
            [item for item in dir_path.iterdir() if include_hidden or not item.name.startswith('.')],
            key=lambda x: (x.is_file(), x.name.lower()) # Sort directories first, then files, then by name
        )
    except PermissionError:
        tree_lines.append(f"{level_prefix}└── [Error: Permission Denied]")
        return tree_lines
    except FileNotFoundError:
        tree_lines.append(f"{level_prefix}└── [Error: Not Found]")
        return tree_lines


    entries_to_process = [
        entry for entry in contents
        if entry.name not in ignore_list
        and (not limit_to_directories or entry.is_dir())
    ]

    for i, entry in enumerate(entries_to_process):
        if len(tree_lines) >= length_limit:
            tree_lines.append(f"{level_prefix}└── ... (Reached line limit)")
            break

        connector = "└── " if i == len(entries_to_process) - 1 else "├── "
        entry_name = entry.name + ("/" if entry.is_dir() else "")
        tree_lines.append(f"{level_prefix}{connector}{entry_name}")

        if entry.is_dir():
            child_prefix = "    " if i == len(entries_to_process) - 1 else "│   "
            tree_lines.extend(
                generate_tree_string(
                    entry,
                    level + 1, # level is not strictly used but incremented for logical consistency
                    limit_to_directories,
                    length_limit - len(tree_lines),
                    include_hidden,
                    ignore_list,
                    level_prefix + child_prefix,
                    max_depth,
                    current_depth + 1,
                    # file_output is handled by the caller for the final list
                )
            )
    return tree_lines


def main():
    parser = argparse.ArgumentParser(
        description="Генерирует дерево каталогов проекта для README.md.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "root_dir",
        nargs="?",
        default=".",
        help="Корневой каталог проекта (по умолчанию: текущий каталог).",
    )
    parser.add_argument(
        "-d",
        "--max-depth",
        type=int,
        help="Максимальная глубина отображения дерева.",
    )
    parser.add_argument(
        "--dirs-only",
        action="store_true",
        help="Показывать только каталоги.",
    )
    parser.add_argument(
        "-H",
        "--hidden",
        action="store_true",
        help="Включить скрытые файлы и каталоги (начинающиеся с точки).",
    )
    parser.add_argument(
        "-i",
        "--ignore",
        action="append",
        default=[],
        help="Имена файлов или каталогов для игнорирования (можно указать несколько раз).\n"
             "Стандартно игнорируются: .git, __pycache__, .idea, .vscode, venv, .venv, build, dist, *.egg-info",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Файл для сохранения дерева (например, tree.txt).",
    )
    parser.add_argument(
        "--length-limit",
        type=int,
        default=2000, # Increased default limit
        help="Приблизительный лимит на количество строк в выводе (по умолчанию: 2000).",
    )

    args = parser.parse_args()

    root_path = Path(args.root_dir).resolve()

    default_ignore = [
        ".git", "__pycache__", ".idea", ".vscode", "venv", ".venv",
        "build", "dist", "*.egg-info", "node_modules", ".DS_Store"
    ]
    # Combine user-provided ignores with defaults, ensuring uniqueness
    ignore_set = set(default_ignore)
    if args.ignore:
        ignore_set.update(args.ignore)

    print(f"Генерация дерева для: {root_path}")
    if args.max_depth is not None:
        print(f"Максимальная глубина: {args.max_depth}")
    if args.dirs_only:
        print("Режим: только каталоги")
    if args.hidden:
        print("Включая скрытые файлы/каталоги")
    if list(ignore_set): # Check if ignore_set is not empty before printing
        print(f"Игнорируются: {', '.join(sorted(list(ignore_set)))}")
    print("-" * 30)

    try:
        tree_lines = generate_tree_string(
            dir_path=root_path,
            limit_to_directories=args.dirs_only,
            include_hidden=args.hidden,
            ignore_list=list(ignore_set), # Convert set to list for the function
            max_depth=args.max_depth,
            length_limit=args.length_limit
        )
    except Exception as e:
        print(f"Произошла ошибка при генерации дерева: {e}")
        return

    output_string = "\n".join(tree_lines)

    print("\n```text") # Start of Markdown code block
    print(output_string)
    print("```\n") # End of Markdown code block

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(f"{root_path.name}/\n") # Write root dir name first for file output
                f.write("\n".join(tree_lines[1:])) # Write the rest of the tree
            print(f"Дерево проекта сохранено в: {args.output}")
        except IOError as e:
            print(f"Ошибка при сохранении файла: {e}")

if __name__ == "__main__":
    main()