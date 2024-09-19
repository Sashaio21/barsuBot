import psycopg2
host = "localhost"
user = "postgres"
password = "qazwsxedc"
db_name = "DataStudents"


def AvailabilityUser(idUsers):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        query = f"""SELECT id 
        FROM dataforrasp
        WHERE id = {idUsers}"""
        with connection.cursor() as cursor:
            cursor.execute(
                query
            )
            if cursor.fetchone() == None:
                return None
            else:
                return "bubs"
    except Exception as ex:
        print("Error ", ex)
    finally:
        if connection:
            connection.close
            # print("final - AvailabilityUser")

def createRecord (idUsers ,faculty, speciality, group, who, nameTeacher = "-"):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        if who == "student":
            query = f"""INSERT INTO dataforrasp (id, faculty, speciality, grouprasp, who_you) 
            VALUES ({int(idUsers)} ,'{str(faculty).replace(' ', '_')}', '{str(speciality).replace(' ', '_')}', '{str(group).replace(' ', '_')}', '{who.replace(' ', '_')}')"""
        else:
            query = f"""INSERT INTO dataforrasp (id, "nameTeacher", who_you) 
            VALUES ({int(idUsers)} , '{nameTeacher.replace(' ', '_')}' , '{who.replace(' ', '_')}')"""
       
        with connection.cursor() as cursor:
            cursor.execute(
                query
            )
    except Exception as ex:
        print("Error ", ex)
    finally:
        if connection:
            connection.close
            # print("final - createRecord")

def getData(idUsers):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        query = f"""SELECT id, faculty, speciality, grouprasp, "nameTeacher", who_you
        from dataforrasp
        WHERE id = {idUsers};"""
        with connection.cursor() as cursor:
            cursor.execute(
                query
            )
            # print(cursor.fetchone())
            return list(cursor.fetchone())
    except Exception as ex:
        print("Error ", ex)
    finally:
        if connection:
            connection.close
            # print("final - getData")


def deleteRecord(idUsers):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        query = f"""DELETE
        from dataforrasp
        WHERE id = {idUsers};"""
        with connection.cursor() as cursor:
            cursor.execute(
                query
            )
    except Exception as ex:
        print("Error ", ex)
    finally:
        if connection:
            connection.close
            # print("final - deleteRecord")