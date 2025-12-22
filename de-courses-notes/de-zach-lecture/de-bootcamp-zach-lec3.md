# Free Data Engineer Bootcamp from Zach

source: [The ultimate YouTube DE boot camp](https://github.com/DataExpert-io/data-engineer-handbook/blob/main/bootcamp/introduction.md)

## Lecture 1
### Spark
+ Spark is a distributed compute framework -> parallelly process separated amount of data
+ Spark leverages RAM to provide faster process than previous iterations of distributed compute that mainly use disk (Hive-Hadoop/ Java MR)
+ Spark is storage agnostic (decoupling of storage and compute) -> allow user to choose whichever storage they want (avoid vendor lock-in)
+ However, Spark needs users that know how to use it or Company has already set other distributed processing systems

+ Spark words
  - RDD: lowest unit in Spark
  - Dataset (only Scala): best for pipelines that require unit and integration tests as a mock data can be created from schema right away
    - needs to define which columns are nullable to avoid error so it is a practice for data quality
  - DataFrame: suited for pipelines that are less likely to experience change and easy to run testing
  - Spark SQL: suited for pipelines that are used in collaboration with data scientists and can be changed quickly 

+ Spark's unit 
  - Plan: a transformation that will happen when there is a trigger (action) so it is evaluated as lazy. it can be one function or more-than-one functions
      - can use `explain()` on dataframes to see plan's details  
  - Driver: read the plan and determine how the plan should be run (start executing, how to join, how much parallelism each step needs) and assign to executor. important driver settings below
      - `spark.driver.memory`: rarely being used for complex jobs or jobs that change the plan after execution
      - `spark.driver.memoryOverheadFactor`: only used for complex jobs that might require more memory when they are executed 
      - **every driver setting doesn't need to be touched, it is very very rare**
  - Executor: worker
      - `spark.executor.memory`: determin how much memory each executor gets, if it's too low, Spark will use disk to be able to keep processing which will cause jobs to much slower
          - suggestion: when it runs out of memory, shouldn't set the number of memory to maximum number. But try experiment with lower number and gradually increase (2, 4, 6, etc) and run it for a while to check how it works in the number of memory
      - `spark.executor.cores`: how many tasks can happen on each machine (default-4 but shouldn't be more than 6) otherwise it will cause bottleneck that too many tasks running at the same time (risk to OOM-out of memory)
      - `spark.executor.memoryOverheadFactor`: what % of memory should an executor use for non-heap related tasks (~10%). For jobs with lots of UDFs (?) and complexity (join & union), may need to bump this up

+ Types of JOINs in Spark (similar wiht ones in lecture2)
  - Shuffle sort-merge Join: default join
      - works when both sides of the join are large (<10 TBs)
  - Broadcast Hash Join: a join without shuffle (because smaller table will be transfered to every node)
      - works well when one side of the join is small
      - `spark.sql.autoBroadcastJoinThreshold` default-10MB but >1GB may give weird memory problem 
  - Bucket Join: a join without shuffle (because data is partitioned and it can finish the process within the nodes)
      - a number of bucket must be on Power of 2 (2, 4, 8, 16, 32)
      - don't set too many buckets for small data bacause some buckets might be empty
      - more efficient if there are multiple JOINs or aggregations downstream
      - In initial state on Presto, if a number of buckets is less than 16, the process will be slow
**Spark's Join can't solve all problems so in some case, might ask upstream users to fix data or log data?**
 
+ Shuffle
  - Map-Reduce
      - Stage 1: Map-normal process like arithmetic or anything else that doesn't need other rows/ data to compute
      - Stage 2: Reduce-a process that need other rows like `Group By` / `Order By` / aggregate functions
  - RDD isn't used generally as all commands built on top of RDD e.g. `spark.sql.shuffle.partitions`, `spark.default.parallelism`

+ Skewness
  - it happens when data in some partition is more than another because there are more actions or anything (like celebrities have more data than normal users)
  - Data Science can help in skewness identification (i.e. boxplot)
  - How to solve it with Spark
      - Adaptive query execution (job running will be slower than normal execution):
        1. Spark version 3+
        2. set `spark.sql.adaptive.enabled` = `True` **beware of setting to be True all the time, slowness can cause running job more expensive**
      - Salting the Group By for Spark version less than 3
        1. `Group By` a random number -> aggregate + `Group by` again. **data must be additive**
        2. be careful with `AVG` - break it into `SUM` and `COUNT` and divide
           ```
           df.withColumn("salt_random_column", (rand * n ).cast(IntegerType))
               .groupBy(groupByFields, "salt_random_column")
               .agg(aggFields)
               .groupBy(groupByFields)
               .agg(aggFields)
           ```
      - Filter out outliers and create a dedicated pipeline for them

+ Spark on Databricks vs regular Spark
  - suggestion: Even though Databricks allows to use Spark as notebooks, code is more proper in production as testing (e.g. Unit testing) can be done with code
    - Notebooks might be used when non-tech people are invited to collaborate in the project
! attach image ...

+ Where Spark can read data from
  - Data Lake: Delta Lake, Apache Iceberg, Hive metastore
  - RDBMS: Postgres, Oracle
  - API: -turn REST API into data **be careful about memory (Driver) when processing many APIs or parallelly processing API**
  - a flat file: CSV, JSON

**Spark output almost always be partitioned on execution date**

## Lab 1


## Lecture 2

+ Spark Server vs Spark Notebooks
  - Server (submit via Spark CLI or `spark-submit`
    - run new session every time a new jar file comes in so cache will be cleared automaticallly after job has been done
    - nice for testing
  - Notebook
    - before job starts running, need to have a Notebook session stay live, then need to terminate after job has been done
    - Databricks allows to directly run notebook in production so it is kinda dangerous so should connect Databricks with Github for version control as two things below to minimize damage from bad changes
      1. Pull Request review process for every change
      2. CI/CD check
+ Caching and Temporary views
  - Temporary views (like CTE in SQL)
    - Always get recomputed unless cached in memory
  - Caching (similar to materialized views in SQL)
    - store pre-computed values for reuse
    - it stays partitioned so even 100GB data can be cached and broken into small chunks for many nodes
    - Storage levels
      - Memory only
      - Disk only (not recommend to use this option in Dataframe caching but it's okay to use for actual schema)
      - Memory and Disk -default
    - Caching only is good if it fits into memory otherwise there might be a chance to miss some staging table in pipeline
    - For Notebooks, call `unpersist` state when job has been done otherwise the cached data will reduce available memory
+ Broadcast Join optimization
  - like in lecture2, it prevents Shuffle
  - can set threshold with `spark.sql.autoBroadcastJoinThreshold`
    - default small size of instrutor is 10MB, so this setting can help in size increasing
  - alternative is to use broatcast dataframe, it will work the same. moreover, it is explicit in code so next person can know the intent for the code block
+ UDFs (user-defined function)
  - allow to do complex process
  - for PySpark, it needs to serialize and deserialize multiple times between Python and Java/Scala, causing performance slower but Apache Arrow helps to optimize PySpark UDFs to become more inline with Scala Spark UDFs
    - but for user-defined aggregating functions, the problem still persists
  - Dataset API in Scala Spark performs faster as no serialization and deserialization steps
+ Spark tuning
  - Executor memory
    - needs to adjust to actual usage, don't just set to maximum (16GB)
  - Driver memory
    - the same with executor memory
    - only needs to be bumped up if:
      - call `df.collect()`
      - have a very complex job
  - Shuffle partitions
    - default is 200
    - suggestion: should aim for 100MB per partition but it can increase or decrease up to 50% (50MB, 150MB) depends on memory, I/O, network of environment
  - Adaptive Query Execution (AQE)
    - helps with skewed datasets but wasteful for data isn't skewed
+ Parquet files
  - run-length encoding for powerful compression, better for properly-sorted data
  - suggestion
    - don't use global `.sort()` as it needs to shuffle
    - use `.sortWithinPartitions` because it is parallelizable
        
## Lab 2


## Lecture 3
### Where to catch quality bugs
#### In development - best case
1. how to catch bugs during development phase
   - unit test for every function
     - add unit tests of pipelines in CI/CD so others can see and fix although they don't know or understand about pipelines
   - integration test for
   - linter: make code more readable and easier to spot bugs - coding standard for a team
#### In production, but not showing up in tables - still okay
+ 2 types of the problem in this state
  - error from staging state to production and the audit failed before deployment
  - false positive when in production
+ how to catch bugs in production
  - use write-audit-publish pattern
    - replicate staging table to be the same with production table so quality check can be done there and if it passes, then it's ready for production
#### In production, in production tables - worst choice
- data users can notice whether it's immediate or after deployment for a while

**Software engineering has higher quality standards than data engineering**
- Reason
  - Impact from application failed and pipeline failed is different because frontend part is the main business function
    - however,
      * data delays can impact machine learning's effectiveness for the model that needs streaming data or latest data
      * data quality can impact result of experimentation (e.g. A/B testing)
  - Test-driven development and behaviour-driven development are newer in data engineering
  - Background of data engineers is more diverse

**tradeoff between busines velocity and sustainability**
- business wants answers fast but engineers don't want to waste their resources to fix bugs
- it depends on team leader and culture
- but sustainability is more preferable

**Data Engineering capability standard**
- Latency: choose the right latency for streaming and microbatch pipelines
- Quality: apply best practices and frameworks (tools like Great Expectations, Amazon DQ, Chispa to show which is error)
- Completeness: practise how to communicate with domain experts to get the right schema or architecture
- Ease-of-access and usability: create data products (e.g. built-in sql, powerful dashboard, read-and-write API) and proper data modeling 

**Mindset to have for better engineering**
- create more readable codeing for others
- aware of cases that might cause silent failure
- create alerts of exceptions for debug logs and do testing & CI/CD
- DRY (don't repeat yourself) to avoid encapsulation like avoid hard-coding or create a source of truth and YAGNI (You aren't gonna need it) to create only necessary things in the first go
- design documents is the best for future redesigning or troubleshooting
- care about efficiency: data structures and algorithms, how each tools do join and shuffle

## Lab 3
### how to set files up for unit test with pytest
directory1   
-- function   
---- __init__.py   
---- function1.py   
-- tests   
---- __init__.py   
---- test_function1.py   

1. create py file to do unit testing: main() and functions to test
2. create py file to test by import the above file
   - create function with test in front like test_function1()
   - create fake data to test: start with namedtuple for table's schema
   - create actual output that is what is returned from the imported function
   - create expected output for the fake input with namedtuple and values
     - may need to convert the output to dataframe or anything to simulate what will happen in production
   - use assert() to compare actual output and expected output
3. what to test
   - deplicate case
   -   d
4. run pytest at directory1-level


