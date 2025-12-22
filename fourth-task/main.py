import sys
from typing import Dict, List, Optional


LOG_LEVELS = ("INFO", "DEBUG", "ERROR", "WARNING")


def parse_log_line(line: str) -> Optional[Dict[str, str]]:
    """
    Парсить один рядок логу у словник:
    {date, time, level, message}

    Якщо рядок не відповідає очікуваному формату — повертає None.
    Очікуваний формат:
    YYYY-MM-DD HH:MM:SS LEVEL Message...
    """
    line = line.strip()
    if not line:
        return None

    parts = line.split(" ", 3)  # date, time, level, message
    if len(parts) < 4:
        return None

    date, time, level, message = parts
    level = level.upper()

    return {"date": date, "time": time, "level": level, "message": message}


def load_logs(file_path: str) -> List[Dict[str, str]]:
    """
    Завантажує логи з файлу у список словників.
    Некоректні рядки пропускаються.
    """
    logs: List[Dict[str, str]] = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parsed = parse_log_line(line)
                if parsed:
                    logs.append(parsed)

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except OSError as exc:
        raise OSError(f"Failed to read file: {file_path}. Error: {exc}") from exc

    return logs


def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    """
    Фільтрує записи логу за рівнем.
    Використано функціональний підхід: filter + lambda.
    """
    level = level.upper()
    return list(filter(lambda log: log.get("level") == level, logs))


def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Рахує кількість записів для кожного рівня логування.
    """
    counts = {lvl: 0 for lvl in LOG_LEVELS}
    for log in logs:
        level = log.get("level")
        if level in counts:
            counts[level] += 1
        else:
            counts[level] = counts.get(level, 0) + 1
    return counts


def display_log_counts(counts: Dict[str, int]) -> None:
    """
    Виводить таблицю статистики.
    """
    header_left = "Рівень логування"
    header_right = "Кількість"

    print(f"{header_left:<17} | {header_right}")
    print("-" * 17 + "-|-" + "-" * 8)

    # Виводимо у заданому порядку рівнів
    for level in LOG_LEVELS:
        print(f"{level:<17} | {counts.get(level, 0)}")


def display_log_details(filtered_logs: List[Dict[str, str]], level: str) -> None:
    """
    Виводить деталі логів для конкретного рівня.
    """
    level = level.upper()
    print(f"\nДеталі логів для рівня '{level}':")

    if not filtered_logs:
        print("Немає записів для цього рівня.")
        return

    for log in filtered_logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py /goit-algo-hw-05/fourth task/logfile.log [level]")
        sys.exit(1)

    file_path = sys.argv[1]
    level_arg = sys.argv[2] if len(sys.argv) >= 3 else None

    try:
        logs = load_logs(file_path)
        counts = count_logs_by_level(logs)
        display_log_counts(counts)

        if level_arg:
            filtered = filter_logs_by_level(logs, level_arg)
            display_log_details(filtered, level_arg)

    except FileNotFoundError as exc:
        print(exc)
        sys.exit(1)
    except OSError as exc:
        print(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
