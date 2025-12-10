# Free Data Engineer Bootcamp from Zach

source: [The ultimate YouTube DE boot camp](https://github.com/DataExpert-io/data-engineer-handbook/blob/main/bootcamp/introduction.md)

## Lecture 1
### Fact Data Modeling
+ Facts are something that actually happened or occurred e.g. app logs of users, a transaction of some activitie so they are immutable (unchangable) and often used in aggregations unlike dimensional data that is often used in filtering, grouping or giving context for facts data


+ Imagine that what you can tell from 1 row of fact data table, you can't tell **WHO, WHERE, HOW** from the IDs you see on the row except you did join or keep it denormalized those questions can be answered from dimension data tables.   
For fact data table, the questions are **What, When** e.g. what action users do: buy/ sold/ deposited/ clicked/ delivered, what when data is collected: timestamp/ date


+ Fact modeling is hard because
    1. has 10x-100x volume than dimension data e.g. 1 user can create many activities 
    2. require a lof of context (dimensional data) for effective analysis
    3. without context, duplicate data in facts are way more common than in dimension

+ Normalization vs Denormalization
    - Normalization is best for small data to deduplicate data but for large data required many resources to join data
    - Denormalization always brings some dimensional attributes so it is quicker for analysis (less join) but requires large storage instead
        - It can reduce compute and network cost to do join process. For the example in the video, denormailzation can reduce compute cost to join large datasets by storing more data so it doesn't need to join anymore

**Don't count raw logs as fact data because raw logs doesn't have proper format for analysis and might have duplicate problem**

+ How does fact modeling work?
  - fact datasets should have quality guarantees otherwise we can't tell what's going on there (it's answer for what, when)
  - fact data should be smaller than raw logs as it doesn't keep unnecessary columns or hard-to-understand columns e.g. http status or error log (this is for software engineer)
  - fact data doesn't need to in normalized form only, it can be in denormalized form but keeps only necessary columns otherwise it is raw logs instead of fact data
 
+ Data drift
  - Data drift is essentially the concept that the data in production (Analytics or AI model) has changed over time from the version it's been used.
  - Shared schema about how every team has changed the dataset to make everyone on the same page (changed -> transformed, computed etc)
 
+ how to handle high volume fact data
  - sampling: it doesn't give result for all use cases (imprecision) but it gives an overview of distribution when do with different sample many times
  - broadcast join for partitioned data
      - just bring shared table (small table) to every node that stores each partition of data and do join to reduce time to shuffle all data
  - bucketing: fact data can be bucketed by one of the important dimensions (often user) so it reduces cost from shuffle when joining
      - bucket join:
        1. separate all data into many small tables by hashing key column (to join) for both tables in the same amount
        2. join each small table from both tables that have the same hash key with the key column
      - sorted-merge bucket join: the same as above but adding sort process for all small tables before joining  

+ how long should you hold onto fact data?
  - Big tech approach
      - < 10TB: retention didn't matter much, might anonymize data after 60-90 days before move transformed data to a new PII table (legal-wise)
      - \> 100TB: very short retention period -14 days or less to not make the cost high   

+ Deduplication of fact data
    - example
        - user click to see the same notification multiple times
        - network error causes duplicate data
        - error from automation that might cause transactions happened at the same precise timestamp
    - how to deduplicate 
        - criteria: no duplicate in a weeek? a day? an hour? before it will be used in data extraction, distribution of duplicate might give some insight
        - solutions
            - streaming (time window: suggest 15min to 1hour to not use too big size of memory)
            - microbatch (divide a single day data to small 24-hour data and deduplicate data by pairing close datasets like 0 and 1 to be result a, 2 and 3 to be result b and then result a and b later until it comes back to a single dataset) <-- might have picture for this explanation     

## Lab 1


## Lecture 2



## Lab 2


## Lecture 3

## Lab 3

