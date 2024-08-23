import sqlite3

def read_from_db():
    conn = sqlite3.connect('../../momentum_ai/news.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM news
    ''')
    
    # Fetch all rows from the executed query
    all_news = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return all_news