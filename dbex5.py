import mysql.connector
import sys

def connectDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        port="3305",
        database="ex5"
    )
    return mydb

def addStu(cursor, stu_name):
    """

    :param cursor: db cursor
    :param stu_name: String student_name
    :return:
    """
    try:
        sql = "INSERT INTO students VALUES (null, %s)"
        val = [stu_name]
        cursor.execute(sql, val)
        mydb.commit()
    except Exception:
        print("error" + Exception)
        mydb.rollback()


def selectStudentById(cursor, stu_id):
    try:
        sql = "select * from students where stu_id = %s"
        val = [stu_id]
        cursor.execute(sql, val)
        student = cursor.fetchall()
        return True if len(student)>0 else False
    except Exception:
        print("error" + Exception)
        mydb.rollback()
        return False


def addCourse(cursor, course_name):
    """

    :param cursor: db cursor
    :param course_name: String course_name
    :return:
    """
    try:
        sql = "INSERT INTO courses VALUES (null, %s)"
        val = [course_name]
        cursor.execute(sql, val)
        mydb.commit()
    except Exception:
        print("error" + Exception)
        mydb.rollback()


def selectCourseById(cursor, c_id):
    try:
        sql = "select * from courses where c_id = %s"
        val = [c_id]
        cursor.execute(sql, val)
        course = cursor.fetchall()
        return True if len(course)>0 else False
    except Exception:
        print("error" + Exception)
        mydb.rollback()
        return False

def testStuCourseExist(cursor,s):
    stu_id = s.split(',')[0]
    course_id = s.split(',')[1]
    val = [course_id, stu_id]
    test = 'select * from stu_course where c_id=%s and stu_id=%s'
    result = []
    try:
        cursor.execute(test, val)
        result = cursor.fetchall()
    except Exception:
        print("error: mysql fails")
        mydb.rollback()
    if len(result)<1:
        return True
    else:
        return False

def enrollCourse(cursor, s):
    stu_id = s.split(',')[0]
    course_id = s.split(',')[1]
    val = [course_id, stu_id]
    if testStuCourseExist(cursor, s)==True:
        sql = "INSERT INTO stu_course VALUES (%s, %s);"
        try:
            cursor.execute(sql, val)
            mydb.commit()
            return True
        except Exception:
            print("error" + Exception)
            mydb.rollback()
    else:
        return False


def seeStuCourses(cursor, stu_id):
    result = []
    sql = "select stu_id as student_id, stu_name as student_name," \
          "c_id as course_id, c_name course_name from students join"" \
        ""stu_course using(stu_id) join courses using(c_id) "" \
        ""where stu_id = %s order by c_id;"
    val = [stu_id]
    try:
        cursor.execute(sql, val)
        result = cursor.fetchall()
    except Exception:
        print("Error: sql fails")
        mydb.rollback()
    return result


def seeCoursesStu(cursor, c_id):
    result = []
    sql = "select c_id, c_name, stu_name, stu_id from courses join " \
          "stu_course using(c_id) join students using(stu_id)" \
          "where c_id = %s order by stu_id;"
    val = [c_id]
    try:
        cursor.execute(sql, val)
        result = cursor.fetchall()
    except Exception:
        print("Error: sql fails")
        mydb.rollback()
    return result


def checkSchedule(cursor, stu_id, day):
    result = []
    sql = "select c_name, c_time, c_day from course_time " \
          "join courses using(c_id) join stu_course using (c_id) " \
          "join students using(stu_id) where stu_id = %s and c_day = %s " \
          "group by c_name order by c_id"
    val = [stu_id, day]
    try:
        cursor.execute(sql, val)
        result = cursor.fetchall()
    except Exception:
        print("Error: sql fails")
        mydb.rollback()
    return result

if __name__ == "__main__":

    mydb = connectDB()
    cursor = mydb.cursor()
    day_dic = {'Monday', 'Tuesday', 'Wednesday', 'Thursday'
               , 'Friday', 'Saturday', 'Sunday'}

    while True:
        print("----------------------\n" +
              "There are the options:\n" +
              "1. Add a student\n" +
              "2. Add a course\n" +
              "3. Student enroll class\n"
              "4. See a student's courses\n" +
              "5. See a students in a specific course\n" +
              "6. Check schedule for a student on a day\n" +
              "7. Exit program")
        tmp = input()
        if tmp == "1":
            f = False
            while f is False:
                name = input("Please input a new student's name: \r\n").strip()
                if name != "" and name != " ":
                    addStu(cursor, name)
                    f = True
        elif tmp == "2":
            f = False
            while f is False:
                name = input("Please input a new course name: \r\n").strip()
                if name != "" and name != " ":
                    addCourse(cursor, name)
                    f = True
        elif tmp == "3":
            f = False
            while f is False:
                s = input("Please input student_id and course_id (e.g 1,2):").strip()
                if s != "" and s != " " and len(s.split(','))==2:
                    if selectStudentById(cursor, s.split(',')[0])==False or selectCourseById(cursor, s.split(',')[1])==False:
                        print("Student or course doesn't exist\r\n")
                    else:
                        flag = enrollCourse(cursor, s)
                        if flag == False:
                            print("This line already exists!\r\n")
                        f = True
        elif tmp == '4':
            f = False
            while f is False:
                stu_id = input("Please input a student_id").strip()
                if stu_id != "" and stu_id != " ":
                    if selectStudentById(cursor, stu_id)==False:
                        print("Student doesn't exist\r\n")
                    else:
                        result = seeStuCourses(cursor, stu_id)
                        if len(result)<1:
                            print("This student doesn't enroll in any courses")
                        else:
                            for item in result:
                                print(item)
                        f = True
        elif tmp == "5":
            f = False
            while f is False:
                c_id = input("Please input a course_id").strip()
                if c_id != "" and c_id != " ":
                    if selectCourseById(cursor, c_id) == False:
                        print("Course doesn't exist\r\n")
                    else:
                        result = seeCoursesStu(cursor, c_id)
                        if len(result)<1:
                            print("This course doesn't have any students")
                        else:
                            for item in result:
                                print(item)
                        f = True
        elif tmp == '6':
            f = False
            while f is False:
                s = input("Please input a stu_id and a day(e.g 1,Friday)").strip()
                if s != "" and s != " " and len(s.split(',')) == 2:
                    if selectStudentById(cursor, s.split(',')[0])==False:
                        print("Student doesn't exist\r\n")
                    elif s.split(',')[1] not in day_dic:
                        print("Please input correct day format\r\n")
                    else:
                        result = checkSchedule(cursor,
                                               s.split(',')[0], s.split(',')[1])
                        if len(result)<1:
                            print('No classes on that day')
                        else:
                            for item in result:
                                print(item)
                        f = True
        elif tmp=='7':
            sys.exit(1)
        else:
            print('Please input a correct index')