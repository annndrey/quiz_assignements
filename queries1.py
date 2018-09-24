import sqlite3


def run_query(db, q, args=None):
    """(str, str, tuple) -> list of tuple
    Return the results of running query q with arguments args on
    database db.
    """
    # create db connection and db cursor
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # execute the query with the given args passed
    # if args is None, we have only a query
    if args is None:
        cur.execute(q)
    else:
        cur.execute(q, args)
    # fetching the results
    results = cur.fetchall()
    # closing connection and cursor
    cur.close()
    conn.close()

    return results


def get_course_instructors(db, course):
    '''Return the Course number, sections
    and instructors for the given course number.'''

    # in this query we select course name,
    # sections and instructor name for a given course
    query = '''SELECT Course, Sections, Name '''
    '''FROM Courses  WHERE Course = "%s"''' % course

    return run_query(db, query)


def get_course_time(db, course):
    '''Return the course number, ID,
    the date and start time of the given
    course's exam for all sections.
    Note there are only multiple sections
    if the course IDs are different.'''

    # to get the course time we have to join two
    # tables and select respective fields for a given course
    query = '''SELECT Courses.Course, Date, Start '''
    '''FROM Time INNER JOIN Courses ON Courses.ID == Time.ID'''
    ''' where Courses.Course = "%s"''' % course

    return run_query(db, query)


def get_course_time_section(db, course, section):
    '''Return the course number, section, the date
    and start time of the given course's exam.'''

    # to get course time for a given course and
    # section we have to join courses and
    # time tables and specify course and section names
    query = '''SELECT Course, Courses.ID, Date, Start FROM Time'''
    '''INNER JOIN Courses ON Courses.ID == Time.ID '''
    '''where Courses.Course = "%s" AND Courses.Sections = "%s"''' % (
        course, section)

    return run_query(db, query)


def courses_multi_instructors(db):
    '''Return the course number and instructor names for courses with more
    than one instructor. Note that this means the ID must be
    the same for each instructor.'''

    # if the name column contains comma,
    # then there's more than one instructor there.
    # so we have to select these rows
    query = '''SELECT Course, Name from Courses WHERE NAME LIKE "%,%"'''

    return run_query(db, query)


def courses_how_many_instructors(db):
    '''Return the course number and the number
    of instructors for courses with more
    than one instructor. Note that this means the ID must be
    the same for each instructor.'''

    # to calculate the number of instructors first we have to obtain
    # all the records with more than one instructor
    res = courses_multi_instructors(db)

    instructors = []

    # for every row in the result we count the number of instructors
    # by splitting name value by comma
    # and calculating the resulting list length
    for r in res:
        instructors.append([r[0], len(r[1].split(','))])

    return instructors


def find_dept_courses(db, dept):
    '''Return the courses from the given department.  Use  the "LIKE"
    clause in your SQL query for the course name.'''

    # to get all the courses from a given departement we have to select
    # all the courses which name starts with a departement name
    query = '''SELECT Course FROM Courses WHERE Course = LIKE "''' + dept + "%"

    return run_query(db, query)


def get_locations(db, course):
    '''Return the course, section and
    locations of the exam for the given course.'''

    # here we join two tables again,
    # Courses and Locations and select respective columns
    query = '''SELECT Courses.Course, Courses.Sections,'''
    ''' Locations.Room FROM Locations INNER JOIN Courses'''
    ''' ON Courses.ID == Locations.ID where Course.Course = "%s"''' % course
    return run_query(db, query)


def check_conflicts(db, course):
    '''Return  a list of course numbers of courses
    that  have conflicts with the given course.
    A conflict is the same date and
    same start time. HINT: this may require more than one search.'''

    # we have to perform two selects here.
    # in the first one, inner select,
    # we got all the courses with more than one similar date and time
    # in the second, outer select, we check if the given course is there
    query = '''SELECT Course FROM Courses WHERE Course IN '''
    '''(SELECT Course FROM Time INNER JOIN Courses ON '''
    '''Courses.ID == Time.ID GROUP BY Time.Date,Time.Start '''
    '''HAVING count(*) > 1) AND Courses.Course = "%s"''' % course
    return run_query(db, query)


def get_exam_info(db, course, sec=None):
    """
    Gets exam info on given course name. If a course have multiple sections,
    user can enter a section name
    """

    res = get_course_time(db, course)

    if len(res) > 1:
        if not sec:
            sec = raw_input(
                "There are multiple sections of Course"
                " %s. What is your section?" % course)
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


def exam_time(db, course):
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

    # if course name is not defined, exit
    if len(user_course) == 0:
        exit()

    # call the wrapping function for fetching and printing the result
    exam_time(db, user_course)

    while True:
        # if user_course is not defined, exit loop
        if not user_course:
            exit()
        else:
            # here we can enter the course name again
            user_course = raw_input(
                "Please enter the next course or return to quit.")
            if not user_course:
                exit()

            # another call for the wrapping function
            exam_time(db, user_course)
