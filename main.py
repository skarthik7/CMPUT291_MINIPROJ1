import sqlite3
from venv import create
import getpass
import random
from datetime import date
connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

def create_tables():
    # watch(sid, cid, mid, duration)
    # follows(cid, pid)
    # editors(eid, pwd)

    global connection, cursor
    
    cursor.executescript('''drop table if exists editors;
                            drop table if exists follows;
                            drop table if exists watch;
                            drop table if exists sessions;
                            drop table if exists customers;
                            drop table if exists recommendations;
                            drop table if exists casts;
                            drop table if exists movies;
                            drop table if exists moviePeople;''' )

    cursor.execute('''PRAGMA foreign_keys = ON;''')

    moviePeople_query = '''
                        create table moviePeople (
                        pid		char(4),
                        name		text,
                        birthYear	int,
                        primary key (pid)
                        );
    '''

    movies_query = '''
                create table movies (
                    mid		int,
                    title		text,
                    year		int,
                    runtime	int,
                    primary key (mid)
                );
    '''

    casts_query = '''
                create table casts (
                        mid		int,
                        pid		char(4),
                        role		text,
                        primary key (mid,pid),
                        foreign key (mid) references movies,
                        foreign key (pid) references moviePeople
                );
    
    '''

    recommendations_query = '''
                    create table recommendations (
                            watched    int,
                            recommended    int,                              
                            score float,
                            primary key (watched,recommended),
                            foreign key (watched) references movies,
                            foreign key (recommended) references movies
                    );

    '''
    customers_query = '''
                    create table customers (
                            cid    char(4),
                            name text,
                            pwd    text,
                            primary key (cid)
                    );
    '''
    sessions_query = '''
                    create table sessions (
                            sid    int,
                            cid        char(4),
                            sdate        date,
                            duration    int,
                            primary key (sid,cid),
                            foreign key (cid) references customers on delete cascade
                    );

    '''


    watch_query = '''
                create table watch (
                        sid		int,
                        cid		char(4),
                        mid		int,
                        duration	int,
                        primary key (sid,cid,mid),
                        foreign key (sid,cid) references sessions,
                        foreign key (mid) references movies
                );
    '''

    follows_query = '''
                    create table follows (
                        cid		char(4),
                        pid		char(4),
                        primary key (cid,pid),
                        foreign key (cid) references customers,
                        foreign key (pid) references moviePeople
                    );
    '''

    editors_query = '''
                    create table editors (
                        eid		char(4),
                        pwd		text,
                        primary key (eid)
                    );
    '''
    
    cursor.execute(moviePeople_query)
    cursor.execute(movies_query)
    cursor.execute(casts_query)
    cursor.execute(recommendations_query)
    cursor.execute(customers_query)
    cursor.execute(sessions_query)
    cursor.execute(watch_query)
    cursor.execute(follows_query)
    cursor.execute(editors_query)
    
    print("SUCCESSFULLY CREATED TABLES")


def read_data():
    file_name = input("Database: ")
    file = open(file_name)
    file_data = file.read()
    file.close()
    #print(file_data)

    global connection, cursor
    
    insert_query = file_data
    try:
        cursor.executescript(insert_query)
        connection.commit()
    except sqlite3.Error as e:
        print(e)

    print("SUCCESSFULLY INSERTED DATA")

def query_test():
    global connection, cursor
    

    try:
        cursor.execute('SELECT * from editors') 
        data = cursor.fetchall()
        
    except sqlite3.Error as e:
        print(e)
    
    for i in range(len(data)):
        print(data[i])

    connection.commit()

