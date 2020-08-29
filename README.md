# Purpose of database

<p>The purpose of this database is to provide foundations for anlayzing user acitivies in Sparkify's new music streaming app, and hence the database is optimized for song play analysis.</p>

# Database schema design and ETL pipeline

<p>The schema design is meant to optmize the speed for queries about user activities and song play analysis, and so the fact table is mianly composed of data about user's information, and includes `song_id`, `artist_id`, and `user_id` in orde to connect with the dimension tables.</p>

<p>The ETL pipeline starts from JSON data in a S3 busket, using AWS's Redshif functionality, the JSON files are transdered into a Redshift cluster.</p>

# Files Explanation

<p>`create_tables.py`: initliazaiton of database and tables</p>

<p>`sql_queries.py`: provide queries for initilization and ETL</p>

<p>`etl.py`: extracts files from `song_data` and `log_data` in the S3 bucket, and loads them into the Redshift cluster</p>

<p>'dwh.cfg': AWS account info for IAM, S3, and Redshift</p>


# Running the scripts

<p>To run in terminal first run `create_tables.py` to connect to the Redshift cluster and refresh tables, then run `etl.py` to build ETL to the database from JSON files in S3; </p>