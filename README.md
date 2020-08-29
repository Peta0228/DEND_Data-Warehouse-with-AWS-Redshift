# Purpose of database

<p>The purpose of this database is to provide foundations for analyzing user acitivies in Sparkify's new music streaming app, and hence the database is optimized for song play analysis.</p>

<p>A dataware house is created in AWS Redhsift, and data are pipelined from AWS S3. Before the pipeline can be ran, data modeling was created and testified in Redshift.</p>

# Database schema design and ETL pipeline

<p>The schema design is meant to optimize the speed for queries about user activities and song play analysis, and so the fact table is mainly composed of data about user's information, and includes `song_id`, `artist_id`, and `user_id` in order to connect with the dimension tables.</p>

<p>The ETL pipeline starts from JSON data in a S3 bucket, using AWS's Redshift functionality, the JSON files are transdered into a Redshift cluster.</p>

# Files Explanation

<p>create_tables.py: initialization of database and tables</p>

<p>sql_queries.py: provide queries for initialization and ETL</p>

<p>etl.py: extracts files from `song_data` and `log_data` in the S3 bucket, and loads them into the Redshift cluster</p>

<p>dwh.cfg: AWS account credentials for IAM, S3, and Redshift</p>


# Running the scripts

<p>To run in terminal first run `create_tables.py` to connect to the Redshift cluster and refresh tables, then run `etl.py` to build ETL to the database from JSON files in S3; </p>
