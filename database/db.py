import sqlite3
from config import DB_NAME


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connect()
    cur = conn.cursor()

    # Старые таблицы
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

    # 🆕 НОВЫЕ ТАБЛИЦЫ ДЛЯ ЦЕЛЕЙ
    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_goals(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    goal_text TEXT,
    priority TEXT,
    created_date TEXT,
    status TEXT DEFAULT 'pending'
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS goal_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    goal_id INTEGER,
    completed_date TEXT,
    status TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_settings(
    user_id INTEGER PRIMARY KEY,
    morning_reminder_hour INTEGER DEFAULT 5,
    evening_report_hour INTEGER DEFAULT 23,
    reminder_interval INTEGER DEFAULT 2
    )
    """)

    # 🆕 ТАБЛИЦА ДЛЯ FSM STORAGE (вместо MemoryStorage)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fsm_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    state TEXT,
    data TEXT,
    updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()


# ========== ФУНКЦИИ ДЛЯ ЦЕЛЕЙ ==========

def add_goal(user_id, goal_text, priority='medium'):
    """Добавить новую цель"""
    conn = connect()
    cur = conn.cursor()
    
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    
    cur.execute(
        "INSERT INTO daily_goals(user_id, goal_text, priority, created_date, status) VALUES(?,?,?,?,?)",
        (user_id, goal_text, priority, today, 'pending')
    )
    
    conn.commit()
    conn.close()


def get_today_goals(user_id):
    """Получить цели на сегодня"""
    conn = connect()
    cur = conn.cursor()
    
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    
    cur.execute(
        "SELECT id, goal_text, priority, status FROM daily_goals WHERE user_id=? AND created_date=? ORDER BY priority DESC",
        (user_id, today)
    )
    
    data = cur.fetchall()
    conn.close()
    
    return data


def complete_goal(goal_id):
    """Отметить цель как выполненную"""
    conn = connect()
    cur = conn.cursor()
    
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Обновляем статус цели
    cur.execute("UPDATE daily_goals SET status='completed' WHERE id=?", (goal_id,))
    
    # Добавляем в историю
    cur.execute(
        "SELECT user_id FROM daily_goals WHERE id=?",
        (goal_id,)
    )
    result = cur.fetchone()
    
    if result:
        user_id = result[0]
        cur.execute(
            "INSERT INTO goal_history(user_id, goal_id, completed_date, status) VALUES(?,?,?,?)",
            (user_id, goal_id, today, 'completed')
        )
    
    conn.commit()
    conn.close()


def incomplete_goal(goal_id):
    """Отметить цель как невыполненную"""
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("UPDATE daily_goals SET status='incomplete' WHERE id=?", (goal_id,))
    
    conn.commit()
    conn.close()


def get_goal_stats(user_id):
    """Получить статистику выполнения целей"""
    conn = connect()
    cur = conn.cursor()
    
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Всего целей на сегодня
    cur.execute(
        "SELECT COUNT(*) FROM daily_goals WHERE user_id=? AND created_date=?",
        (user_id, today)
    )
    total = cur.fetchone()[0]
    
    # Выполнено целей
    cur.execute(
        "SELECT COUNT(*) FROM daily_goals WHERE user_id=? AND created_date=? AND status='completed'",
        (user_id, today)
    )
    completed = cur.fetchone()[0]
    
    # Невыполненные цели
    cur.execute(
        "SELECT goal_text FROM daily_goals WHERE user_id=? AND created_date=? AND status='incomplete'",
        (user_id, today)
    )
    incomplete = cur.fetchall()
    
    conn.close()
    
    return {
        'total': total,
        'completed': completed,
        'incomplete': len(incomplete),
        'incomplete_list': [g[0] for g in incomplete],
        'percentage': round((completed / total * 100) if total > 0 else 0, 1)
    }


def delete_old_goals(user_id, days=7):
    """Удалить старые цели (старше N дней)"""
    conn = connect()
    cur = conn.cursor()
    
    from datetime import datetime, timedelta
    old_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    cur.execute(
        "DELETE FROM daily_goals WHERE user_id=? AND created_date < ?",
        (user_id, old_date)
    )
    
    conn.commit()
    conn.close()


# ========== ФУНКЦИИ ДЛЯ FSM STORAGE ==========

def save_fsm_state(user_id, state, data):
    """Сохранить состояние FSM"""
    conn = connect()
    cur = conn.cursor()
    
    from datetime import datetime
    now = datetime.now().isoformat()
    
    import json
    data_json = json.dumps(data) if isinstance(data, dict) else data
    
    # Проверяем, есть ли уже запись
    cur.execute("SELECT id FROM fsm_data WHERE user_id=?", (user_id,))
    existing = cur.fetchone()
    
    if existing:
        cur.execute(
            "UPDATE fsm_data SET state=?, data=?, updated_at=? WHERE user_id=?",
            (state, data_json, now, user_id)
        )
    else:
        cur.execute(
            "INSERT INTO fsm_data(user_id, state, data, updated_at) VALUES(?,?,?,?)",
            (user_id, state, data_json, now)
        )
    
    conn.commit()
    conn.close()


def get_fsm_state(user_id):
    """Получить состояние FSM"""
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("SELECT state, data FROM fsm_data WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    conn.close()
    
    if result:
        import json
        try:
            data = json.loads(result[1])
        except:
            data = result[1]
        return result[0], data
    
    return None, None


def delete_fsm_state(user_id):
    """Удалить состояние FSM"""
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM fsm_data WHERE user_id=?", (user_id,))
    
    conn.commit()
    conn.close()


# ========== ФУНКЦИИ ДЛЯ ПОЛЬЗОВАТЕЛЬСКИХ НАСТРОЕК ==========

def set_user_settings(user_id, morning_hour=5, evening_hour=23, interval=2):
    """Установить настройки пользователя"""
    conn = connect()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT OR REPLACE INTO user_settings(user_id, morning_reminder_hour, evening_report_hour, reminder_interval) VALUES(?,?,?,?)",
        (user_id, morning_hour, evening_hour, interval)
    )
    
    conn.commit()
    conn.close()


def get_user_settings(user_id):
    """Получить настройки пользователя"""
    conn = connect()
    cur = conn.cursor()
    
    cur.execute(
        "SELECT morning_reminder_hour, evening_report_hour, reminder_interval FROM user_settings WHERE user_id=?",
        (user_id,)
    )
    
    result = cur.fetchone()
    conn.close()
    
    if result:
        return {
            'morning_hour': result[0],
            'evening_hour': result[1],
            'interval': result[2]
        }
    
    return {
        'morning_hour': 5,
        'evening_hour': 23,
        'interval': 2
    }


# ========== СТАРЫЕ ФУНКЦИИ (без изменений) ==========

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
