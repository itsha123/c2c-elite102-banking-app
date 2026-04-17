"""All the functions that interact with the users in the database."""
from typing import cast

import bcrypt
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

DBConn = MySQLConnection | MySQLConnectionAbstract | PooledMySQLConnection

def create_user(db: DBConn, username: str, password: str, init_balance: float) -> None:
    """Create a new user in the database."""
    sql = "INSERT INTO users (username, password, balance) VALUES (%s, %s, %s)"
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    val = (username, hashed_password, init_balance)
    cursor = db.cursor()
    cursor.execute(sql, val)
    db.commit()
    cursor.close()

def check_pass(db: DBConn, username: str, password: str) -> bool:
    """Check if provided password is correct."""
    sql = "SELECT password FROM users WHERE username = %s"
    val = (username,)
    cursor = db.cursor()
    cursor.execute(sql, val)
    stored_pass_hash = cast("tuple[str]", cursor.fetchone())[0]
    cursor.close()
    return bcrypt.checkpw(password.encode("utf-8"), stored_pass_hash.encode("utf-8"))

def deposit_money(db: DBConn, username: str, amount: float) -> None:
    """Deposit money into account."""
    sql = "UPDATE users SET balance = balance + %s WHERE username = %s"
    val = (amount, username)
    cursor = db.cursor()
    cursor.execute(sql, val)
    db.commit()
    cursor.close()

def withdraw_money(db: DBConn, username: str, amount: float) -> bool:
    """Withdraw money from account."""
    sql = "SELECT balance FROM users WHERE username = %s"
    val = (username,)
    cursor = db.cursor()
    cursor.execute(sql, val)
    balance = cast("tuple[float]", cursor.fetchone())[0]
    cursor.close()
    if balance > amount:
        sql = "UPDATE users SET balance = balance - %s WHERE username = %s"
        val = (amount, username)
        cursor = db.cursor()
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        return True
    return False

def check_balance(db: DBConn, username: str) -> float:
    """Check account balance."""
    sql = "SELECT balance FROM users WHERE username = %s"
    val = (username,)
    cursor = db.cursor()
    cursor.execute(sql, val)
    balance = cast("tuple[float]", cursor.fetchone())[0]
    cursor.close()
    return balance

def delete_user(db: DBConn, username: str) -> None:
    """Delete user from database."""
    sql = "DELETE FROM users WHERE username = %s"
    val = (username,)
    cursor = db.cursor()
    cursor.execute(sql, val)
    db.commit()
    cursor.close()

def list_users(db: DBConn) -> list[tuple[str, float]]:
    """List all users in the database."""
    sql = "SELECT username, balance FROM users"
    cursor = db.cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    cursor.close()
    return cast("list[tuple[str, float]]", users)
