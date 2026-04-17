"""Unit tests for database operations."""
import unittest

import mysql.connector

from database_operations import (
    check_balance,
    check_pass,
    create_user,
    delete_user,
    deposit_money,
    list_users,
    withdraw_money,
)


class TestAllFunctions(unittest.TestCase):
    """Tests for all database operations."""

    def test_1create_user_and_return(self) -> None:
        """Test user creation and balance check."""
        db = mysql.connector.connect(
            host="192.168.4.112",
            user="root",
            password="password",
            database="bank",
        )
        create_user(db, "testuser", "testpass", 1000)
        balance = check_balance(db, "testuser")
        self.assertEqual(balance, 1000.0)

    def test_2password(self) -> None:
        """Test password check."""
        db = mysql.connector.connect(
            host="192.168.4.112",
            user="root",
            password="password",
            database="bank",
        )
        self.assertTrue(check_pass(db, "testuser", "testpass"))

    def test_3deposit(self) -> None:
        """Test account deposit."""
        db = mysql.connector.connect(
            host="192.168.4.112",
            user="root",
            password="password",
            database="bank",
        )
        deposit_money(db, "testuser", 500)
        balance = check_balance(db, "testuser")
        self.assertEqual(balance, 1500.0)

    def test_4withdraw(self) -> None:
        """Test account withdraw."""
        db = mysql.connector.connect(
            host="192.168.4.112",
            user="root",
            password="password",
            database="bank",
        )
        withdraw_money(db, "testuser", 200)
        balance = check_balance(db, "testuser")
        self.assertEqual(balance, 1300.0)

    def test_5delete_user(self) -> None:
        """Test deleting user."""
        db = mysql.connector.connect(
            host="192.168.4.112",
            user="root",
            password="password",
            database="bank",
        )
        delete_user(db, "testuser")

    def test_6list_users(self) -> None:
        """Test listing users."""
        db = mysql.connector.connect(
            host="192.168.4.112",
            user="root",
            password="password",
            database="bank",
        )
        self.assertEqual(list_users(db), [])

if __name__ == "__main__":
    unittest.main()
