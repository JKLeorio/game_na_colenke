import sqlite3
db= sqlite3.connect("2048.sqlite")
cur=db.cursor()

def get_best():
    cur.execute("""
    create table if not exists RECORDS (
        name text,
        score integer
    )
    """)

    cur.execute(''' 
    SELECT name, max(score) score FROM RECORDS
    GROUP by name
    ORDER by score DESC
    LIMIT 3 
    ''')
    return(cur.fetchall())

def add_player(player_name,player_score):
    cur.execute(f'''
    INSERT INTO RECORDS(name,score)
    VALUES("{player_name}","{player_score}")
    ''')
    db.commit()
