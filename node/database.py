import sqlite3
import json

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('servers.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS servers (
            id TEXT PRIMARY KEY,
            hostname TEXT,
            ip TEXT,
            os_type TEXT,
            capabilities TEXT,
            last_seen TEXT,
            token TEXT
        )
        ''')
        self.conn.commit()

    def add_server(self, server_data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO servers 
        (id, hostname, ip, os_type, capabilities, last_seen, token)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            server_data['id'],
            server_data['hostname'],
            server_data['ip'],
            server_data['os_type'],
            json.dumps(server_data['capabilities']),
            server_data['last_seen'],
            server_data['token']
        ))
        self.conn.commit()

    def get_all_servers(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM servers')
        columns = [description[0] for description in cursor.description]
        servers = []
        for row in cursor.fetchall():
            server = dict(zip(columns, row))
            server['capabilities'] = json.loads(server['capabilities'])
            servers.append(server)
        return servers 