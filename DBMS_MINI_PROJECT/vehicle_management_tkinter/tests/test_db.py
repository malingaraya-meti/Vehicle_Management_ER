import unittest
from src.db.connection import connect_db
from src.db.repository import fetchall, exec_sql

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    def test_connection(self):
        self.assertIsNotNone(self.conn)

    def test_fetchall(self):
        cols, rows = fetchall("SHOW TABLES")
        self.assertIsInstance(cols, list)
        self.assertIsInstance(rows, list)

    def test_exec_sql_insert(self):
        sql = "CREATE TABLE IF NOT EXISTS test_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))"
        success, error = exec_sql(sql)
        self.assertTrue(success)

        sql_insert = "INSERT INTO test_table (name) VALUES (%s)"
        success, error = exec_sql(sql_insert, ("Test Name",))
        self.assertTrue(success)

        sql_select = "SELECT * FROM test_table WHERE name = %s"
        cols, rows = fetchall(sql_select, ("Test Name",))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "Test Name")

    def test_exec_sql_delete(self):
        sql_delete = "DELETE FROM test_table WHERE name = %s"
        success, error = exec_sql(sql_delete, ("Test Name",))
        self.assertTrue(success)

        sql_select = "SELECT * FROM test_table WHERE name = %s"
        cols, rows = fetchall(sql_select, ("Test Name",))
        self.assertEqual(len(rows), 0)

if __name__ == "__main__":
    unittest.main()