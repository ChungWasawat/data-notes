# Free Data Engineer Bootcamp from Zach

source: [The ultimate YouTube DE boot camp](https://github.com/DataExpert-io/data-engineer-handbook/blob/main/bootcamp/introduction.md)

## Lecture 1
### Fact Data Modeling
Facts are something that actually happened or occurred e.g. app logs of users, a transaction of some activitie so they are immutable (unchangable) and often used in aggregations unlike dimensional data that is often used in filtering, grouping or giving context for facts data

Fact modeling is hard because
1. has 10x-100x volume than dimension data e.g. 1 user can create many activities 
2. require a lof of context (dimensional data) for effective analysis
3. without context, duplicate data in facts are way more common than in dimension

Normalization vs Denormalization
- Normalization is best for small data to deduplicate data but for large data required many resources to join data
- Denormalization always brings some dimensional attributes so it is quicker for analysis (less join) but requires large storage instead

**Don't count raw logs as fact data because raw logs doesn't have proper format for analysis and might have duplicate problem**

--old--
Before start doing something, need to know your consumer to set goals for what you are doing
- data that is easy to query, not many complex data types for data scientists, data analysts
- data that is probably harder, compact for other data engineers (nested query is stll fine)
- cleaned and well-formatted data for specific ml models
- data for creating charts

#### OLTP vs OLAP vs Master data
- OLTP: optimizes for low-latency, low-volume queries
    - normalized database for web/ mobile app
- OLAP: optimizes for large-volume, groupby queries, minimizes joins
    - denormalised data in data warehouse
- Master data: optimizes for completeness of entity definitions, deduplicated, normalized 

***OLTP and OLAP is a continuum***

Production database snapshots (many tables) -> Master data (have a table that collects all important data, still have others) -> OLAP (a table for DS or DA) -> Metrics (charts that show aggregated values)

***Example***
- Cumulative table design
    - table that hold historical data as well as current data
    - core components
        - yesterday dataframe and today one
        - full outer join the two tables
        - coalesce null values to choose only users who have been active since yesterday
        - hang onto all of history
    - usage
        - growth analytics (dimension table of all users -> being used by all downstream consumers)
        - state transition tracking ( yesterday-used/ today-miss -> churn, yesterday-missed/ today-use -> resurrected)
    - diagram
        - yesterday + today -(full outer join)-> coalesce ids and unchanging dimensions, compute cumulative metrics (days since x), combine arrays and changing values -> cumulated output
    - strengths
        - historical analysis without shuffle data (select data from a table without using join)
        - easy transition analysis for checking who is currently active
    - drawbacks
        - only be backfilled sequentially (not able to backfill in parallel)
        - handling PII (Personally identifiable information) can be a mess as another table is needed to check if users delete their account or is inactive for too long

#### Compactness vs Usability
- the most usable tables: 
    - no complex data types, easy to be manipulated with where and group by
    - majority of consumers are less technical
- the most compact tables: 
    - compressed to be as small as possible,  need to be decoded before use (not suitable for basic features like calendar as network I/O overhead and a waste of decoding time)
    - minimize data size as much as possible for a large number of users
    - online systems where latency and data volume matter a lot for technical consumers
- the middle group tables: 
    - use complex data types (array, map, struct), making querying trickier but smaller in size
    - upstream staging or master data for other data engineers 

#### Struct vs Array vs Map
- Struct (a table inside of a table)
    - **Keys are rigidly defined**, compression is good
    - Values can be any type
- Map
    - Keys are loosely defined, compression is okay -> flexible
    - Values all have to be the same type
- Array
    - Ordinal (a ordered list)
    - List of values that all have to be the same (e.g. array of string, array or map/ struct, etc)

A diaster from denormalizing a compressed data (temporal dimension) that would need to join other dimensions with spark shuffle is a messy order of compressed data

### Lab 
```
-- postgresql
-- create struct
create type struct_name as (
    data1 integer,
    data2 real
)
-- create enum 
create type enum_name as enum('high', 'medium', 'low')
-- create new cumulative table with the struct
create table cumulative_table (
    id integer,
    data1 integer,
    data2 text,
    struct_name struct_type[] (struct_name can be struct_type)
    primary key(id, data1)
) 
-- insert data into cumulative table 
with yesterday as (
    select * from yesterday_table
    where current_date = 'yesterday'
),
    today as (
    select * from today_table
    where date = 'today'
    )
-- case 1 no yesterday data but have today data, case 2 have both data, case 3 no today data but have yesterday data
-- double colon = cast in postgresql
insert into cumulative_table
select 
    coalesce(t.data1, y.data1) as data1,
    coalesce(t.data2, y.data2) as data2,
    coalesce(t.data3, y.data3) as data3,
    case when y.struct_name is null
    	then array[row(
    		t.data_in_struct1,
    		t.data_in_struct2
    	)::struct_type]
    when t.date is not null
        then y.struct_name || array[row(
     		t.data_in_struct1,
    		t.data_in_struct2
    	)::struct_type]
    else y.struct_name
    end as struct_name
    coalesce( t.date, y.current_date +1) as current_date
from today t full outer join yesterday y 
    on t.data1 = y.data1

-- unnest array
with unnested as (
select data1,
-- split array into rows of the struct
    unnest(struct_name::struct_type) as struct_name
from cumulative_table
where date = 'specific date' and data1 = 'abc'
)
-- split struct into columns 
select data1, (struct_name::struct_type).*
from unnested

-- slicing index of array (array_name is struct_name)
select data1,
    (array_name[1]::struct_type).data_in_struct1 --first item in array
    (array_name[cardinality(array_name)]::struct_type).data_in_struct1 --last item in array
-- benefits from array is faster than group by
-- normal way: need group by to find min, max of the same data1 
```
