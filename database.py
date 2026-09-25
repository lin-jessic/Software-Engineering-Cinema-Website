import os
import sqlite3
from flask import g

# --- 正確設定你的 SQLite 資料庫路徑 ---
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # 會員資料
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            id_number TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            phone TEXT UNIQUE,
            birthday TEXT,
            bank_account TEXT,
            password TEXT NOT NULL,
            security_question TEXT,
            security_answer  TEXT,
            balance INTEGER DEFAULT 0
        )
        """
    )

    # 訂單資料
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            theater TEXT,
            movie TEXT,
            show_date TEXT,
            show_time TEXT,
            seats TEXT,                -- 例如 "G10,G11"
            ticket_adult INTEGER,
            ticket_student INTEGER,
            food_detail TEXT,          -- 例如 "爆米花套餐 x1"
            total_price INTEGER,
            payment_method TEXT,       -- 'credit', 'cash', 'eticket', 'card'
            status TEXT,               -- 例如 '已完成'
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def register_user(username, id_number, email, phone,
                  birthday, bank_account, password,
                  security_question, security_answer):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # ✅ 檢查 email / id_number / phone 是否已存在
    cur.execute("""
        SELECT
          CASE
            WHEN email = ? THEN 'email'
            WHEN id_number = ? THEN 'id_number'
            WHEN phone = ? THEN 'phone'
          END AS dup
        FROM users
        WHERE email = ? OR id_number = ? OR phone = ?
        LIMIT 1
    """, (email, id_number, phone, email, id_number, phone))

    row = cur.fetchone()
    if row:
        conn.close()
        return (False, row["dup"])

    try:
        cur.execute("""
            INSERT INTO users (
                username, id_number, email, phone,
                birthday, bank_account, password,
                security_question, security_answer
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username, id_number, email, phone,
            birthday, bank_account, password,
            security_question, security_answer
        ))
        conn.commit()
        conn.close()
        return (True, None)

    except sqlite3.IntegrityError as e:
        # 保險：就算同時多人註冊也能抓到重複
        conn.close()
        msg = str(e)
        if "users.email" in msg:
            return (False, "email")
        if "users.id_number" in msg:
            return (False, "id_number")
        if "users.phone" in msg:
            return (False, "phone")
        return (False, "unknown")

def get_all_members():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, phone FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows

