
import re
from typing import Callable, Iterable

def generator_numbers(text: str) -> Iterable[float]:
    """
        Генерує всі дійсні числа з тексту як float.
        Вважаємо, що числа коректні і відокремлені пробілами з обох боків.
        """
    pattern = r'(?<!\S)[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?!\S)'

    for match in re.finditer(pattern, text):
        yield float(match.group())

def sum_profit(text: str, func: Callable[[str], Iterable[float]]) -> float:
    """
    Обчислює суму всіх чисел у тексті,
    використовуючи generator_numbers.
    """
    return sum(func(text))

if __name__ == "__main__":
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими надходженнями "
        "27.45 і 324.00 доларів."
    )

    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")