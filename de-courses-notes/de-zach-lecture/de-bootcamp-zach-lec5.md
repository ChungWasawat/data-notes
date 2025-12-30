# Free Data Engineer Bootcamp from Zach

source: [The ultimate YouTube DE boot camp](https://github.com/DataExpert-io/data-engineer-handbook/blob/main/bootcamp/introduction.md)

## Lecture 1
normally, data is extracted once a day, but it is also extracted "intraday" in streaming
+ Difference between streaming , near real-time, real-time
  - streaming -continuous
    - data is processed as it is generated
    - Flink
  - near real time
    - data is processed in small batches every few minutes
    - Spark Structured Streaming
  - Real-time and streaming are often synonymous but not always
    - eventhough it's called real-time but in reality, there are some seconds to stream and process data via pipeline: event generation -> Kafka -> Flink -> sink (storage) 
  - Small batch/ hourly batch, microbatch, near real-time are the same
  - Less technical people think real time = streaming, but it is not for most of their requests
    - it means low-latency or predictable refresh rate
      - e.g. refresh at 9AM every day
  - Streaming also requires different skill sets compared to batch as Streaming pipelines need to run 24/7
    - it is much more software engineering oriented (act more like servers than DAGs)
    - requires quality tests more than just unit test and integration test
      - network? like servers

+ Considerations for streaming
  - Skills on the team
    - If it's new for the team, need at least 3 people to handle the system (preventing burnout or overworkload for 1 or 2)
  - Need an answer what the incremental benefit is
    - tradeoff between daily batch, hourly batch, microbatch, streaming
    - Complexity of data quality of streaming, compared to batch pipelines
  - Homogeneity of pipelines
    - The team should stick to what they always do like batch team should only handle batch pipelines, the same to streaming as well
+ Use cases for streaming
  - Obvious
    - low latency is the most important
    - e.g.
      - detecting fraud, preventing bad behaviour asap
      - high-frequency trading
      - live event processing
  - Grey area (microbatch may work too)
    - data that is served to customers
      - customers love latest data but it actually needs to be real-time? or just microbatch
    - reducing the latency of upstream master data
      - instead of extracting the entire data at once, it can be divided to do microbatch hourly to reduce heavy compute cost
      - in some case, it can't be streaming because dataset size is too big to hold on RAM all day
  - No-go
    - Ask the above questions to ensure that reducing latency really benefits business
    - Analysts want latest data even though yesterday's data can be used 
+ The structure of a streaming pipeline
  - sources:
    - Kafka
    - RabbitMQ
      - low thoughput -> not scalable as Kafka
      - have more complex routing mechanisms (do message broker easier than do pub-sub in Kafka) 
  - enriched dimensional sources
    - Google Flink side inputs: add more columns to the streaming data/ fact data (denormalization with dimensional data)
  - compute engine (process data like in SQL)
    - Flink
    - Spark Structured Streaming
  - destination or sink (storage)
    - another Kafka topic
    - Iceberg -Data Lake
      - allow people to append existing partition unlike Hive (Big batch oriented)
      - streaming friendly
    - Postgres -Database
+ Streaming challenges
  - Out of order events
    - different latency can make data land to sink after its later generated data (misordered)
    - Flink has watermarking to deal with out-of-order events
      - watermark like a time window/ buffer like 15 seconds to guarantee the order of events 
  - Late arriving data
    - need to set time to tell it is too late
    - not a problem for batch as it waits until schedule time to extract data
  - Recovering from failures
    - The longer we wait to fix the failures, the more data gets behind it
    - How Flink deals with this problem
      - Offsets
        - Earliest offset: read everything back in Kafka as far as it can read
        - Latest offset: only read new data after the job starts
        - Specific timestamp (maybe like when it failed): only read data at the time and after
      - Checkpoints
        - save checkpoint evey n second to keep the state of the job at the moment
        - only used internally in Flink
      - Savepoints
        - more agnostic than Flink (compatible with other systems)

## Lecture 2
