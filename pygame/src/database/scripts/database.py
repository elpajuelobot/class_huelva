import sqlite3

class DataBase:
    def __init__(self):
        self.CreateTable()

    def CreateTable(self):
        try:
            conn, curs = self.ConnectDB()
            with conn:
                curs.execute("""
                    CREATE TABLE IF NOT EXISTS worlds (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            seed TEXT NOT NULL,
                            player_axis TEXT NOT NULL DEFAULT 'X:400, Y:300',
                            player_health INTEGER NOT NULL DEFAULT 20,
                            player_inventory TEXT,
                            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                            last_played TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
        except conn.Error:
            print("Error")
            conn.rollback()
        finally:
            conn.close()


    def ConnectDB(self):
        conn = sqlite3.connect("src/database/worlds.db")
        conn.row_factory = sqlite3.Row
        return conn, conn.cursor()

    def WriteDelete(self, instruction, data, many=False):
        try:
            conn, curs = self.ConnectDB()
            with conn:
                if many:
                    curs.executemany(instruction, data)
                else:
                    curs.execute(instruction, data)
                conn.commit()
        except conn.Error:
            print("Error")
            conn.rollback()
        finally:
            conn.close()

    def Select(self, instruction, data=None, chall=True):
        try:
            conn, curs = self.ConnectDB()
            params = data if data is not None else ()
            with conn:
                curs.execute(instruction, params)
                if chall:
                    result = curs.fetchall()
                else:
                    result = curs.fetchone()
                return result
        except conn.Error:
            print("Error")
        finally:
            conn.close()
