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
  - Small batch, micro batch, near real time are the same
  - Less technical people think real time = streaming, but it is not for most of their requests
    - it means low-latency or predictable refresh rate
      - e.g. refresh at 9AM every day

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

## Lecture 2
