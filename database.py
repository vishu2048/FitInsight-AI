
import sqlite3
from pathlib import Path


# ==========================================
# DATABASE LOCATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "fitinsight.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    # Enable foreign key checking
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ==========================================
# CREATE TABLES
# ==========================================

def create_tables():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # --------------------------------------
        # USERS TABLE
        # --------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                age INTEGER,

                gender TEXT,

                height REAL,

                weight REAL,

                activity_level TEXT,

                goal TEXT,

                target_weight REAL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # --------------------------------------
        # DAILY LOGS TABLE
        # --------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_logs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                date TEXT NOT NULL,

                weight REAL,

                steps INTEGER,

                sleep_duration REAL,

                workout_duration REAL,

                calories_burned REAL,

                calories_consumed REAL,

                water_intake REAL,

                notes TEXT,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
            )
        """)

        connection.commit()

        # --------------------------------------
        # CHECK EXISTING DUPLICATE CHECK-INS
        # --------------------------------------

        cursor.execute("""
            SELECT
                user_id,
                date,
                COUNT(*) AS duplicate_count
            FROM daily_logs
            GROUP BY user_id, date
            HAVING COUNT(*) > 1
        """)

        duplicates = cursor.fetchall()

        if duplicates:

            print("\nWARNING: Existing duplicate check-ins found.")

            for duplicate in duplicates:
                print(
                    f"User ID: {duplicate['user_id']} | "
                    f"Date: {duplicate['date']} | "
                    f"Records: {duplicate['duplicate_count']}"
                )

            print(
                "Unique index was not created. "
                "Existing records have been preserved."
            )

        else:

            # --------------------------------------
            # DATABASE-LEVEL DUPLICATE PROTECTION
            # --------------------------------------

            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS
                idx_daily_logs_user_date
                ON daily_logs(user_id, date)
            """)

            connection.commit()

            print("Daily check-in duplicate protection enabled.")

        print("Database tables checked successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ==========================================
# GET EXISTING DUPLICATE CHECK-INS
# ==========================================

def get_duplicate_daily_logs():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                user_id,
                date,
                COUNT(*) AS duplicate_count
            FROM daily_logs
            GROUP BY user_id, date
            HAVING COUNT(*) > 1
            ORDER BY date DESC
        """)

        return cursor.fetchall()

    finally:
        connection.close()


# ==========================================
# ADD USER
# ==========================================

def add_user(
    name,
    age,
    gender,
    height,
    weight,
    activity_level,
    goal,
    target_weight
):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (
                name,
                age,
                gender,
                height,
                weight,
                activity_level,
                goal,
                target_weight
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            age,
            gender,
            height,
            weight,
            activity_level,
            goal,
            target_weight
        ))

        connection.commit()

        return cursor.lastrowid

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ==========================================
# GET USER
# ==========================================

def get_user(user_id=1):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE id = ?
        """, (user_id,))

        return cursor.fetchone()

    finally:
        connection.close()


# ==========================================
# UPDATE USER
# ==========================================

def update_user(
    user_id,
    name,
    age,
    gender,
    height,
    weight,
    activity_level,
    goal,
    target_weight
):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE users
            SET
                name = ?,
                age = ?,
                gender = ?,
                height = ?,
                weight = ?,
                activity_level = ?,
                goal = ?,
                target_weight = ?
            WHERE id = ?
        """, (
            name,
            age,
            gender,
            height,
            weight,
            activity_level,
            goal,
            target_weight,
            user_id
        ))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ==========================================
# GET LATEST DAILY LOG
# ==========================================

def get_latest_daily_log(user_id=1):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM daily_logs
            WHERE user_id = ?
            ORDER BY date DESC, id DESC
            LIMIT 1
        """, (user_id,))

        return cursor.fetchone()

    finally:
        connection.close()


# ==========================================
# GET ALL DAILY LOGS
# ==========================================

def get_daily_logs(user_id=1):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM daily_logs
            WHERE user_id = ?
            ORDER BY date ASC, id ASC
        """, (user_id,))

        return cursor.fetchall()

    finally:
        connection.close()


# ==========================================
# INITIALIZE DATABASE
# ==========================================

if __name__ == "__main__":

    create_tables()

    print("================================")
    print("FitInsight AI Database")
    print("================================")
    print(f"Database: {DATABASE_PATH}")
    print("Database initialization completed.")
