import pytest
from typing import List, Dict, Any
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

transactions: List[Dict[str, Any]] = [
    {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
    {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
    {"id": 3, "operationAmount": {"currency": {"code": "EUR"}}},
    {"id": 4}  # Без operationAmount
]


@pytest.mark.parametrize(
    "currency, expected_count",
    [
        ("USD", 2),
        ("EUR", 1),
        ("GBP", 0),
    ],
)
def test_filter_by_currency(currency: str, expected_count: int) -> None:
    """Проверяет фильтрацию транзакций по валюте."""
    filtered = list(filter_by_currency(transactions, currency))
    assert len(filtered) == expected_count
    for transaction in filtered:
        assert transaction["operationAmount"]["currency"]["code"] == currency


def test_filter_by_currency_empty_list() -> None:
    """Проверяет обработку пустого списка."""
    filtered = list(filter_by_currency([], "USD"))
    assert len(filtered) == 0


def test_filter_by_currency_no_operation_amount() -> None:
    """Проверяет, что транзакции без operationAmount игнорируются."""
    filtered = list(filter_by_currency([{"id": 1}], "USD"))
    assert len(filtered) == 0


@pytest.mark.parametrize(
    "transactions, expected_descriptions",
    [
        (
            [
                {'description': 'Зарплата'},
                {'description': 'Покупка'},
                {'description': 'Перевод другу'},
            ],
            [
                "Зарплата",
                "Покупка",
                "Перевод другу",
            ],
        ),
        (
            [
                {'description': None},
                {'other_field': 'value'},
                {},
            ],
            [
                "Описание отсутствует",
                "Описание отсутствует",
                "Описание отсутствует",
            ],
        ),
        ([], ["Транзакции отсутствуют"]),
    ],
)
def test_transaction_descriptions(transactions: List[Dict[str, Any]], expected_descriptions: List[str]) -> None:
    """Проверяет генерацию описаний транзакций."""
    assert list(transaction_descriptions(transactions)) == expected_descriptions


@pytest.mark.parametrize(
    "start, end, expected_numbers",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9999999999999998, 10000000000000000, ["9999 9999 9999 9998", "9999 9999 9999 9999", "1000 0000 0000 0000"]),
        (5, 4, []),
    ],
)
def test_card_number_generator_range(start: int, end: int, expected_numbers: List[str]) -> None:
    generated_numbers = list(card_number_generator(start, end))
    assert generated_numbers == expected_numbers


def test_card_number_generator_formatting() -> None:
    generated_number = next(card_number_generator(10, 10))
    assert len(generated_number) == 19
    assert generated_number.count(" ") == 3
    assert all(c.isdigit() or c == " " for c in generated_number)