def login_reg_screen():

    global connection, cursor

    print("Hello!")

    id_input = ' '
    run = 0
    while id_input[0] not in ['c','e']:
        id_input = input("ID: ")
        run+=1
        if run != 0 and id_input[0] not in ['c','e']:
            print("INVALID ID provided")
   
    pw_input = getpass.getpass("Password: ")

    if id_input[0] == 'c':
        cursor.execute('SELECT * from customers;') 
        data = cursor.fetchall()
    elif id_input[0] == 'e':
        cursor.execute('SELECT * from editors;') 
        data = cursor.fetchall()

    for sublist in data:
        if id_input == sublist[0]:
            user_type = "EXISTING USER"
            break
        else:
            user_type = "NEW USER"
    print(user_type)
    if user_type == "EXISTING USER":
        if id_input[0] == 'e':
            cursor.execute('SELECT pwd from editors WHERE eid = ?', (id_input,))
            data = cursor.fetchone()
        elif id_input[0] == 'c':
            cursor.execute('SELECT pwd from customers WHERE cid = ?', (id_input,)) 
            data = cursor.fetchone()


        if data[0] == pw_input:
            print("CORRECT PASS")
            return ["Successful", id_input]

        else:
            print('INCORRECT PASS')
            # print(data[0])
            # print(pw_input)
            return ["Not Successful", id_input]
        connection.commit()

        

    else:
        print("\nCreating NEW account.\n")
        type_input = input("Customer or Editor (enter c/e): ")
        if type_input== 'c':

            unique = False

            cursor.execute('SELECT * from customers;') 
            data = cursor.fetchall()
            all_cids = []
            for dat in data:
                all_cids.append(dat[0])
            
            while unique is False:
                new_id_input = input("cid: ")
    
                if new_id_input in all_cids:
                    user_type = "EXISTING USER"
                    print("cid is not unique.")
                    unique = False

                else:
                    unique = True
                
            name_input = input("Name: ")
            new_pw_input = getpass.getpass("password: ")
            try:
                cursor.execute('''insert into customers values (?,?,?); ''', (new_id_input,name_input,new_pw_input,)) 
                print("\nNew user account created.\nInserted to the table.\n")
            except sqlite3.Error as e:
                print(e)

        elif type_input == 'e':
            unique = False

            cursor.execute('SELECT * from editors;') 
            data = cursor.fetchall()
            all_eids = []
            for dat in data:
                all_eids.append(dat[0])

            while unique is False:
                new_id_input = input("eid: ")
    
                if new_id_input in all_eids:
                    user_type = "EXISTING USER"
                    print("eid is not unique.")
                    unique = False

                else:
                    unique = True
                
            
            new_pw_input = getpass.getpass("password: ")
            try:
                cursor.execute('''insert into editors values (?,?); ''', (new_id_input,new_pw_input,)) 
                print("\nNew user account created.\nInserted to the table.\n")
            except sqlite3.Error as e:
                print(e)
    
        return ["Successful", new_id_input]

def customer_functionality(login_status):

    global connection, cursor
    cursor.execute('SELECT name from customers WHERE cid =? ;',(login_status[1],))

    data = cursor.fetchone()

    print("\nWelcome, {}!".format(data[0]))
    connection.commit()

    if login_status[0] == "Successful":

        

        

        option = 0
        while option != 5:
            print("\nSELECT one OF THE FOLLOWING:")
            print("1. Start a session")
            print("2. Search for movies")
            print("3. End watching a movie")
            print("4. End the session")
            print("5. Exit;")
            option = int(input("\nOption: "))
    
        #print("USER {} SELECTED OPTION {}".format(login_status[1],option))
            if option == 1:
                start_session(login_status[1])
                
            elif option == 2:
                search_movies(login_status[1],option)
                
            elif option == 3:
                pass
            elif option == 4:
                pass
            elif option == 5:
                print("Thank you for using our system.")
            else:
                print("INVALID OPTION. Re-enter below.\n")

def start_session(cid):

    # OPTION 1
    global connection, cursor

    # new session
    cursor.execute('SELECT sid from sessions;')
    data = cursor.fetchall()
    sids = []
    for sid in data:
        sids.append(sid[0])
    
    sids.sort()
    
    first_sid = sids[0]
    last_sid = sids[len(sids)-1]+100


    new_random_sid = random.randint(first_sid,last_sid)

    while new_random_sid in sids:
        new_random_sid = random.randint(first_sid,last_sid)

    print("New Randomly generated SID is", new_random_sid,".\n")
    todays_date = date.today()

    cursor.execute('''insert into sessions values (?,?,?,NULL); ''', (new_random_sid,cid,todays_date))
    connection.commit()

    return

