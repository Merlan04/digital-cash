import pandas as pd
from database.db import get_all

def create_excel(user_id: int):
    """
    Создает Excel отчет по всем транзакциям пользователя
    """
    data = get_all(user_id)

    if not data:
        return None

    df = pd.DataFrame(data, columns=["Category", "Amount", "Type", "Date"])

    filename = f"report_{user_id}.xlsx"
    df.to_excel(filename, index=False)

    return filename