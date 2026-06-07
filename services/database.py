"""Base de datos SQLite — usuarios, figuritas, intercambios y logros."""

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "album.db"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                google_id TEXT UNIQUE,
                avatar_url TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS user_stickers (
                user_id INTEGER NOT NULL,
                sticker_id TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                PRIMARY KEY (user_id, sticker_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS user_progress (
                user_id INTEGER PRIMARY KEY,
                trivia_today_json TEXT NOT NULL DEFAULT '{}',
                last_unlock_json TEXT,
                custom_team_json TEXT NOT NULL DEFAULT '{}',
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS user_achievements (
                user_id INTEGER NOT NULL,
                achievement_id TEXT NOT NULL,
                unlocked_at TEXT NOT NULL,
                PRIMARY KEY (user_id, achievement_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS exchange_offers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                offer_sticker_id TEXT NOT NULL,
                wanted_rarity TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS sim_matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                opponent_id TEXT NOT NULL,
                opponent_name TEXT NOT NULL,
                user_goals INTEGER NOT NULL,
                opp_goals INTEGER NOT NULL,
                result TEXT NOT NULL,
                played_on TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_sim_matches_user ON sim_matches(user_id);

            CREATE TABLE IF NOT EXISTS user_wallet (
                user_id INTEGER PRIMARY KEY,
                coins_spent INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS cup_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                played_on TEXT NOT NULL,
                round_index INTEGER NOT NULL DEFAULT 0,
                wins INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_cup_runs_user ON cup_runs(user_id);
            """
        )


def create_user(email: str, username: str, password_hash: str | None = None,
                google_id: str | None = None, avatar_url: str | None = None) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO users (email, username, password_hash, google_id, avatar_url, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (email.lower().strip(), username.strip(), password_hash, google_id, avatar_url, _now()),
        )
        user_id = cur.lastrowid
        conn.execute(
            "INSERT INTO user_progress (user_id, trivia_today_json, custom_team_json) VALUES (?, '{}', '{}')",
            (user_id,),
        )
        return user_id


def get_user_by_email(email: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),)).fetchone()
        return dict(row) if row else None


def get_user_by_username(username: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username.strip(),)).fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def get_user_by_google_id(google_id: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE google_id = ?", (google_id,)).fetchone()
        return dict(row) if row else None


def link_google_account(user_id: int, google_id: str, avatar_url: str | None = None) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE users SET google_id = ?, avatar_url = COALESCE(?, avatar_url) WHERE id = ?",
            (google_id, avatar_url, user_id),
        )


def get_user_stickers(user_id: int) -> dict[str, int]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT sticker_id, quantity FROM user_stickers WHERE user_id = ? AND quantity > 0",
            (user_id,),
        ).fetchall()
        return {r["sticker_id"]: r["quantity"] for r in rows}


def add_sticker(user_id: int, sticker_id: str, amount: int = 1) -> None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT quantity FROM user_stickers WHERE user_id = ? AND sticker_id = ?",
            (user_id, sticker_id),
        ).fetchone()
        if row:
            conn.execute(
                "UPDATE user_stickers SET quantity = quantity + ? WHERE user_id = ? AND sticker_id = ?",
                (amount, user_id, sticker_id),
            )
        else:
            conn.execute(
                "INSERT INTO user_stickers (user_id, sticker_id, quantity) VALUES (?, ?, ?)",
                (user_id, sticker_id, amount),
            )


def remove_sticker(user_id: int, sticker_id: str, amount: int = 1) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT quantity FROM user_stickers WHERE user_id = ? AND sticker_id = ?",
            (user_id, sticker_id),
        ).fetchone()
        if not row or row["quantity"] < amount:
            return False
        new_qty = row["quantity"] - amount
        if new_qty <= 0:
            conn.execute(
                "DELETE FROM user_stickers WHERE user_id = ? AND sticker_id = ?",
                (user_id, sticker_id),
            )
        else:
            conn.execute(
                "UPDATE user_stickers SET quantity = ? WHERE user_id = ? AND sticker_id = ?",
                (new_qty, user_id, sticker_id),
            )
        return True


def get_progress_row(user_id: int) -> dict:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM user_progress WHERE user_id = ?", (user_id,)).fetchone()
        if not row:
            conn.execute(
                "INSERT INTO user_progress (user_id) VALUES (?)",
                (user_id,),
            )
            return {"trivia_today_json": "{}", "last_unlock_json": None, "custom_team_json": "{}"}
        return dict(row)


def save_progress_row(user_id: int, trivia_today: dict, last_unlock, custom_team: dict) -> None:
    with get_conn() as conn:
        conn.execute(
            """UPDATE user_progress SET trivia_today_json = ?, last_unlock_json = ?, custom_team_json = ?
               WHERE user_id = ?""",
            (
                json.dumps(trivia_today, ensure_ascii=False),
                json.dumps(last_unlock, ensure_ascii=False) if last_unlock else None,
                json.dumps(custom_team, ensure_ascii=False),
                user_id,
            ),
        )


def get_achievements(user_id: int) -> set[str]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT achievement_id FROM user_achievements WHERE user_id = ?",
            (user_id,),
        ).fetchall()
        return {r["achievement_id"] for r in rows}


def unlock_achievement(user_id: int, achievement_id: str) -> bool:
    with get_conn() as conn:
        try:
            conn.execute(
                "INSERT INTO user_achievements (user_id, achievement_id, unlocked_at) VALUES (?, ?, ?)",
                (user_id, achievement_id, _now()),
            )
            return True
        except sqlite3.IntegrityError:
            return False


def list_exchange_offers(exclude_user_id: int | None = None) -> list[dict]:
    with get_conn() as conn:
        if exclude_user_id:
            rows = conn.execute(
                """SELECT e.*, u.username FROM exchange_offers e
                   JOIN users u ON u.id = e.user_id
                   WHERE e.user_id != ?
                   ORDER BY e.created_at DESC""",
                (exclude_user_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT e.*, u.username FROM exchange_offers e
                   JOIN users u ON u.id = e.user_id ORDER BY e.created_at DESC"""
            ).fetchall()
        return [dict(r) for r in rows]


def get_user_exchange_offers(user_id: int) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM exchange_offers WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def create_exchange_offer_db(user_id: int, offer_sticker_id: str, wanted_rarity: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO exchange_offers (user_id, offer_sticker_id, wanted_rarity, created_at)
               VALUES (?, ?, ?, ?)""",
            (user_id, offer_sticker_id, wanted_rarity, _now()),
        )
        return cur.lastrowid


def get_exchange_offer(offer_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            """SELECT e.*, u.username FROM exchange_offers e
               JOIN users u ON u.id = e.user_id WHERE e.id = ?""",
            (offer_id,),
        ).fetchone()
        return dict(row) if row else None


def delete_exchange_offer(offer_id: int) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM exchange_offers WHERE id = ?", (offer_id,))


def record_sim_match(
    user_id: int,
    opponent_id: str,
    opponent_name: str,
    user_goals: int,
    opp_goals: int,
    result: str,
    played_on: str,
) -> None:
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO sim_matches
               (user_id, opponent_id, opponent_name, user_goals, opp_goals, result, played_on, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, opponent_id, opponent_name, user_goals, opp_goals, result, played_on, _now()),
        )


def count_sim_matches_today(user_id: int, played_on: str) -> int:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM sim_matches WHERE user_id = ? AND played_on = ?",
            (user_id, played_on),
        ).fetchone()
        return int(row["n"]) if row else 0


def get_sim_overall(user_id: int) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """SELECT
                 COUNT(*) AS played,
                 COALESCE(SUM(result = 'win'), 0) AS won,
                 COALESCE(SUM(result = 'draw'), 0) AS drawn,
                 COALESCE(SUM(result = 'loss'), 0) AS lost,
                 COALESCE(SUM(user_goals), 0) AS goals_for,
                 COALESCE(SUM(opp_goals), 0) AS goals_against
               FROM sim_matches WHERE user_id = ?""",
            (user_id,),
        ).fetchone()
        return {
            "played": int(row["played"]),
            "won": int(row["won"]),
            "drawn": int(row["drawn"]),
            "lost": int(row["lost"]),
            "goals_for": int(row["goals_for"]),
            "goals_against": int(row["goals_against"]),
        }


def get_sim_by_opponent(user_id: int) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT opponent_id, opponent_name,
                 COUNT(*) AS played,
                 COALESCE(SUM(result = 'win'), 0) AS won,
                 COALESCE(SUM(result = 'draw'), 0) AS drawn,
                 COALESCE(SUM(result = 'loss'), 0) AS lost
               FROM sim_matches WHERE user_id = ?
               GROUP BY opponent_id, opponent_name
               ORDER BY won DESC, played DESC""",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def get_sim_ranking(limit: int = 20) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT u.username AS username,
                 COUNT(*) AS played,
                 COALESCE(SUM(m.result = 'win'), 0) AS won,
                 COALESCE(SUM(m.result = 'draw'), 0) AS drawn,
                 COALESCE(SUM(m.result = 'loss'), 0) AS lost
               FROM sim_matches m JOIN users u ON u.id = m.user_id
               GROUP BY m.user_id, u.username
               ORDER BY won DESC, played ASC
               LIMIT ?""",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]


def get_coins_spent(user_id: int) -> int:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT coins_spent FROM user_wallet WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return int(row["coins_spent"]) if row else 0


def add_coins_spent(user_id: int, amount: int) -> None:
    """Suma `amount` a las monedas gastadas del usuario (crea la fila si falta)."""
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO user_wallet (user_id, coins_spent) VALUES (?, ?)
               ON CONFLICT(user_id) DO UPDATE SET coins_spent = coins_spent + ?""",
            (user_id, amount, amount),
        )


def get_today_cup_run(user_id: int, played_on: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            """SELECT * FROM cup_runs WHERE user_id = ? AND played_on = ?
               ORDER BY id DESC LIMIT 1""",
            (user_id, played_on),
        ).fetchone()
        return dict(row) if row else None


def create_cup_run(user_id: int, played_on: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO cup_runs (user_id, played_on, round_index, wins, status, created_at, updated_at)
               VALUES (?, ?, 0, 0, 'active', ?, ?)""",
            (user_id, played_on, _now(), _now()),
        )
        return cur.lastrowid


def update_cup_run(run_id: int, round_index: int, wins: int, status: str) -> None:
    with get_conn() as conn:
        conn.execute(
            """UPDATE cup_runs SET round_index = ?, wins = ?, status = ?, updated_at = ?
               WHERE id = ?""",
            (round_index, wins, status, _now(), run_id),
        )


def get_cup_overall(user_id: int) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """SELECT
                 COUNT(*) AS runs,
                 COALESCE(SUM(status = 'champion'), 0) AS champion,
                 COALESCE(SUM(wins >= 3), 0) AS finals,
                 COALESCE(MAX(wins), 0) AS best_wins
               FROM cup_runs WHERE user_id = ?""",
            (user_id,),
        ).fetchone()
        return {
            "runs": int(row["runs"]),
            "champion": int(row["champion"]),
            "finals": int(row["finals"]),
            "best_wins": int(row["best_wins"]),
        }


def reset_user_progress(user_id: int) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM user_stickers WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM user_achievements WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM exchange_offers WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM sim_matches WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM user_wallet WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM cup_runs WHERE user_id = ?", (user_id,))
        conn.execute(
            """UPDATE user_progress SET trivia_today_json = '{}', last_unlock_json = NULL,
               custom_team_json = '{}' WHERE user_id = ?""",
            (user_id,),
        )
