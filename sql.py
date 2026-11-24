import sqlite3
#connecting to sqlite
connection=sqlite3.connect("student.db")
#creating a cursor object which is responsible for insert record,create table,retrieve record
cursor=connection.cursor()

#creating a table
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
"""

cursor.execute(table_info)

cursor.execute("SELECT COUNT(*) FROM STUDENT")
if cursor.fetchone()[0] == 0:

    cursor.execute("""
    INSERT INTO STUDENT VALUES
    ('Alice', 'Data Science', 'A', 85),
    ('Bob', 'Computer Science', 'B', 92),
    ('Charlie', 'Information Technology', 'A', 78),
    ('David', 'Data Science', 'B', 88),
    ('Emma', 'Computer Science', 'A', 95),
    ('Frank', 'Electronics', 'C', 72),
    ('Grace', 'Computer Science', 'B', 89),
    ('Henry', 'Information Technology', 'C', 81),
    ('Ivy', 'Data Science', 'A', 90),
    ('Jack', 'Electronics', 'B', 76);
    """)


# Display all the records
print("The inserted records are")

data = cursor.execute('''SELECT * FROM STUDENT''')

for row in data:
    print(row)

# Close the connection
connection.commit()
connection.close()