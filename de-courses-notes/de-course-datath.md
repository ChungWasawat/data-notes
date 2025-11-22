# Data Engineer course by DataTH
## Lecture 0
<details>
  <summary><b>Data to AI Maturity</b></summary>

- a level to tell de responsibility roughly based on org's readiness, infrastruture, etc.
    - In early levels, an organization’s needs are managing data platform, data pipeline
    - In transformed org, they pay more attention to data quality if data is good to use, there is data lineage of the data ( data observability and data reliability )

1. Manual Data Drudgery
    - use manual reports
    - use spreadsheets and powerpoints to communicate status (of projects?)
    - still have disagreements on how data was processed
2. Death by Dashboards
    - only privileged employees can create reports
    - spend much money on BI tools (dashboard, report)
    - an enormous amount of irrelevant data was kept
    - multiple, inconsistent sources of truth
3. Data Tells a Story
    - multi-sources data merging
    - business results are measurable
    - more consitent view of info
    - IT and Business leadership coordinate work
    - every employee can access data
4. Emerging Intelligence
    - measurable results are consistent
    - data cross silos (of different department)
    - proactive information supportive employee (data-driven)
5. Transformed Organization
    - AI/ML is real
    - employees focus on high value work and leave low value work automated
    - recommendations are right for employee

</details>
<details>
  <summary><b>Big Data</b></summary>

### Key consideration for Big Data
1. Volume: has a big scale of data
2. Variety: has different forms of data
3. Velocity: analysis of streaming data or growth speed of data
4. Veracity: uncertainty of data
5. Value(?): create data insight to business