def search_movies(cid,option):
    # search for movie based on keyword
    number_of_keywords = int(input("Number of keywords: "))
    # keyword = input("Keywords: ")
    keywords = []
    for word in range(number_of_keywords):
        new_word = input("Keywords: ")
        keywords.append(new_word)
    # Shawshank Red Varun Dhawan

    print("\nKEYWORDS entered:\n")
    for k in keywords:
        print(k)
    print('\n')
    
    result = []
    data1 = []
    data2 = []
  
    for keyword in keywords:
        n_keyword = '%{}%'.format(keyword)
        cursor.execute('SELECT title, year, runtime from movies WHERE title like ?  ;',(n_keyword,))
        data1.append(cursor.fetchall())
        
        cursor.execute('SELECT m.title, m.year, m.runtime from movies m, casts c, moviePeople mp WHERE ((c.role like ? OR mp.name like ?) AND (c.pid = mp.pid AND m.mid = c.mid));',(n_keyword,n_keyword,))
        data2.append(cursor.fetchall())


    results = []
    # print(data1)
    # print(data2)
    for dat1 in data1:
        for da1 in dat1:
            
            if da1 is not []:
                results.append(da1)
    for dat2 in data2:
        for da2 in dat2:
            
            if da2 is not []:
                results.append(da2)

    number = 1
    output = 0
    
    
    if len(results) <= 5:
        for result in results:
            print("{}. {}, {}, {}".format(number,result[0],result[1],result[2]))
            number += 1
        more = False
    else:
        new_results = results[0:5]
        five = 5
        
        for result in new_results:
            print("{}. {}, {}, {}".format(number,result[0],result[1],result[2]))
            number += 1
            output += 1
        more = True
    serial = 6
    end = False
    while output < len(results):
        next_option= input("\nSelect a movie (1-{}) or more (m): ".format(serial-1))
        if next_option.lower() == 'm':
            if more is False:
                print("\nNo more movies available.")
            elif more is True:
                new_results = results[five:five+5]
                five+=5
                number = 1
                for result in new_results:
                    print("{}. {}, {}, {}".format(serial,result[0],result[1],result[2]))
                    number += 1
                    serial += 1
        elif type(option) is int:
            if int(next_option) in range (1,int(next_option)+1):
                print("Selected movie name is {}".format(results[int(next_option)-1][0]))
                details(results[int(next_option)-1][0],cid)
                end = True
            else:
                print("Invalid.")
                
    
        output+=5
    if end is not True:
        print("\nDisplayed ALL movies corresponding to keyword provided.")
        next_option= int(input("\nSelect a movie (1-{}): ".format(serial-1)))
        
        if next_option in range (1,next_option+1):
            print("Selected movie name is {}".format(results[next_option-1][0]))
            details(results[next_option-1][0],cid)
            end = True
        else:
            print("Invalid.")
        
        
        

    # dwayne p500 works
    # morgan p100 lucy issue

def details(movie_name,cust_id):
    # OPTION 2 contd. PT 2
    # print("details func.")
    # print(movie_name)

    global connection, cursor


    cursor.execute('''SELECT mp.name FROM movies m, moviePeople mp, casts c WHERE mp.pid = c.pid AND m.mid = c.mid AND m.title = ?;''',(movie_name,))

    data1 = cursor.fetchall()
    print("\nThe cast members in {} are: ".format(movie_name))
    cast_member_serial = 1
    for cm in data1:
        print('{}. {}'.format(cast_member_serial, cm[0]))
        cast_member_serial += 1
    #print(data)
    print('\n')
    cursor.execute('''SELECT COUNT(c.cid) FROM customers c, watch w, movies m WHERE c.cid = w.cid AND m.mid = w.mid AND m.title = ?''',(movie_name,))
    data2 = cursor.fetchall()
    print("The number of customers who watched this movie is: {}\n".format(data2[0][0]))

    print("1. Select a cast member and follow them.")
    print("2. Start watching the movie.")

    choice = int(input("Choice: "))
    if choice == 1:
        cast_member_choice = int(input("Cast member choice:"))
        # print(data1[cast_member_choice-1][0])
        # print(cust_id)

        cursor.execute('''SELECT pid from moviePeople where name = ?''',(data1[cast_member_choice-1][0],))

        mp_pid = cursor.fetchall()

        # cursor.execute('''INSERT into follows values ?, ?;''',(cust_id,mp_pid,))
        try:
            #cursor.execute("INSERT INTO follows (cid, pid) VALUES "+ "({}, {});".format(str(cust_id),mp_pid[0][0]))
            cursor.execute("""
                    INSERT INTO follows(cid,pid)
                    VALUES (?,?)
            """, (cust_id,mp_pid[0][0]))
            print("You have followed {}.".format(data1[cast_member_choice-1][0]))

        except sqlite3.Error as e:
            print("You already follow {}.".format(data1[cast_member_choice-1][0]))
    
    elif choice == 2:
        print("\nYou chose to watch the movie {}.".format(movie_name))
    

        connection.commit()


def main():
    global connection, cursor

    path="./register.db"
    connect(path)
    create_tables()
    read_data()

    #query_test()

    login_status = login_reg_screen()
    if login_status[0] == "Successful":
        customer_functionality(login_status)
    # customer_functionality(["Successful",'c950'])
    
    #query_test()

if __name__ == "__main__":
    main()


    # prj-test.db
    # a2-test-data.db
