import mysql.connector

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


def enrollCourse(cursor, s):
    stu_id = s.split(',')[0]
    course_id = s.split(',')[1]
    sql = "INSERT INTO stu_course VALUES (%s, %s)"
    val = [course_id, stu_id]
    try:
        cursor.execute(sql, val)
        mydb.commit()
    except Exception:
        print("error" + Exception)
        mydb.rollback()


if __name__ == "__main__":

    mydb = connectDB()
    cursor = mydb.cursor()


    print("----------------------\n" +
          "There are the options:\n" +
          "1. Add a student\n" +
          "2. Add a course\n" +
          "3. Student enroll class\n")
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
                    enrollCourse(cursor, s)
                    f = True



