# SQL + PostgresSQL
This is a note of SQL syntax for me, as well as some commonly-used commands to
run postgres/psycopg2

## SQL Tips

### Tips for date/timestamps
```sql
-- mytable: userid (int), time (timestamp), type (varchar)

-- "::date" converts the timestamp to date
select time::date as login_date
from my_table
;

-- extract() or date_part(): get day of the week. 0=Sunday, 6=Saturday
-- select date_part('dow', tbl.time) as day_of_week,
select extract(dow from time) as day_of_week,
  count(tbl.time) as cnt
from my_table tbl
group by day_of_week
order by day_of_week
;

-- "> timestamp <date>": timestamp comparison 
select count(tbl.time) as cnt
from my_table tbl
where tbl.time > timestamp '2013-11-30'
;

-- date/timestamp operations
---- returns date '2001-09-08'
select distinct date '2001-09-01' + integer '7' 
from my_table;
---- returns timestamp '2001-09-01 01:00:00'
select distinct date '2001-09-01' + interval '1 hour' 
from my_table;


```

### Tips for subqueries/temp tables
```sql
with 
tmp_tbl_x as (
  select tbl_a.col1, tbl_a.col2
  from tbl_a
),
tmp_tbl_y as (
  select tbl_b.col2, tbl_b.col3
  from tbl_b
)

select tbl_c.*
from tbl_c
join tmp_tbl_x on tmp_tbl_x.col2 = tbl_c.col2
join tmp_tbl_y on tmp_tbl_y.col2 = tmp_tbl_x.col2
;

```

### Others
```sql
-- cast()
select cast(tbl.col1 as real) / tbl.col2 as my_ratio
from tbl
;

-- case/when
select 
  case when condition_1 then result_1
  case when condition_2 then result_2
  else result_3 end
from tbl
;

-- coalesce()
select p.id,
  coalesce(cnt.cnt, 0) as cnt
from person p
join login_cnt cnt on p.id = cnt.id
;

```

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

## Other Reference
- [SQL for Data Scientists](http://blog.yhat.com/posts/sql-for-data-scientists.html)
