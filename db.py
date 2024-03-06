import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('leonardo.db')
        self.c = self.conn.cursor()
        #table
        self.ELEMENT = "ELEMENT"
        self.OPTION = "OPTION"
        self.PROMPT = "PROMPT"
        self.ELEMENTS = "ELEMENTS"
        #columns
        self.user_id = "user_id"
        self.elements = "elements"
        self.alchemy = "alchemy_v2"
        self.photoreal = "photoreal_v2"
        self.gradation = "gradazione"
        self.prompt = "prompt"
        self.post_id = "post_id"
        self.element_name = "element_name"
        self.element_id = "element_id"

    def create_table(self):
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS IMAGE (generationid TEXT PRIMARY KEY, {self.user_id} INT)''')
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.ELEMENT} ({self.element_id} TEXT PRIMARY KEY, {self.user_id} INT, {self.gradation} FLOAT CHECK({self.gradation} >= -1 AND {self.gradation} <= 1))''')
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.OPTION} ({self.user_id} INT PRIMARY KEY, {self.alchemy} BOOL, {self.photoreal} BOOL)''')
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.PROMPT} ({self.user_id} INT PRIMARY KEY, {self.post_id} INT,  {self.prompt} TEXT)''')
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.ELEMENTS} ({self.element_id} TEXT PRIMARY KEY, {self.element_name} TEXT)''')
        return
    
    def insert_element(self, user_id, element_id):
        self.c.execute(f'''INSERT OR REPLACE INTO {self.ELEMENT} ({self.element_id}, {self.user_id}) VALUES (?, ?)''', (element_id, user_id))
        self.conn.commit()

    def update_gradation(self, gradation, element_id):
        self.c.execute(f'''UPDATE {self.ELEMENT} SET {self.gradation} = ? WHERE {self.element_id} = ?''', (gradation, element_id))
        self.conn.commit()

    def get_gradations(self, user_id):
        self.c.execute(f'''SELECT {self.element_id} FROM {self.ELEMENT} WHERE {self.user_id} = ?''', (user_id,))
        rows = self.c.fetchall()
        self.conn.commit()
        return [row[0] for row in rows] if rows else []
    
    def get_gradation(self, user_id, element_id):
        self.c.execute(f'''SELECT {self.gradation} FROM {self.ELEMENT} WHERE {self.user_id} = ? AND {self.element_id} = ?''', (user_id, element_id,))
        rows = self.c.fetchall()
        self.conn.commit()
        return rows[0]

    def get_elements(self, user_id):
        self.c.execute(f'''SELECT {self.element_id} FROM {self.ELEMENT} WHERE {self.user_id} = ?''', (user_id,))
        rows = self.c.fetchall()
        self.conn.commit()
        return [row[0] for row in rows] if rows else []
    
    def delate_elements(self, user_id):
        self.c.execute(f"DELETE FROM {self.ELEMENT} WHERE {self.user_id} = ?", (user_id,)) 
        self.conn.commit()
    
    def insert_option(self, user_id, alchemy, photoreal):
        self.c.execute(f'''INSERT OR REPLACE INTO {self.OPTION} ({self.user_id}, {self.alchemy}, {self.photoreal}) VALUES (?, ?, ?)''', (user_id, alchemy, photoreal))
        self.conn.commit()

    def delate_option(self, user_id):
        self.c.execute(f"DELETE FROM {self.OPTION} WHERE {self.user_id} = ?", (user_id,)) 
        self.conn.commit()

    def get_option(self, user_id):
        self.c.execute(f'''SELECT {self.alchemy}, {self.photoreal} FROM {self.OPTION} WHERE {self.user_id} = ?''', (user_id,))
        rows = self.c.fetchall()
        self.conn.commit()
        if rows:
            return rows[0] # Restituisce il secondo campo della prima riga
        else:
            return None  # Restituisce None se non ci sono risultati

    def image_id(self, user_id, generationid):
        self.c.execute('''INSERT INTO IMAGE (generationid, user_id) VALUES (?, ?)''', 
                        (generationid, user_id))
        self.conn.commit()
    
    def get_image_ids(self, user_id):
        self.c.execute('''SELECT generationid FROM IMAGE WHERE user_id = ?''', (user_id,))
        rows = self.c.fetchall()
        self.conn.commit()
        return [row[0] for row in rows] if rows else []

    def delate_image_id(self, user_id):
        self.c.execute("DELETE FROM IMAGE WHERE user_id = ?", (user_id,)) 
        self.conn.commit()

    def insert_prompt(self, user_id, post_id, prompt):
        self.c.execute(f'''INSERT OR REPLACE INTO {self.PROMPT} ({self.user_id}, {self.post_id}, {self.prompt}) VALUES (?, ?, ?)''', (user_id, post_id, prompt))
        self.conn.commit()

    def get_prompt(self, user_id):
        self.c.execute(f'''SELECT {self.prompt}, {self.post_id} FROM {self.PROMPT} WHERE {self.user_id} = ?''', (user_id,))
        rows = self.c.fetchall()
        self.conn.commit()
        if rows:
            return rows[0] # Restituisce il secondo campo della prima riga
        else:
            return None  # Restituisce None se non ci sono risultati
        
    def delate_prompt(self, user_id):
        self.c.execute(f"DELETE FROM {self.PROMPT} WHERE {self.user_id} = ?", (user_id,)) 
        self.conn.commit()

    def insert_elements_id(self, element_id, element_name):
        self.c.execute(f'''INSERT OR REPLACE INTO {self.ELEMENTS} ({self.element_id}, {self.element_name}) VALUES (?, ?)''', (element_id, element_name))
        self.conn.commit()
        return
    
    def get_element_id(self, element_name):
        self.c.execute(f'''SELECT {self.element_id} FROM {self.ELEMENTS} WHERE {self.element_name} = ?''', (element_name,))
        rows = self.c.fetchall()
        self.conn.commit()
        if rows:
            return rows[0] # Restituisce il secondo campo della prima riga
        else:
            return None  # Restituisce None se non ci sono risultati
        
    def get_element_name(self, user_id):
        self.c.execute(f'''
            SELECT {self.ELEMENTS}.{self.element_name}, COALESCE({self.ELEMENT}.{self.gradation}, 1) AS gradation
            FROM {self.ELEMENT}
            JOIN {self.ELEMENTS} ON {self.ELEMENT}.{self.element_id} = {self.ELEMENTS}.{self.element_id}
            WHERE {self.ELEMENT}.{self.user_id} = ?
        ''', (user_id,))
        rows = self.c.fetchall()
        return [f"{row[0]}:{row[1]}" for row in rows] if rows else []