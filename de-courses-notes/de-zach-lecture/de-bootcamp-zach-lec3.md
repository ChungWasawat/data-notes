# Free Data Engineer Bootcamp from Zach

source: [The ultimate YouTube DE boot camp](https://github.com/DataExpert-io/data-engineer-handbook/blob/main/bootcamp/introduction.md)

## Lecture 1
### Spark
+ 


--example format below--
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
