import matplotlib.pyplot as plt
from database.db import get_expenses

def create_chart(user):

    data = get_expenses(user)

    if not data:
        return None

    labels = []
    values = []

    for cat, val in data:
        labels.append(cat)
        values.append(val)

    plt.figure()
    plt.pie(values, labels=labels, autopct="%1.1f%%")

    filename = f"chart_{user}.png"
    plt.savefig(filename)
    plt.close()  # ✅ ДОБАВЬТЕ ЭТО

    return filename