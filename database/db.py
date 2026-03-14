import sqlite3
from config import DB_NAME


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,
    category TEXT,
    amount INTEGER,
    date TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(user_id, first_name, last_name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users(user_id, first_name, last_name) VALUES(?,?,?)",
        (user_id, first_name, last_name)
    )

    conn.commit()
    conn.close()


def get_all_users():
    """Получить всех пользователей"""
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM users")
    data = cur.fetchall()
    conn.close()

    return [row[0] for row in data]


def add_transaction(user, ttype, category, amount, date):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO transactions(user_id,type,category,amount,date) VALUES(?,?,?,?,?)",
        (user, ttype, category, amount, date)
    )

    conn.commit()
    conn.close()


def get_expenses(user):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT category,SUM(amount)
    FROM transactions
    WHERE user_id=? AND type='expense'
    GROUP BY category
    """, (user,))

    data = cur.fetchall()
    conn.close()

    return data


def get_all(user):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, category,amount,type,date
    FROM transactions
    WHERE user_id=?
    ORDER BY date DESC
    """, (user,))

    data = cur.fetchall()
    conn.close()

    return data


def update_transaction(transaction_id, new_amount):
    """Обновить сумму транзакции"""
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE transactions SET amount=? WHERE id=?",
        (new_amount, transaction_id)
    )

    conn.commit()
    conn.close()


def delete_transaction(transaction_id):
    """Удалить транзакцию"""
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))

    conn.commit()
    conn.close()


def delete_all_transactions(user_id):
    """Удалить все транзакции пользователя"""
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM transactions WHERE user_id=?", (user_id,))

    conn.commit()
    conn.close()

    def get_last_transaction(user_id):
        """Получить последнюю транзакцию"""
        conn = connect()
        cur = conn.cursor()

        cur.execute("""
        SELECT * FROM transactions
        WHERE user_id=?
        ORDER BY date DESC
        LIMIT 1
        """, (user_id,))

        data = cur.fetchone()
        conn.close()

        return data