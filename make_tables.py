# create the tables

import sqlite3


def create_location_table(db, loc_file):
    '''Locations table has format ID, Room'''

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('''DROP TABLE IF EXISTS Locations''')
    # create the table
    cur.execute('''CREATE TABLE Locations (ID TEXT UNIQUE, Room TEXT)''')

    # ADD THE rows
    rows = []
    for row in loc_file:
        row = row.replace("\r\n", "").split(",", 1)
        if len(row) == 2:
            rows.append(row)
    cur.executemany('insert into Locations values (?, ?)', rows)

    # commit and close cursor and connection
    con.commit()
    cur.close()
    con.close()


def create_course_table(db, course_file):
    '''Courses Table should be ID,Course,Section,Name'''

    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute('''DROP TABLE IF EXISTS Courses''')

    # create the table
    cur.execute(
        '''CREATE TABLE Courses (ID TEXT UNIQUE, '''
        '''Course TEXT, Sections TEXT, Name TEXT)'''
        )

    # Insert the rows
    rows = []
    for row in course_file:
        row = row.replace("\r\n", "").split(",")
        if len(row) == 4:
            rows.append(row)
    cur.executemany('insert into Courses values (?, ?, ?, ?)', rows)

    # commit and close the cursor and connection
    con.commit()
    cur.close()
    con.close()


def create_time_table(db, time_file):
    '''Time Table should be ID,Date,Start,End,Duration
    '''

    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute('''DROP TABLE IF EXISTS Time''')
    # create the table
    cur.execute(
        '''CREATE TABLE Time (ID TEXT UNIQUE, '''
        '''Date TEXT, Start TEXT, End TEXT, Duration TEXT)''')

    # insert the rows
    rows = []
    for row in time_file.readlines()[0].split("\r"):
        if not row.startswith("ID"):
            row = row.replace("\r", "")
            rows.append(row.split(","))
    cur.executemany('insert into Time values (?, ?, ?, ?, ?)', rows)

    # commit and close the cursor and connection
    con.commit()
    cur.close()
    con.close()


def run_query(db, q, args=None):
    """(str, str, tuple) -> list of tuple
        Return the results of running query q with arguments args on
        database db."""

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    # execute the query with the given args passed
    # if args is None, we have only a query
    if args is None:
        cur.execute(q)
    else:
        cur.execute(q, args)

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def check_courses(db):
    '''Return the entire Courses table '''

    return run_query(db, '''SELECT * FROM Courses''')


def check_time(db):
    '''Return the entire Time table '''

    return run_query(db, '''SELECT * FROM Time''')


def check_rooms(db):
    '''Return the entire Locations table '''

    return run_query(db, '''SELECT * FROM Locations''')


if __name__ == '__main__':

    # open the necessary files
    location_csv = open("./locations.csv", 'rb')
    time_csv = open("./time.csv", 'rb')
    courses_csv = open("./courses.csv", 'rb')
    database_name = "./exams.db"
    # create the tables
    create_course_table(database_name, courses_csv)
    create_location_table(database_name, location_csv)
    create_time_table(database_name, time_csv)
    # close the files
    location_csv.close()
    time_csv.close()
    courses_csv.close()

    raw_input("Checking courses")
    print check_courses(database_name)
    raw_input("Checking locations")
    print check_rooms(database_name)
    raw_input("Checking time")
    print check_time(database_name)