# ⭐ 新增：登入驗證用
def verify_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, username, id_number, email, phone, birthday, bank_account, password, balance
        FROM users
        WHERE email = ?
        """,
        (email,),
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    user_id, username, id_number, email_db, phone, birthday, bank_account, pwd_db, balance = row

    if pwd_db == password:
        return {
            "id": user_id,
            "username": username,
            "id_number": id_number,
            "email": email_db,
            "phone": phone,
            "birthday": birthday,
            "bank_account": bank_account,
            "balance": balance if balance is not None else 0,
        }
    else:
        return None
    
# 取得單一使用者（用 id）
def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH, timeout=3)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, email, phone, id_number, birthday, bank_account, balance "
        "FROM users WHERE id = ?",
        (user_id,)
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "phone": row[3],
        "id_number": row[4],
        "birthday": row[5],
        "bank_account": row[6],
        "balance": row[7] if row[7] is not None else 0,
    }


# 更新會員基本資料（姓名、電話、生日、銀行帳號）
def update_user_profile(
    *,
    user_id,
    username,
    email,
    phone,
    birthday,
    bank_account,
    security_question=None,
    security_answer=None
):
    conn = get_db()
    cur = conn.cursor()

    fields = {
        "username": username,
        "email": email,
        "phone": phone,
        "birthday": birthday,
        "bank_account": bank_account,
    }

    # ✅ 只有真的有填才更新（避免變 None）
    if security_question not in (None, ""):
        fields["security_question"] = security_question
    if security_answer not in (None, ""):
        fields["security_answer"] = security_answer

    set_sql = ", ".join([f"{k} = ?" for k in fields])
    values = list(fields.values()) + [user_id]

    cur.execute(
        f"UPDATE users SET {set_sql} WHERE id = ?",
        values
    )
    conn.commit()
    return True

def get_user_security_question(email):
    """忘記密碼第一步：用 email 抓題目"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT id, security_question
        FROM users
        WHERE email = ?
    """, (email,))
    row = cur.fetchone()
    conn.close()
    return row   # row["id"], row["security_question"]


def verify_security_answer(email, question, answer):
    user = get_user_by_email(email)
    return (
        user
        and user["security_question"] == question
        and user["security_answer"] == answer
    )


def get_user_by_email(email):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    # 依你的 row_factory 決定回傳方式
    # 如果你用 sqlite3.Row，就可以 dict(row)
    return dict(row)




# 儲值：把金額加到 balance，回傳最新餘額
def add_balance(user_id, amount):
    conn = sqlite3.connect(DB_PATH, timeout=3)
    cur = conn.cursor()

    # 直接在 SQL 裡做加總
    cur.execute(
        "UPDATE users SET balance = COALESCE(balance, 0) + ? WHERE id = ?",
        (amount, user_id),
    )
    conn.commit()

    # 查詢更新後的餘額
    cur.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    new_balance = cur.fetchone()[0]
    conn.close()
    return new_balance

def use_balance(user_id, amount):
    """從儲值卡扣款，餘額不足會回傳 False"""
    conn = sqlite3.connect(DB_PATH, timeout=3)
    cur = conn.cursor()

    cur.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        return False

    current = row[0] or 0
    if current < amount:
        conn.close()
        return False

    cur.execute(
        "UPDATE users SET balance = balance - ? WHERE id = ?",
        (amount, user_id),
    )
    conn.commit()
    conn.close()
    return True


# 建立一筆訂票紀錄
def create_booking(user_id, movie_title, showtime, quantity):
    conn = sqlite3.connect(DB_PATH, timeout=3)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO bookings (user_id, movie_title, showtime, quantity)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, movie_title, showtime, quantity),
    )
    conn.commit()
    conn.close()


# 查詢某位會員的所有訂票紀錄
def get_bookings_by_user(user_id):
    conn = sqlite3.connect(DB_PATH, timeout=3)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, movie_title, showtime, quantity, created_at
        FROM bookings
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()

    # 回傳 list[dict]
    bookings = []
    for row in rows:
        bookings.append(
            {
                "id": row[0],
                "movie_title": row[1],
                "showtime": row[2],
                "quantity": row[3],
                "created_at": row[4],
            }
        )
    return bookings


def create_order(
    user_id,
    movie_title,
    theater,
    date,
    time,
    ticket_count,
    adult_count=0,
    student_count=0,
    seats="",
    food_detail="",
    payment_method="credit",
    total_price=0,
):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO orders (
            user_id,
            movie_title,
            theater,
            date,
            time,
            ticket_count,
            adult_count,
            student_count,
            seats,
            food_detail,
            payment_method,
            total_price
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            movie_title,
            theater,
            date,
            time,
            ticket_count,
            adult_count,
            student_count,
            seats,
            food_detail,
            payment_method,
            total_price,
        ),
    )
    conn.commit()
    return cur.lastrowid

def cancel_order(order_id, user_id):
    """退票邏輯：標記為已退票，並在需要時退回儲值金額"""

    conn = get_db()
    cur = conn.cursor()

    # 取得訂單資訊
    cur.execute(
        "SELECT status, payment_method, total_price FROM orders WHERE id = ? AND user_id = ?",
        (order_id, user_id)
    )
    row = cur.fetchone()

    if row is None:
        return False   # 訂單不存在

    status, payment_method, total_price = row

    # 如果已退票，不再退一次
    if status == "已退票":
        return True

    # 標記為已退票
    cur.execute(
        "UPDATE orders SET status = '已退票' WHERE id = ? AND user_id = ?",
        (order_id, user_id)
    )

    # ⭐ 若使用儲值卡付款 → 退回金額
    if payment_method == "card":
        cur.execute(
            "UPDATE users SET balance = balance + ? WHERE id = ?",
            (total_price, user_id)
        )

    conn.commit()
    return True

def get_orders_by_user(user_id):
    """取得某位會員的所有訂單（回傳 list[dict]）"""
    conn = get_db()
    # 使用 Row，可以用欄位名稱取值，再轉成 dict
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM orders
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )

    rows = cur.fetchall()
    # 轉成 dict，Jinja 模板就可以用 order.xxx 取值
    return [dict(row) for row in rows]


def get_orders_by_user(user_id):
    """取得某位會員的所有訂單（回傳 list[dict]）"""
    conn = get_db()
    # 使用 Row，可以用欄位名稱取值，再轉成 dict
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM orders
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )

    rows = cur.fetchall()
    # 轉成 dict，Jinja 模板就可以用 order.xxx 取值
    return [dict(row) for row in rows]


def get_order_by_id(order_id, user_id):
    """取得特定一筆訂單（回傳 dict 或 None）"""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM orders
        WHERE id = ? AND user_id = ?
        """,
        (order_id, user_id),
    )

    row = cur.fetchone()
    if row is None:
        return None

    # 回傳 dict，例如：
    # {
    #   "id": ...,
    #   "movie_title": ...,
    #   "adult_count": ...,
    #   "student_count": ...,
    #   "total_price": ...,
    #   "seats": ...,
    #   "food_detail": ...,
    #   "payment_method": ...,
    #   ...
    # }
    return dict(row)


def get_user_by_email(email: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def update_password(email: str, new_password: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
    conn.commit()
    conn.close()

def update_user_password(user_id, new_password):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET password = ?
        WHERE id = ?
    """, (new_password, user_id))

    conn.commit()
    # ⚠️ 不要 conn.close()，交給 teardown
    return True

def check_user_password(user_id, plain_password):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()

    return bool(row and row["password"] == plain_password)