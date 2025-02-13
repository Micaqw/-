def get_mask_card_number(card_number: int) -> str:
    """Функция маскировки номера банковской карты"""
    refactored_card_number: str = str(card_number)
    return " ".join(
        [refactored_card_number[:4], refactored_card_number[4:6], "**", "****", refactored_card_number[-4:]]
    )


def get_mask_account(card_number: int) -> str:
    """Функция маскировки номера банковского счета"""
    refactored_card_number: str = str(card_number)
    return "**" + refactored_card_number[-4:]