### Big Data Platform
#### On-premise
[Apache Hadoop Ecosystem](http://blog.newtechways.com/2017/10/apache-hadoop-ecosystem.html)
- some services of the ecosystem
    - Ingest: Kafka, Flume
    - Store: HDFS
    - Resource Manager: Yarn
    - Prep and Train: Map-Reduce
    - Analysis: Hive
#### Cloud Computing
 AWS, Azure, GCP 
- example from Azure
    - Ingest: Azure Data Factory
    - Store: Azure Data Lake Storage
    - Prep and Train: Azure Databricks
    - Analysis: Power BI

</details>
<details>
  <summary><b>Types of Data</b></summary>
  
|         | Structured Data    | Semi-Structured Data                                     | Unstructured Data           |
|---------|--------------------|----------------------------------------------------------|-----------------------------|
| format  | tabular format (fixed)    | flexible format  | no format                   |
| example | CSV, Parquet, Avro | Key-Value, Document (JSON, XML), Graph                   | file, picture, video, sound |

     
** Currently, some unstructured data can be categorized with AI assistance

</details>
<details>
  <summary><b>Types of Data Storage</b></summary>

### 1. Database

#### Definition: 
- keep structured or unstructured data that needs to write or access quickly 
- so a change in database happens all the time (OnLine Transaction Processing)
- examples: web/ mobile app, a system that stores user data

#### Key considering how to organize data (and choose suitable database?):
- Schema
- Normalization
- View
- Access Control
- Database Management System

#### Types
<U>**1. SQL database or Relational Database Management System (RDBMS)**</U>   
commonly used to store data which has a consistent schema (structured data) and describable relationship to other databases.

**Main component of SQL database**
- table 
- table schema
- relation
    - normally doesn’t support many-many relationship 
    - so it’s solved by creating a bridge table to connect via each table’s primary key as foreign keys of it
- primary key

**Database Tools**
- MySQL
- PostgreSQL (can store semi-structured like JSON)
- Oracle
- etc

! some databases can store unstructured data, but it shouldn't do   
!! so the best practice is to store the data in data lake and store file path URL in database

<U>**2. NoSQL database**</U>    
commonly stores semi-structured data

**Types of NoSQL database**
1. Document
    - MongoDB or PostgreSQL JSON
        - analogous: doc → row, collection → table
        - Mongodb offer BSON to store JSON in binary
        - PostgreSQL offer JSONB (similar to BSON)
2. Key-Value
    - Redis
        - store data in memory not on disk, it's a trade-off between read/ write speed and persistence
        - suited to store temporary data (web, mobile app) or cache
3. Wide-Column or Tabular/ Columnar
    - Cassandra
        - suited for aggregated function
    - Snowflake
        - a SQL-like database
        - improve query performance by automatically applying micro-partition (many sub-small tables and read data in cluster) to only read specific amount of rows
4. Graph
    - Neo4j has node or vertex as real-life entities (name, age, etc) and edges as relation between nodes

### 2. Data Warehouse
Definition:
- to store a big amount of structured/ semi-structured data
- the stored data is historical and not used in production stage (no major change happens)
- used in data analytics (OnLine Analytical Processing)
- not strict with relation as relational database
- e.g. Apache Hive/ Impala, Amazon Redshift, BigQuery, Azure Synapse, Snowflake

**Data Mart is a small version of Data Warehouse**   for a sub-unit for business
- e.g. Sales Data Mart, Marketing Data Mart, Call Center Data Mart
- [learn more about data](https://www.guru99.com/data-mart-tutorial.html)

### 3. Data Lake
Definition:
- to store big data (usually be raw) whether structured or unstructured as a file
- most providers have fault tolerance policy in their product so it can be sure that there are replicas of data
- can be called as object storage or blob storage
- If there is bad data in Data Lake, it’s called Data Swamp
- is schema-on-read (know the schema when read data unlike traditional database and data warehouse which is schema-on-write so they need predefined schema)

</details>

## Lecture 1
<details>
  <summary><b>Data pipeline</b></summary>

### Data Pipeline
Definition: 
- A pipeline to move data from source to destination   

Why data pipeline is needed: 
- integration: easy to manage data e.g. applying data transformation to every source, adding automation, etc
- decoupling: less complex when a change of source/dest happens because src, dest don't connect directly

#### Data Pipeline Design
**Data pipeline components**
- Data source: IOT sensors, spreadsheets, web/ moblie application 
- Processing: Extract -> Transform -> Load
- Destination: Database/ Data Warehouse/ Data Lake, Dashboards, AI models
- Automation
- Monitoring

**Processing**   
<U>Extract</U> 
- Things to consider how to extract
    - Type: Files (csv, parquet, etc), API (json, etc), Database, Data Warehouse
    - Format: Data Schema, Metadata, Table shape
    - Frequency: periodically update every hour?/ week? etc    
- After finished, data is stored in staging table if applicable

<U>Transform</U> 
- transformation example
    - change data format from source to expected format at destination
    - create new columns for data aggregation
    - enrich existing data with data from external source (third-party or public)
- After finished, move transformed data to staging area

<U>Load</U> 
- move data at staging area into data warehouse/ data lake/ database
 
**Key Considerations / Trade-offs**    
- <B>Accuracy</B> of data
- <B>Speed</B> of data transfer
- <B>Scalability</B> (data size per load)
- <B>Security</B> between data transfer
- Need to find balance between these (if add speed, may reduce accuracy), match business need 
- Example
    - <U>initial load/ historical load/ full load</U> vs <U>incremental load/ change data capture load</U>
        - this may affect speed 
    - <U>Batch (scheduled, event-driven)</U> vs <U>Stream (cdc, mini-batch)</U>
        - this may affect speed and accuracy

#### Tools for creating data pipeline

| No Code (Pre-built connectors) | No Code (Drag and drop) | Code                                                                  |
|--------------------------------|-------------------------|-----------------------------------------------------------------------|
| Fivetran                       | Talend                  | Hadoop MapReduce                                                      |
| Airbyte                        | Informatica             | Apache Spark (data processing tools but can works like data pipeline) |
|                                | Azure Data Factory      |                                                                       |

<details>
  <summary>these tools have trade-offs between flexible and convenient!</summary>
but I think recent no-code tools may be flexible enough as technologies develop all the time
</details>
</details>
<details>
  <summary><b>Data Integration</b></summary>

**Common Data source**
- Files (csv, parquet)
- Application Programming Interface/ API (free or paid)
- Web scraping
- Database
- Data warehouse
- Data lake

### Data Integration
Definition: create a **source of truth/ golden record** from merging data from multiple sources    
Benefit: can see overview of all data e.g. customer 360

Format of data integration
- Schema integration
    - structure conflict: 
        - combine 1 denormalised source with multiple normalised source from other department
    - naming conflict
        - the same column but different name in other department
    - !!! need understanding about sources from data owner before implementing
        - data schema?
        - frequency of update?
        - etc
- Value integration
    - the same data but in different form
        - currency, miles - kilometres, date format
    - data not matched
        - different update period in different systems e.g. one updates yearly, another updates monthly
    - !!! use primary key to match those unmatched value

</details>

## Lecture 2
<details>
  <summary><b>Data Quality and Data Cleansing</b></summary>

**Data Cleansing**: find and edit data anomaly (format error, missing data, outlier) <- (human error, sensor failure), but some data needs specialist to edit 

**data cleansing cycle**    
data auditing -> workflow planing -> workflow execution -> examine result -> data auditing    
!!! sometimes it's hard to find root clause, so it may need more learning or specialist to help

**Good Data Quality** needs   
- completeness -without missing values
- validity -not breaking the restriction
- consistency -having the same/ similar format

**benefits from good data quality**
- Data accuracy
- Data completeness
- Timeliness
    - up to date data
- Data consistency
- Data Validity

**Tools for data quality**
1. [data dictionary](https://atlan.com/what-is-a-data-dictionary/): a file that has all information of data like name, type, description
2. [data catalog](https://www.cloudskillsboost.google/focuses/11034?parent=catalog): a collection of information about data and metadata like data dictionary, moreover some catalogs have data masking to unveil data from specific employees
- Tools: Azure Data Catalog, Talend Data Catalog, 
AWS Glue Data Catalog, Google Dataplex
3. [data lineage](https://kylo.readthedocs.io/en/v0.9.0/how-to-guides/FeedLineage.html): a tool to show data transfer from source to destination, usually is incorporated in data catalog as a feature
- Tools: ApacheAtlas, OpenMetadata, DataHub, Kylo

</details>
<details>
  <summary><b>Exploratory Data Analysis</b></summary>

### Exploratory Data Analysis
Before implementing EDA, we have to do data profiling

**Data Profiling** is to see overview of data if there is an anomaly like see statistical values like mean, min, max, count, etc
- Tools: [ydata-profiling](https://github.com/ydataai/ydata-profiling)

   
**Techniques** to do EDA
- statistical techniques
- data aggregation
- data visualisation

**Two important questions for EDA guideline**
- Q1 Number or Visualization
    - number: descriptive statistics
        - distribution: count, mean, min, max, etc (data profiling?)
        - variance: standard deviation
    - visualization: histogram (how data is distributed and its skewness), boxplot (outliers), scatterplot (relation between two variables)
- Q2 Univariate or Multivariate
    - univariate: mean of each column
    - multivariate: covariance between two variables (scatterplot)
</details>
<details>
  <summary><b>Data Anomaly</b></summary>

**Data Anomaly**   
**Cause of Data Anomalies**
- error during extracting from sources or when transforming
- examples:
    - lexical error (typo)
    - duplication
    - inconsistency (not in the same format)
    - missing values
    - outliers

**Type of Data Anomaly**
- Syntactical Anomalies
    - spelling mistake, domain format error, syntactical error, irregularity
    - how to fix:
        - add data validation part to check data correctness before storing
            - set a specific set of rules to validate data -should be done by a team
        - check data source credit by comparing it with other sources
            - compare filled address with google map api
- Semantic Anomalies
    - duplication, integrity constraint violation (age must not be below 0), contradictions (end date is before start date)
    - how to fix:
        - use regular expression to find anomaly case
        - if not understand community pattern from regex101.com, can ask ChatGPT or Gemini about it
        - regex is different in each SQL
- Coverage Anomalies
    - missing values (Missing At Random-MAR, Missing Not At Random-MNAR)
    - how to fix
        - find cause of missing values
        - if error from sources, discuss with a team that maintain the data
        - If not error from sources, check Data Pipeline/ ETL code
        - fix it on your own after consideration about pros/ cons
            - delete all rows that are missing
            - data imputation with statistics
            - regression model to impute the blank space
- Outliers
    - sometimes outliers are interesting data not only error
    - use boxplot or three sigma (standard deviation) to detect outliers
</details>
<details>
  <summary><b>Distributed Data Processing</b></summary>

### Distributed Data Processing
**main components**

- Data Storage
    - Responsible for storing information
    - HDFS, BigTable ?
- Data Processor
    - Responsible for accepting user queries, converting them into a query plan, and executing it.
    - includes a job master, workers and clients to communicate with the master
- Metadata
    - Stores information about the tables/views/Schemas created by the system. E.g., Hive metastore, Unity catalog, etc

#### Hadoop MapReduce
| Pros                                           | Cons                                                                   |
|------------------------------------------------|------------------------------------------------------------------------|
| use a cluster of computers to compute big data | process so slowly as it has to write data into hard disk in every step |
|                                                | hard to code                                                           |

**example MapReduce cycle**

input → split data → map function → shuffle data → reduce function → output    
!!! not every function use map or reduce every time

[see more about MapReduce](https://www.edureka.co/blog/mapreduce-tutorial/)

#### Apache Spark
**Description**
- This technology is developed from Hadoop, but it writes data into memory rather than write new data into hard disk every step
- use Resilient Distributed Dataset for fault-tolerant of the system
- support modern programming language like Python, Scala, Java

**Additional modules**
- Spark SQL: to write SQL inside Spark
- Structured Streaming: for real time data
- MLlib: Machine Learning module
- GraphX: show data processing in Graph


**Type of data in Spark**
- Resilient Distributed Dataset
    - low level object of Spark DataFrame and Spark Dataset
    - support Java/ Scala/ Python
    - its command separated to two types
        - Transformation: Lazy until Action trigger and its transformed data cannot be change during execution(immutable)
        - Action: Execute itself and all previous transformation in memory and return results of the lineage
- Spark DataFrame & Spark SQL
    - Spark DataFrame
        - suited for data in Relational Database as it is in tabular format, similar to Pandas/ R DataFrame users
        - immutable object
        - higher-level abstraction built over RDDs
        - support Python, R, (Java, Scala)
    - How Spark SQL works
        - convert SparkDataframe to TempView(on device-level)/ GlobalTempView(Cluster-level) and use SQL command on that view
        - Spark SQL is superior to Spark Dataframe or Dataset as it is already optimised and compatible with other SQL-based languages
- Spark Dataset
    - combines the benefits of RDDs (type safety, object-oriented programming) and DataFrames (Catalyst optimization and ease of use)
    - can be viewed as a specialized form of Dataset (Dataset[Row])
    - support Java, Scala as it supports JVM object    

[more about RDD, dataset, dataframe](https://www.databricks.com/blog/2016/07/14/a-tale-of-three-apache-spark-apis-rdds-dataframes-and-datasets.html#:~:text=In%20this%20blog,%20I%20explore%20three%20sets%20of%20APIs%E2%80%94RDDs,%20DataFrames,)

**How to execute on Spark**
- through specific modules like PySpark, SparkR
- through Spark Shell but only one command works at the time
- through Spark Submit to send the whole job to run on a cluster

**How to install Spark**
- through local machine but every machine has different OS, so it needs more time
- through cloud computing like Google DataProc, Databricks but service cost might be high
- on Kubernetes, works well with local server or cloud server and also be easy to install as it doesn’t need prior Hadoop installation

**Recommended Tools**
- Databricks: Spark on Cloud Computing (works well with many Cloud providers)
    - notebook-like UI and support Python, R, Scala, Java, SQL
    - support all major cloud provider: AWS, GCP, Azure

**Pyspark coding**
- `SparkContext` (sc) = connection to Spark
    - to load data into RDD
        - `sc.parallelize([1,2,3]/ [(1,'a'),(2,'b')])`
        - `sc.textFIle(path, minPartitions=5)` use `getNumPartitions()` to check how many partitions
    - RDD.map(function): 1 on 1
    - RDD.filter(function): reduce rows
    - RDD.flatMap(function like split string): add more rows
    - RDD.union(another RDD)
    - RDD.reduce() result in one value, RDD.reduceByKey()
    - to save file: RDD.saveAsTextFile() and RDD.coalesce(1).saveAsTextFile()
- `SparkSession` (spark) = interface to the connection
    - `SparkSession.builder.getOrCreate` to create `SparkSession`
    - `SparkSession.catalog.listTables()` to list all tables
    - `spark.createDataFrame(RDD, schema= names)` to create DataFrame from RDD, pandas also uses this command (`toPandas` to convert back)
    - `df.printSchema` to show data type, `df.columns` to show all columns, `df.describe()` to show stat of data
    - `spark.sql` for query and [`results.show`](http://results.show) to show results
    - when convert `pd.DataFrame` to `spark.DataFrame,` the dataframe still can’t use `.sql` or other catalog commands to query directly as it’s only on local. so it needs to use `createTempView` to enable the command
    - `df.filter(”col > 10”)` or `df.filter(df.col > 10)` = where in sql
    - `df.select("col1", python_variable)` = select in sql or use sql expression with this  `df.selectExpr(”col1”, “col2 / 10 as xdd”)`
        - the diff between it and `withColumn()` is `select` show only selected col and `withColumn` show all cols
    - `pyspark.sql.functions as F` to enable more agg functions like `stddev`
    - for machine learning, call [`pyspark.ml`](http://pyspark.ml) to use `Transformer` for dataframe transformation and `Estimator` for model
    - change type, `df.withColumn("col1", df.col1.cast("integer"))`
    - to do one hot encoding: 1) stringindexer 2) onehotencoder as spark only accept numeric value

</details>

## Lecture 3
<details>
  <summary><b>Cloud Computing</b></summary>

|                     | On-Premise                                                  | Cloud Computing                                                                    |
|---------------------|-------------------------------------------------------------|------------------------------------------------------------------------------------|
| cost                | server, maintenance, human resources, -CapEx                | pay as you go (pricing depends on each cloud provider) -OpEx                       |
| place               | dedicated area                                              | choose a site provided by cloud providers                                          |
| security at place   | need cost in security guards but still prone to human error | no worries                                                                         |
| efficiency          | based on budget                                             | flexible                                                                           |
| incident management | need countermeasures for incidents e.g back-up sites        | cloud providers also offer several sites for backup and assure customers as in SLA |
| software license    | need to buy on their own and a team to maintain it          | many ready to use and up to date services                                          |

**Type of cloud computing**
- Public Cloud
    - pros
        - many services
        - data center around the world
        - scalability and flexibility
        - Service Level Agreement to gain trust
    - cons
        - data is not in private area, might affect data privacy
- Private Cloud
    - pros
        - data control in organisation
        - more privacy than public as it’s only used in the private network
    - cons
        - cost for hardware and human resource to maintain and manage network
- Hybrid Cloud
    - pros
        - have own server but deploy public cloud in the server
        - data privacy control
        - many services from cloud provider
    - for example
        - Google Cloud Anthos to control Kubernetes-installed servers (private server)
        - Amazon Outpost to be installed in private data center

**Concepts**
- Infrastructure as a Service
    - virtual machine, virtual networking, google cloud storage (no need to maintain physical server)
- Platform as a Service
    - google cloud composer, google cloud dataproc (managed server, still needs care in some part)
    - google app engine, cloud sql (serverless)
- Software as a Service
    - google drive, gmail, google colab (no need to create app)

[IaaS, PaaS, SaaS from Azure](https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/2-describe-infrastructure-service)

***how to increase efficiency of computing***
- vertical scaling
    - increase server’s specification
- horizontal scaling
    - increase a number of servers (suited for a cluster in Big data)

**Cloud Agnostic**
- to use a service that works compatibly with several cloud providers
- this one is to avoid vendor lock-in (stuck in one ecosystem)
    - another is to use services from different cloud providers

! can see how amazon s3 achieves 99.999999999% in the slide and erasure coding as well    
!! can use private service access to migrate from gcp to aws
</details>

## Lecture 4
<details>
  <summary><b>Data Pipeline Orchestration</b></summary>

Data Pipeline Orchestration will help to arrange an order of ETL pipelines and monitor the process from the start to the end

Old orchestration tool, [Cron](https://crontab.guru/), has some disadvantages such as hard to manage when there are many dependencies, and no job status monitoring

New tools:
1. Apache Airflow
2. Dagster
3. Prefect
4. Argo workflow
5. Kubeflow pipeline
6. Flyte
7. Kestra
8. Mage.ai 

</details>
<details>
  <summary><b>Airflow</b></summary>

Airflow is python-based tool, has big community and third party providers

Concept: Directed Acyclic Graph (DAG) > tasks always have destination


**Airflow's use cases in Airbnb**
1. Data Cleansing
2. Email Targeting
3. Growth Analytics (A/B testing)
4. Sessionization (Click on websites)
5. Search (order)
6. Maintenance 


**Components**
- cli
    - handle and monitor pipeline on command line
    - backfill data
- web ui for the cli
- metadata repository
    - keep job status and other information(meta data) of data pipeline
- workers
    - controlled by airflow master node to execute jobs
    - so it’s automated
- scheduler
    - work like cron

**Task is a job in a single DAG**
- Sensor task
    - ready and waiting for file input (like detecting a new file in dags folder) or specific conditions
- Operator task
    - to command the system or transfer data with specific programming languages (Bash, Python, etc)
- Hook task (additional)
    - connection to third party providers (S3, etc)
    - can work with sensor and operator when both have to connect with third party whether directly or indirectly

**Example of Airflow tasks for ETL**
- Extract
    - sensor
        - receive signal from new file coming
    - operator
        - transfer file to prepare cleansing
- Transform
    - operator
        - clean data
- Load
    - operator
        - transfer transformed data to data storage
    - sensor
        - monitor storing process

There are more pipeline orchestration tools such as Cloud Composer from GCP, Data Factory from Azure

</details>
<details>
  <summary><b>Airflow DAG</b></summary>

**DAG definition file (python file)**
1. importing modules
    - import DAG/ operator/ python modules (`datetime`, `timedelta`)
    - recommended module
        - `days_ago` to calculate time diff instead of `timedelta` for python
2. default arguments
    - configurate a dictionary for default/ constant variables
3. instantiate a dag
    - schedulers adopt ETL concept
        - it will work after the chosen time passed
            - `@daily` ETL will work tomorrow as it needs to wait until today has passed
            - `@weekly` monday-sunday so it will work after sunday
    - set name, start/ end date, scheduling interval
    - can see examples in the silde
4. tasks
    - set operator (`BashOperator`/ `PythonOperator` are popular)
    - can use operator from airflow or other providers (third party)
    - see more operators in the slide
5. setting up dependencies
    - task1 >> task2, task1 << task2, task1.set_downstream(task2), task2.set_upstream(task1)
    - [task1, task2] >> task3 ≠ task1>> task2>>task3
    - [task1, task2] >> task3, task1 >> task3 << task2  -> fan in
    - task1 >> [task2. task3]   -> fan out

</details>

## Lecture 5
<details>
  <summary><b>Data Warehouse</b></summary>

**Normalized vs Denormalized**
| Normalized                                                               | Denormalized                                                            |
|--------------------------------------------------------------------------|-------------------------------------------------------------------------|
| Split data into each table to reduce duplication, so less space required | Store data in a table and data might be duplicated, much space required |
| Join cost is high when querying                                          | Less join cost than normalized, so read speed is faster                 |
| Easy to alter data in a row, write process is faster as table is small   | Need time to find a row to edit as table is too big                     |
| Good for Database which has many write processes (OLTP)                  | Good for Data Warehouse which has many read processes(OLAP)             |

but columnar storage helps data warehouse to save more space and read faster than row-base storage

**Table, View**    
Table   -actual data stored in table    
View    -view-only table that show data from a table

| View                                     | Materialized View                                                                  |
|------------------------------------------|------------------------------------------------------------------------------------|
| No extra space                           | Need space to store query result                                                   |
| Need to recalculate when calling a query | No need to recalculate as it already stored                                        |
| Queried data is fresh                    | Data might not be up-to-date (but some providers have their own solution for this) |

**Increase query speed with partition and index:**   
Partition: reduce size of data to go through when reading   
Index: focus only an index column, save time to go through irrelevant columns

</details>
<details>
  <summary><b>BigQuery</b></summary>

BigQuery is a serverless data warehouse from google cloud, sql-based query    
[Data types in Bigquery](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types)

Native table: data stores in bigquery, so read speed is faster    
External table: create a table from data stores outside bigquery, it's convenient but not fast as native table

**Some tips to optimize cost on bigquery**    
1. use **Preview** tap to see data instead of `select * from table`
2. don't use `select *`, only query wanted columns and `limit` doesn't help here
3. set **Table Expiration** for a temporary-used table  
4. use other data storages for long term storage options

[Cost Optimization for BigQuery](https://cloud.google.com/blog/products/data-analytics/cost-optimization-best-practices-for-bigquery)

Another way to reduce cost: capacity-based    
it's like we reserve processing slot and pay in advance for the slot, so don't have to concern about cost as much as on-demand

[bigframes](https://cloud.google.com/python/docs/reference/bigframes/latest) (bigquery dataframes) is a library to run pandas dataframe on bigquery engine

</details>
<details>
  <summary><b>Data Lakehouse</b></summary>

[Data Lakehouse](https://www.databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html) has some interesting advantages from both data warehouse and data lake
- support ACID Transaction
- need to set schema and can apply governance
- be compatible with BI tools 
- separate compute and storage.
- support standard file format like parquet
- support structured, semi-Structured, unstructured data
- support real-time streaming data

BigLake = a connection to enable BigQuery features, although data is stored in GCS 

BigLake removes the problem about data duplication in GCS and BQ for external table or object management for native table

Big Lake can connect to AWS S3, Azure Data Lake Storage GEN2 and work with Apache Icebreg, GCP DataPlex

[How does BigLake work?](https://cloud.google.com/bigquery/docs/biglake-intro)

</details>
<details>
  <summary><b>Dataplex and Analytics hub</b></summary>

**Dataplex**   
A service to do data mesh in GCP. [introduction of dataplex](https://cloud.google.com/dataplex/docs/introduction)

Interesting points
- create data mesh without data transfer (data fabric)
- manage data governance and security from here 
- access to all data from here (self-service data platform)
- search wanted data with data catalog
- use serverless spark and notebook service to query or process data in an org

**Analytics hub**    
A Google Cloud feature to share information from BigQuery

Interesting points
- share information automatically
- limit access from some users, so data can be sold to specific partners
- commit Federated Computational Governance to Data Mesh

</details>

## Lecture6

<details>
  <summary><b>Data Visualization</b></summary>

### Data visualization

**Report** -analyze data and write the report of it (more than 1 pages?) to be ready for ad-hoc question    
**Dashboard** -extract all necessary information for user to answer their business questions quickly

**Tools**
1. Speadsheets: MS Excel, Google sheets
    - suited for small datasets

2. BI tools: Power BI, Looker Studio, Tableau
    - 

3. Coding: Python, R, JS
    - 

</details>

## Lecture 7

There are case studies in the slide to learn

<details>
  <summary><b>Data files</b></summary>

**Speadsheets (MS Excel, GG sheets)**
- it's fine for a small dataset
- doesn't work for a massive dataset

**Comma-separated value (CSV)**
- it's popular and can be opened on spreadsheets
- a file might be too large as it doesn't have compression
- no data type identifier (metadata)
- not convenient for a columnar storage

**Apache Parquet**
- stores data in columnar, so it needs less space
- stores metadata (if upload to BigQuery, it will set data type automatically)

**Apache ORC (Optimized Row Columnar)**
- store data in row columnar, so stored data is small and it will access faster

**Apache ARVO**
- stores schema (in JSON) in a file
- stores files as binary, so file size is small
- works with RPC system (Remote Procedure Call)

[more details](https://medium.com/@aiiaor/%E0%B9%83%E0%B8%8A%E0%B9%89-file-format-%E0%B9%84%E0%B8%AB%E0%B8%99%E0%B8%94%E0%B8%B5%E0%B8%AA%E0%B8%B3%E0%B8%AB%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%81%E0%B9%87%E0%B8%9A%E0%B8%82%E0%B9%89%E0%B8%AD%E0%B8%A1%E0%B8%B9%E0%B8%A5%E0%B9%83%E0%B8%99-database-%E0%B8%87%E0%B8%B2%E0%B8%99-data-science-6f223c3306fb)

Apache Arrow helps to convert files into other formats
</details>

**Network Design** is necessary to design every service to properly work together    
Interesting topics: Networking (VPC, Subnet, CIDR range), Authentication & Authourisation    
[examples from Azure](https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/hybrid-connectivity)

**Data Governance** is to manage data from extracting data to storing data and using it    
Things to focus in Data Governance
- Data Quality: valid trusted data follow business rules
- Data Access: access management, data catalog
- Data Security: data masking, password hashing?    

Example tools: [DataHub](https://datahubproject.io/), [Apache Atlas](https://atlas.apache.org/) (for Hadoop system)

**Data Security and Privacy**
- Data Breach is a critical and harmful incident in business
- Personally Identifiable Information (PII) has to be protected no matter what 
- Besides that, PII must be managed according to local law about privacy like 
    - [GDPR](https://www.snel.com/what-is-gpdr) (EU)
    - [PDPA](https://pdpa.sidata.plus/) (TH)
- Data Protection guideline: 
    - [Guide](https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Other-Guides/Guide-to-Data-Protection-by-Design-for-ICT-Systems-(310519).pdf)
    - [Technical Guide](https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Other-Guides/Technical-Guide-to-Advisory-Guidelines-on-NRIC-Numbers---260819.pdf)

**Modern Data Warehouse**
- Snowflake
    - support popular cloud computing providers
    - support semi-structured data
    - near zero management
    - time travel (check history log)
    - store procedure (built-in function in Python, Scala, Java, Javascript)
- Google BigQuery
- Databricks
- Azure Synapse Analytics
- Mother Duck

**Data Lakehouse**
- Delta Lake
- Apache Hudi
- Apache Iceberg

**Next things to learn**
- Git -Version Control
- Container & Docker
- Kubernetes: Container Orchestration
- Machine Learning model 
    - To understand how to prepare data for feature engineering
    - AutoML 
    - Generative AI (Fine-tuning, RAG)
- Advance Python, SQL, Software engineering
- how to extract data from others like NoSQL DB, XML 
- Spark in Kubernetes, Spark performance tuning
- services from several Cloud providers
- how to create complex ETL pipelines
- other open source softwares like Hive, Cassandra, Druid, Kafka, Presto 
- recommended websites
    - [Fundamentals of Data Engineering](https://blog.datath.com/data-engineer-free-book/)
    - [Designing Data-Intensive Applications](https://dataintensive.net/)
    - [Data Engineering Cookbook](https://cookbook.learndataengineering.com/)
    - [Data Engineering Wiki](https://dataengineering.wiki/Index)

<details>
  <summary><b>Interview preparation</b></summary>

1. Practice to describe how ELT, ETL pipeline flows from the start until the end
    - Topics to revise
        - OLTP vs OLAP
        - Data Lake
        - ETL vs ELT
        - Batch vs Streaming
        - Data Integration
        - Data Quality
        - Cloud Computing
2. Practice introduction with AI
    - [interview warmup](https://grow.google/certificates/interview-warmup/)
    - use STAR methods to answer questions
        - Situation
        - Task
        - Action
        - Result
        - No need to use all four in all questions 
3. Practice along this [guideline](https://cookbook.learndataengineering.com/docs/08-InterviewQuestions/)
4. Create portfolio websites
    - adding projects to show what you can do
        - [Examples](https://www.startdataengineering.com/post/data-engineering-projects/)
5. Practice more skills
    - use [this](https://manussanun.medium.com/skill-sets-for-data-engineer-2024-adf43ac37b53) as a guideline

</details>

**Organizations that should know**
[Apache Software Foundation](https://projects.apache.org/projects.html?category)
[CNCF: Cloud Native Computing Foundation](https://landscape.cncf.io/)
[Linux Foundation: AI & Data Foundation Landscape](https://landscape.lfai.foundation/)

