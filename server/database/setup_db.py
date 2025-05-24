from db import MySqlDb

def user_table(db:MySqlDb):
    query = """
        CREATE TABLE users (
            id VARCHAR(36) PRIMARY KEY,
            username VARCHAR(30) NOT NULL,
            private_key BLOB NOT NULL,
            public_key BLOB NOT NULL
        );
    """
    db.query(query)

def messages_table(db:MySqlDb):
    query = """
        CREATE TABLE messages (
            id VARCHAR(36) PRIMARY KEY,
            time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            message BLOB NOT NULL,
            embedding BLOB,
            metadata BLOB NOT NULL,
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