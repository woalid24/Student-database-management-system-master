import sqlite3
import os


def connect():
    '''Create a database if not existed and make a connection to it.
    Also, sets up the trigger and view if they do not already exist.
    '''
    conn = sqlite3.connect("Students.db")
    cur = conn.cursor()
    
    # Create the main table
    cur.execute("CREATE TABLE IF NOT EXISTS data1 (id INTEGER PRIMARY KEY, fn TEXT, ln TEXT, term INTEGER, gpa REAL)")
    
    # Create a log table for the trigger
    cur.execute("""
        CREATE TABLE IF NOT EXISTS data1_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            old_data TEXT,
            new_data TEXT,
            change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create the trigger for logging updates
    cur.execute("""
        CREATE TRIGGER IF NOT EXISTS log_data1_update
        AFTER UPDATE ON data1
        FOR EACH ROW
        BEGIN
            INSERT INTO data1_log (old_data, new_data)
            VALUES (
                json_object('id', OLD.id, 'fn', OLD.fn, 'ln', OLD.ln, 'term', OLD.term, 'gpa', OLD.gpa),
                json_object('id', NEW.id, 'fn', NEW.fn, 'ln', NEW.ln, 'term', NEW.term, 'gpa', NEW.gpa)
            );
        END;
    """)
    
    # Create a view to list students with GPA above 3.0
    cur.execute("""
        CREATE VIEW IF NOT EXISTS high_gpa_students AS
        SELECT id, fn, ln, term, gpa 
        FROM data1 
        WHERE gpa > 3.0
    """)
    
    conn.commit()
    conn.close()


def insert(fn, ln, term, gpa):
    '''Insertion function to insert a new student into the database.'''
    conn = sqlite3.connect("Students.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO data1 VALUES (NULL, ?, ?, ?, ?)", (fn, ln, term, gpa))
    conn.commit()
    conn.close()


def view():
    '''View function to show the content of the main table.'''
    conn = sqlite3.connect("Students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM data1")
    rows = cur.fetchall()
    conn.close()
    return rows


def view_high_gpa_students():
    '''View function to show the content of the high GPA students view.'''
    conn = sqlite3.connect("Students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM high_gpa_students")
    rows = cur.fetchall()
    conn.close()
    return rows


def search(fn="", ln="", term="", gpa=""):
    '''Search function to find specific students in the database.'''
    conn = sqlite3.connect("Students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM data1 WHERE fn=? OR ln=? OR term=? OR gpa=?", (fn, ln, term, gpa))
    rows = cur.fetchall()
    conn.close()
    return rows


def delete(id):
    '''Delete function to remove a student by ID.'''
    conn = sqlite3.connect("Students.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM data1 WHERE id=?", (id,))
    conn.commit()
    conn.close()


def update(id, fn, ln, term, gpa):
    '''Update function to modify a student's data by ID.'''
    conn = sqlite3.connect("Students.db")
    cur = conn.cursor()
    cur.execute("UPDATE data1 SET fn=?, ln=?, term=?, gpa=? WHERE id=?", (fn, ln, term, gpa, id))
    conn.commit()
    conn.close()


def delete_data():
    '''Delete the database file and reset it.'''
    if os.path.exists("Students.db"):
        os.remove("Students.db")
    connect()


connect()
