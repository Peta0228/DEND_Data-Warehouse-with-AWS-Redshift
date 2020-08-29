import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events (artist varchar, auth varchar, firstName varchar, gender varchar, itemInSession int, lastName varchar, length float, level varchar, location varchar, method varchar, page varchar, registration float, sessionId int, song varchar, status int, ts varchar, userAgent varchar, userId varchar)
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (num_song int, artist_id varchar, artist_latitude float, artist_longitude float, artist_location varchar, artist_name varchar, song_id varchar, title varchar, duration float, year int)
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays(songplay_id int IDENTITY(0,1) PRIMARY KEY, start_time timestamp NOT NULL, user_id varchar NOT NULL, level varchar NOT NULL, song_id varchar, artist_id varchar, session_id int NOT NULL, location varchar NOT NULL, user_agent varchar NOT NULL)
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users(user_id varchar PRIMARY KEY, first_name varchar NOT NULL, last_name varchar NOT NULL, gender char NOT NULL, level varchar NOT NULL)
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs(song_id varchar PRIMARY KEY, title varchar NOT NULL, artist_id varchar NOT NULL, year int NOT NULL, duration float NOT NULL)
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists(artist_id varchar PRIMARY KEY, name varchar NOT NULL, location varchar, latitude float, longitude float)
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(start_time timestamp PRIMARY KEY, hour int NOT NULL, day int NOT NULL, week int NOT NULL, month int NOT NULL, year int NOT NULL, weekday int NOT NULL)
""")

# STAGING TABLES

staging_events_copy = ("""copy staging_events from {} credentials 'aws_iam_role={}' JSON {} region 'us-west-2';
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""copy staging_songs from {} credentials 'aws_iam_role={}' JSON 'auto' region 'us-west-2';
""").format(config['S3']['SONG_DATA'],config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) (SELECT ('1970-01-01'::date + e.ts/1000 * interval '1 second'), e.userId, e.level, s.song_id,s.artist_id, e.sessionId, e.location, e.userAgent FROM staging_events AS e JOIN staging_songs AS s ON (e.song = s.title AND e.artist = s.artist_name AND e.length = s.duration) WHERE e.page = 'NextSong')
""")

user_table_insert = ("""INSERT INTO users(user_id, first_name, last_name, gender, level) (SELECT userId, firstName, lastName, gender, level FROM staging_events WHERE staging_events.page = 'NextSong')
""")

song_table_insert = ("""INSERT INTO songs(song_id, title, artist_id, year, duration) (SELECT song_id, title, artist_id, year, duration FROM staging_songs)
""")

artist_table_insert = ("""INSERT INTO artists(artist_id, name, location, latitude, longitude) (SELECT artist_id, artist_name, artist_location, artist_latitude, artist_longitude FROM staging_songs)
""")

time_table_insert = ("""INSERT INTO time(start_time, hour, day, week, month, year, weekday) (SELECT ('1970-01-01'::date + ts/1000 * interval '1 second') as a, extract(hour from a), extract(day from a), extract(week from a), extract(month from a), extract(year from a), extract(weekday from a) FROM staging_events WHERE staging_events.page = 'NextSong')
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
