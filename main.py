import sqlite3
from venv import create


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
        cursor.execute('SELECT * from customers') 
        data = cursor.fetchall()
        
    except sqlite3.Error as e:
        print(e)
    
    for i in range(len(data)):
        print(data[i])

    connection.commit()

def login_screen():

    global connection, cursor

    print("Hello!")

    id_input = ' '
    run = 0
    while id_input[0] not in ['c','e']:
        id_input = input("ID: ")
        run+=1
        if run != 0 and id_input[0] not in ['c','e']:
            print("INVALID ID provided")
   
    pw_input = input("Password: ")

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
        else:
            print('INCORRECT PASS')

        connection.commit()

    else:
        print("\nCreating NEW account.\n")
        if id_input[0] == 'c':

            unique = False

            cursor.execute('SELECT * from customers;') 
            data = cursor.fetchall()
            all_cids = []
            for dat in data:
                all_cids.append(dat[0])
            #print(data)
            while unique is False:
                new_id_input = input("cid: ")

               
                    
                if new_id_input in all_cids:
                    user_type = "EXISTING USER"
                    print("cid is not unique.")
                    unique = False

                else:
                    unique = True
                        
                   





                
            name_input = input("Name: ")
            new_pw_input = input("password: ")
            cursor.execute('''insert into customers values ('?', '?','?'); ''', (new_id_input,name_input,new_pw_input,)) 

def main():
    global connection, cursor

    path="./register.db"
    connect(path)
    create_tables()
    read_data()

    #query_test()

    login_screen()

if __name__ == "__main__":
    main()


    # prj-test.db
    # a2-test-data.db
