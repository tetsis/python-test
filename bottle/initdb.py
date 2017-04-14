#import psycopg2.extras
import psycopg2

if __name__ == '__main__':
    conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=one_night_zinrou user=one_night_zinrou password=one_night_zinrou")
    dict_cur = conn.cursor()

    dict_cur.execute("DROP TABLE IF EXISTS player")
    dict_cur.execute("DROP TABLE IF EXISTS village")
    conn.commit()

    dict_cur.execute("CREATE TABLE village (name varchar(255) PRIMARY KEY, password varchar(255))")
    conn.commit()

    dict_cur.execute("CREATE TABLE player (name varchar(255) NOT NULL, password varchar(1023), village_name varchar(255) REFERENCES village(name), session_id varchar(1023))")
    conn.commit()

    dict_cur.close()
    conn.close()
