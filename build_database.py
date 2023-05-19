import sqlite3
from sqlite3 import Error
import os, json
from datetime import datetime
import pandas as pd

DATA_DIR = './The Full Plinkage/'
#DATA_DIR = './bet_archives_test/'
ERR_COUNT = 0

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_the_tables(conn):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS bets (
                                        bet_id integer PRIMARY KEY,
                                        game_name text NOT NULL,
                                        bet_date text
                                    );"""
    if conn is not None:
        create_table(conn, sql_create_table)
    else:
        print("Can't connect to database.")


def load_json_data(conn):
    game_names = set()
    files = os.listdir(DATA_DIR)
    list_of_bets = []
    for file in files:
        print(file)
        full_path = DATA_DIR + file
        with open(full_path) as f:
            data = json.load(f)
            for elem in data:
                list_of_bets.append(elem)
                ts = elem['createdAt'] / 1000
                time_stamp = datetime.utcfromtimestamp(ts)#.strftime('%Y-%m-%d %H:%M:%S')
                if 'gameName' in elem.keys():
                    execute_insert(conn, elem['id'], time_stamp, elem['createdAt'], elem['gameName'], elem['currency'], elem['amount'], elem['value'], elem['payout'], '', False, elem['type'])
                elif 'game' in elem.keys():
                    execute_insert(conn, elem['id'], time_stamp, elem['createdAt'], elem['game'], elem['currency'], elem['amount'], elem['value'], elem['payout'], '', False, elem['type'])
            f.close()

    conn.commit()
    print(ERR_COUNT)

    # pd.set_option('display.max_colwidth', None)
    # pd.set_option('display.max_columns', None)
    # df = pd.DataFrame(list_of_bets)
    # print(df.tail(1))

def execute_insert(conn, id, ts, ts_unix, name, currency, amt, val, pay, prov, bonus, cat):
    global ERR_COUNT

    try:
        conn.execute("""INSERT INTO the_bets (bet_id, bet_date, bet_date_unix, game_name, currency, bet_amt, bet_val, bet_payout, game_provider, bonus_triggered, game_category) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",(id, ts, ts_unix, name, currency, amt, val, pay, prov, bonus, cat))
    except Error as err:
        ERR_COUNT += 1

def go(in_db_name):

    conn = create_connection(in_db_name)

    load_json_data(conn)

    return conn
