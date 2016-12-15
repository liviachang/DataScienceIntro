# Introduction for PostgresSQL

## Postgres

```bash
## Create database "my_database"
psql
drop database if exists my_database;
create database my_database;
\q

## list all databases
psql
\l
## or (if default database "postgres" exists)
psql -l 

## after creating an empty tables, load the data to my_database
psql -f data.sql my_database

## connect to the database and access data
psql my_database
## or
psql
\connect my_database

## list all tables
\d
## get info of my_table
\d my_table 
```


## Psycopg2 (Python + PostgresSQL)

### Install psycopg2
```bash
conda install psycopg2
```

### Basic sample code for psycopg2
```python
## connect to the default database "postgres" via psycopg2
import psycopg2 as pg
conn = pg.connect(dbname='postgres', user='liviachang', host='localhost')
conn.autocommit = True
cur = conn.cursor() ## create a cursor
cur.execute('drop database if exists my_database;') ## drop and re-create my_database
cur.execute('create database my_database;')
## close the cursor/connection
cur.close()
conn.commit()
conn.close()

## connect to "my_database"
conn = pg.connect(dbname='my_database', user='liviachang', host='localhost')
conn.autocommit = True
cur = conn.cursor() ## create a cursor

## create a table "my_table"
query_create = '''
  create table my_table (
    userid integer,
    time timestamp,
    type varchar(10)
  );
  '''
cur.execute(query_create)
conn.commit()

## insert data
query_insert = '''
  copy my_table 
  from '/Users/liviachang/Galvanize/ds_intro/data/psql_data01.csv'
  delimiter ','
  csv;
  '''
cur.execute(query_insert)
conn.commit()

## run queries
cur.execute('select count(*) from my_table;')
cur.fetchall()

```

### Advanced sample code for psycopg2
#### Dynamic Queries
```python
import os
query = '''
  copy my_table from '{filename}'
  delimiter ','
  csv;
  '''
data_dir = '/Users/liviachang/Galvanize/ds_intro/data/'

for fn in os.listdir(data_dir):
  if (fn.endswith('.csv')) and (fn!='psql_data01.csv'):
    cur_query = query.format(filename=data_dir+fn)
    cur.execute(cur_query)
    print '{} inserted into table my_table'.format(fn)
```
