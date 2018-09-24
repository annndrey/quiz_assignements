# importing required module to work with database
import sqlite3


def run_query(db, q, args=None):
    """(str, str, tuple) -> list of tuple
    Return the results of running query q with arguments args on
    database db.
    """

    # connect to the database and create the cursor
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    if args is None:
        cur.execute(q)
    else:
        cur.execute(q, args)

    # fetching all the results at once
    results = cur.fetchall()

    # closing database connection
    cur.close()
    conn.close()

    # return the obtained results

    return results


def get_course_instructors(db, course):
    """Return the Course number, sections
    and instructors for the given course number."""

    # Here we make a query to select course,
    # section and instructor name from
    # the courses table for the given course
    query = """SELECT Course, Sections, Name"""
    """ FROM Courses  WHERE Course = '%s'""" % course

    return run_query(db, query)


def get_course_time(db, course):
    """Return the course number, ID, the date and start time of the given
    course's exam for all sections. Note there are only
    multiple sections if the course IDs are different."""

    # here we are making the query to get the course time
    # we have to join two tables and select
    # respective fields for a given course
    query = """SELECT Courses.Course, Date, Start """
    """FROM Time INNER JOIN Courses ON Courses.ID == Time.ID """
    """where Courses.Course = '%s'""" % course

    return run_query(db, query)


def get_course_time_section(db, course, section):
    """Return the course number, section, the date
    and start time of the given course's exam."""

    # to get the date and start time
    # for a given course and section
    # we have to join courses and
    # time tables and specify course and section names
    query = """SELECT Course, Courses.Sections, Date, Start"""
    """FROM Time INNER JOIN Courses ON Courses.ID == Time.ID"""
    """ where Courses.Course = '%s' AND Courses.Sections = '%s'""" % (
        course, section)

    return run_query(db, query)


def courses_multi_instructors(db):
    """Return the course number and instructor names
    for courses with more than one instructor. Note that this
    means the ID must be the same for each instructor."""

    # to find the rows with more than one instructor per course
    # we have to find the ones with a comma in the instructor name column
    query = """SELECT Course, Name from Courses WHERE NAME LIKE '%,%'"""

    return run_query(db, query)


def courses_how_many_instructors(db):
    """Return the course number and the number of instructors for courses with more
    than one instructor. Note that this means the ID must be
    the same for each instructor."""

    # to get the instructors count first
    # we select all the multiinstructors rows
    multiinstr = courses_multi_instructors(db)

    # and here we create a list of lists,
    # where the first element is the course number
    # and the second is the number of instructors
    instr_count = [[i[0], len(i[1].split(','))] for i in multiinstr]

    return instr_count


def find_dept_courses(db, dep):
    """Return the courses from the given department.  Use  the "LIKE"
    clause in your SQL query for the course name."""

    # we create a query to select all the courses
    # starting with a given sequence
    # where the sequence is the department name
    query = """SELECT Course FROM Courses"""
    """ WHERE Course = LIKE '""" + dep + "%'"

    return run_query(db, query)


def get_locations(db, course):
    """Return the course, section and locations
    of the exam for the given course."""

    # to get course name, course section and course
    # locations we have to join two tables, courses and locations
    query = """SELECT Courses.Course, Courses.Sections, Locations.Room"""
    """ FROM Locations INNER JOIN Courses ON Courses.ID == Locations.ID"""
    """ where Course.Course = '%s'""" % course

    return run_query(db, query)


def check_conflicts(db, course):
    """Return  a list of course numbers of courses that have conflicts
    with the given course. A conflict is the same date and same
    start time. HINT: this may require more than one search."""

    # to get all the course numbers that have
    # same date and time for the given course
    # we select all the courses with duplicated dates and times
    # and check if the given course is between them

    query = """SELECT Course FROM Courses WHERE Course IN"""
    """ (SELECT Course FROM Time INNER JOIN Courses ON Courses.ID == Time.ID"""
    """ GROUP BY Time.Date,Time.Start HAVING count(*) > 1) AND"""
    """ Courses.Course = '%s' """ % course

    return run_query(db, query)


def print_course_info(res):
    """ Prints information on course name, date and section """

    # checking if section info is filled
    if res["section"] is None:
        print "Course %s has exam on %s at %s." % (
            res["course"], res["date"], res["time"]
            )
    else:
        print "Course %s section %s has exam on %s at %s." % (
            res["course"], res["section"], res["date"], res["time"]
            )


def get_course_info(db, course, section=None):
    """
    A function to obtain course name, course section and course time
    If section name is not given, we just select the course. It is made for
    the cases when there's more than one section per course
    """
    # get course data
    res = get_course_time(db, course)

    # if the result has more than one row, so there's more than one section
    if len(res) > 1:
        # if section is not defined, asks user for the section name input
        if not section:
            section = raw_input(
                "There are multiple sections of"
                " Course %s. What is your section?" % course)
        # get results for course and the specified section
        res = get_course_time_section(db, course, section)
        # if there's no results, so probably the section name is invalid
        if len(res) == 0:
            section = raw_input(
                "Not a valid section code, please re-enter or return to quit.")
            # if user haven't specified the section name, quit
            if not section:
                exit()
            # else get course info again
            return get_course_info(db, course, section=section)
    # if there's no results for a given course name so the name is not correct
    # asking for another one
    elif len(res) == 0:
        course = raw_input(
            "Not a valid course code, please re-enter or return to quit.")
        # if the name is not specified, leave
        if not course:
            exit()
        #
        return get_course_info(db, course)
    # here we create a dictionnary for the results
    return {
        "course": res[0][0],
        "section": sec,
        "date": res[0][1],
        "time": res[0][2]
        }


def course_data(db, course):
    """ This is a function to store two functions
    that fetch and print course information"""
    res = get_course_info(db, course)
    print_course_info(res)


if __name__ == '__main__':
    # write your program here
    # you may assume the database has been made and has the name
    # DO NOT CHANGE THIS LINE
    db = 'exams.db'

    # add the rest of your code here
    # get the course name from user input
    course = raw_input("Please enter your course or return to quit.")

    # stop the app if there's course name given
    if len(course) == 0:
        exit()

    # call the wrapping function for fetching and printing the result
    course_data(db, course)

    # here we add the infinite loop to let user get another course info
    while True:
        # if user_course is not defined, exit loop
        if not course:
            exit()

        else:
            # here we can enter the course name again
            course = raw_input(
                "Please enter the next course or return to quit.")

            if not course:
                exit()

            # prints course info here
            course_data(db, course)
