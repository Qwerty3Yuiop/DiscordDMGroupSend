from db import MySqlDb
import dotenv
dotenv.load_dotenv("server/.env")

def user_table(db:MySqlDb):
    query = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY,
            username VARCHAR(30) NOT NULL,
            private_key BLOB NOT NULL,
            public_key BLOB NOT NULL
        );
    """
    db.query(query)

def messages_table(db:MySqlDb):
    query = """
        CREATE TABLE IF NOT EXISTS messages (
            id VARCHAR(36) PRIMARY KEY,
            time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            message TEXT NOT NULL,
            embeddings JSON NOT NULL,
            tags JSON NOT NULL,
            sent BOOLEAN DEFAULT FALSE,
            user_id VARCHAR(36) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """
    db.query(query)

def state_table(db:MySqlDb):
    query = """
        CREATE TABLE state (
            id VARCHAR(36) PRIMARY KEY,
            user_id VARCHAR(36) NOT NULL,
            message_id VARCHAR(36) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (message_id) REFERENCES messages(id)
        );
    """

if __name__ == "__main__":
    db = MySqlDb()
    user_table(db)
    messages_table(db)