import sqlite3
import os


class DATABASE:
    connection= None
    def __init__(self):
        if DATABASE.connection is None:
            DATABASE.connection=sqlite3.connect("habit_tracing_app.db")
            self.create_tables()

    def connect(self):
        return DATABASE.connection

    def create_tables(self):
        user ="""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """
        habit= """
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                period TEXT NOT NULL,
                created_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """

        habit_completion="""
            CREATE TABLE IF NOT EXISTS habit_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completion_date DATETIME NOT NULL,
                period_number INTEGER NOT NULL,
                FOREIGN KEY(habit_id) REFERENCES habits(id)
            )
        """

        classes=[user
            , habit
            , habit_completion
                 ]

        with DATABASE.connection:
            for table in classes:
                DATABASE.connection.execute(table)

    def drop_database(self):
        if DATABASE.connection:
            DATABASE.connection.close()

        if os.path.exists("habit_tracing_app.db"):
            os.remove("habit_tracing_app.db")

        DATABASE.connection = sqlite3.connect("habit_tracing_app.db")
        self.cursor = DATABASE.connection.cursor()

        self.create_tables()