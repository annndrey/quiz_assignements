import sqlite3


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


def get_course_instructors(db, course):
    '''Return the Course number, sections
    and instructors for the given course number.'''

    # here a simple query is performed, we select three columns from the Course
    # table for a given course name
    query = '''SELECT Course, Sections, '''
    '''Name FROM Courses  WHERE Course = "%s"''' % course
    return run_query(db, query)


def get_course_time(db, course):
    '''Return the course number, ID, the date and start time of the given
    course's exam for all sections. Note there are only multiple sections
    if the course IDs are different.'''
    # to get course date and start time two tables, Courses and Time
    # are joined together and filtered by the given course name
    query = '''SELECT Courses.Course, Date, Start FROM Time INNER JOIN'''
    '''Courses ON Courses.ID == Time.ID where Courses.Course = "%s"''' % course
    return run_query(db, query)


def get_course_time_section(db, course, section):
    '''Return the course number, section,
    the date and start time of the given course's exam.'''

    # we get date and start time
    # for a given course and section by joining two tables
    # Courses and Times
    query = '''SELECT Course, Courses.ID, Date, Start FROM '''
    '''Time INNER JOIN Courses ON Courses.ID == Time.ID where '''
    '''Courses.Course = "%s" AND Courses.Sections = "%s"''' % (
        course, section)

    return run_query(db, query)


def courses_multi_instructors(db):
    '''Return the course number and instructor names for courses with more
    than one instructor. Note that this means the ID must be
    the same for each instructor.'''

    # we select the Name rows containing comma
    # because if there's a comma, there are more than one instructor
    query = '''SELECT Course, Name from Courses WHERE NAME LIKE "%,%"'''

    return run_query(db, query)


def courses_how_many_instructors(db):
    '''Return the course number and the number of instructors for courses with more
    than one instructor. Note that this means the ID must be
    the same for each instructor.'''

    # first we obtain all the courses with multiple instructors
    res = courses_multi_instructors(db)

    # an empty list for the result
    count_instructors = []

    # for every selected course we count the number
    # of instructors by splitting the Name column by ","
    # and calculating the resulting list length
    for r in res:
        count_instructors.append([r[0], len(r[1].split(','))])

    return count_instructors


def find_dept_courses(db, dept):

    '''Return the courses from the given department.  Use  the "LIKE"
    clause in your SQL query for the course name.'''
    # we select a course departement by filtering all the course names
    # starting with a given dept name
    query = '''SELECT Course FROM Courses WHERE Course = LIKE "''' + dept + "%"

    return run_query(db, query)


def get_locations(db, course):
    '''Return the course, section and locations
    of the exam for the given course.'''

    query = '''SELECT Courses.Course, Courses.Sections, '''
    '''Locations.Room FROM Locations INNER JOIN Courses ON '''
    '''Courses.ID == Locations.ID where Courses.Course = "%s"''' % course
    return run_query(db, query)


def check_conflicts(db, course):
    '''Return  a list of course numbers of courses
    that  have conflicts with the given course.
    A conflict is the same date and same start
    time. HINT: this may require more than one search.'''
    # First we select all the courses
    # with same date and start time
    # after that we check if the given course is in the
    # selected array

    query = '''SELECT Course FROM Courses WHERE Course '''
    '''IN (SELECT Course FROM Time INNER JOIN Courses '''
    '''ON Courses.ID == Time.ID GROUP BY Time.Date,Time.Start'''
    '''HAVING count(*) > 1) AND Courses.Course = "%s"''' % course
    return run_query(db, query)


def get_exam_info(db, course, sec=None):
    """
    Gets exam info on given course name. If a course have multiple sections,
    user can enter a section name
    """

    res = get_course_time(db, course)

    # res has multiple sections
    if len(res) > 1:
        if not sec:
            sec = raw_input(
                "There are multiple sections"
                "of Course %s. What is your section?" % course)
        res = get_course_time_section(db, course, sec)
        if len(res) == 0:
            sec = raw_input(
                "Not a valid section code, please re-enter or return to quit.")
            if not sec:
                raise SystemExit
            return get_exam_info(db, course, sec=sec)

    elif len(res) == 0:
        course = raw_input(
            "Not a valid course code, please re-enter or return to quit.")
        if not course:
            raise SystemExit
        return get_exam_info(db, course)

    return {
        "course": res[0][0],
        "section": sec,
        "date": res[0][1],
        "time": res[0][2]
        }


def print_exam_info(res):
    """ Prints formatted information on course exams """
    # checking if section info is filled
    if res["section"] is None:
        print "Course %s has exam on %s at %s." % (
            res["course"], res["date"], res["time"]
            )
    else:
        print "Course %s section %s has exam on %s at %s." % (
            res["course"], res["section"], res["date"], res["time"]
            )


def exam_info(db, course):
    """ A simple wrapper for duplicated code """

    # obtaining exam info for a given course
    res = get_exam_info(db, course)

    # printing exam info
    print_exam_info(res)


if __name__ == '__main__':
    # write your program here
    # you may assume the database has been made and has the name
    # DO NOT CHANGE THIS LINE
    db = 'exams.db'

    # add the rest of your code here
    # obtaining course name from user input
    user_course = raw_input("Please enter your course or return to quit.")

    # call the wrapping function for fetching and printing the result
    exam_info(db, user_course)

    # if course name is not defined, exit
    if not user_course:
        raise SystemExit

    # an infinite loop for let the user enter another course name
    while True:
        # if user_course is not defined, exit loop
        if not user_course:
            raise SystemExit
        else:
            # here we can enter the course name again
            user_course = raw_input(
                "Please enter the next course or return to quit.")
            if not user_course:
                raise SystemExit

            # another call for the wrapping function
            exam_info(db, user_course)
