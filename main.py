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

def main():
    global connection, cursor

    path="./register.db"
    connect(path)
    create_tables()
    read_data()

if __name__ == "__main__":
    main()
