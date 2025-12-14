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
    - Databricks allows to directly run notebook in production so it is kinda dangerous so should connect Databricks with Github for two things below to minimize damage from bad changes
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


## Lab 3

