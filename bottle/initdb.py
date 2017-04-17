#import psycopg2.extras
import psycopg2

if __name__ == '__main__':
    conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=one_night_zinrou user=one_night_zinrou password=one_night_zinrou")
    dict_cur = conn.cursor()

    dict_cur.execute("DROP TABLE IF EXISTS player")
    dict_cur.execute("DROP TABLE IF EXISTS village")
    dict_cur.execute("DROP TABLE IF EXISTS position")
    dict_cur.execute("DROP TABLE IF EXISTS state")
    conn.commit()

    dict_cur.execute("CREATE TABLE state (id serial PRIMARY KEY, state varchar(23))")
    dict_cur.execute("INSERT INTO state (state) VALUES (%s)", ('waiting',))
    dict_cur.execute("INSERT INTO state (state) VALUES (%s)", ('action',))
    dict_cur.execute("INSERT INTO state (state) VALUES (%s)", ('notification',))
    dict_cur.execute("INSERT INTO state (state) VALUES (%s)", ('night',))
    dict_cur.execute("INSERT INTO state (state) VALUES (%s)", ('daytime',))
    dict_cur.execute("INSERT INTO state (state) VALUES (%s)", ('selection',))
    dict_cur.execute("INSERT INTO state (state) VALUES (%s)", ('execution',))
    dict_cur.execute("INSERT INTO state (state) VALUES (%s)", ('result',))
    conn.commit()

    dict_cur.execute("CREATE TABLE position (id serial PRIMARY KEY, position varchar(23))")
    dict_cur.execute("INSERT INTO position (position) VALUES (%s)", ('villager',))
    dict_cur.execute("INSERT INTO position (position) VALUES (%s)", ('werewolf',))
    dict_cur.execute("INSERT INTO position (position) VALUES (%s)", ('fortuneteller',))
    dict_cur.execute("INSERT INTO position (position) VALUES (%s)", ('thief',))
    dict_cur.execute("INSERT INTO position (position) VALUES (%s)", ('madman',))
    dict_cur.execute("INSERT INTO position (position) VALUES (%s)", ('hanging',))
    conn.commit()

    dict_cur.execute("CREATE TABLE village (id serial PRIMARY KEY, name varchar(255) NOT NULL, password varchar(255), state int REFERENCES state(id), villager_number integer DEFAULT 0, werewolf_number integer DEFAULT 0, fortuneteller_number integer DEFAULT 0, thief_number integer DEFAULT 0, madman_number integer DEFAULT 0, hanging_number integer DEFAULT 0, talking_time integer DEFAULT 0, ending_time timestamp, field_position1 int REFERENCES position(id), field_position2 int REFERENCES position(id), winner_side int REFERENCES position(id))")
    conn.commit()

    dict_cur.execute("CREATE TABLE player (id serial PRIMARY KEY, name varchar(255) NOT NULL, password varchar(1023), village_id int REFERENCES village(id), session_id varchar(1023), point integer DEFAULT 0, earning_point integer DEFAULT 0, position int REFERENCES position(id), game_start_flag boolean DEFAULT FALSE, talks_start_flag boolean DEFAULT FALSE, talks_end_flag boolean DEFAULT FALSE, execution_flag boolean DEFAULT FALSE, result_flag boolean DEFAULT FALSE, action_flag boolean DEFAULT FALSE, winner_or_loser boolean DEFAULT FALSE, selection_player int REFERENCES player(id), hanging_player int REFERENCES player(id))")
    conn.commit()

    dict_cur.close()
    conn.close()
