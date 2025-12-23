# Free Data Engineer Bootcamp from Zach

source: [The ultimate YouTube DE boot camp](https://github.com/DataExpert-io/data-engineer-handbook/blob/main/bootcamp/introduction.md)

## Lecture 1
+ Types of impact that data engineer can provide
  - Measurable: Efficiency improvements and experimentation outcomes from data analyst or scientist
  - Hard-to-measure (hard in term of difficulty and time worthy): Quality improvements (data quality or bugs fixing) and team enablement outcomes (saving time from script or any actions)
  - Immeasurable: Changing intuitions (changing how decision will be made), team culture improvements (creating team dynamic as a leader), being a glue person (holding the team together from being in their own silo)

+ Data Engineer's value
  - supplying insights from preparing data
    - valuable insights can create one of three things for decision making: reinforcement, contradiction, no obviuos result (fail to support or contradict)
  - increasing pipeline efficiencies to save time from old pipeline or reduce maintenance time
    - proper data modeling
    - improving oncall processes: save more time for maintenance
    - reducing data volumes: compress data-parquet or partition/ sample data
    - picking the right tool for the job-comparing pros and cons of each tool (i.e. migrations: data volume, frequency of data usage, etc)
      - e.g Spark rely on memory so it might fail more frequently than Hive that is slower
      - Presto limit only 1TB memory, less suitable for bigger data
    - simplifying model and reducing capabilities like do only 80% not all (it's unnecessary to have competent model or pipeline)
      - e.g. waste time to prepare unused or rarely-used columns because of just-in-case thought but with privacy laws it can reduce some of this
        - rarely-used can be security logs that will be used only when incidents happen
  - providing data quality whether data integrity or errors
    - data quality check: write audit publish pattern
    - documentation
    - good engineering practices
    - clear expectations -reduce communication overhead: SLA, documented gaps (things that might not be in dataset but can impact AI model or decision)
  - after having good pipeline, good data quality -> other engineers can work faster instead of spending time to fix data quality or bugs, waiting old pipeline to finish
  - persuading decision makers to rely on (good) data more 

+ signals when organization may overvalue insights
  1. when crisis happens, they trade long-term tech debt (software(bad design), hardware(server, cloud), human-mentality/ burning out) for quick insights
  2. many ad hoc request from analytic partners (tackling it with requesting form to combine all requests into one)
  * how to stop those things: learn to say no, leverage manager for support, persuade stakeholders with reasons why robust data models are better than quick pipelines

## Lab 1 
### Tableau
+ columns = x-axis?, rows = y-axis?
+ filter top n with right click -> create set
+ Date can be chosen to be Yearly, Monthly, etc.
+ percentage of total to compare in percentage but table (across) and table (down) ??

## Lecture 2
### Dashboard Best practice - Final layer
+ Don't join two tables except 1 side is very tiny
  - Do denormalize and pre-aggregate (might lose some details but get fast-loading instead)\
    - Grouping sets (SQL?) is great here
  - No need to care about master data, scalability because dashboard has to be refined for human
+ Use a low-latency storage for dashboard's data e.g. Druid
+ Think about audience of the dashboard
  - Exces: very easy to understand immediately, low interactivity
  - Analysts: more charts, more density, more exploration capabilities -> may skip pre-aggregate step to keep more details
+ Types of questions
  - Top line questions -may add filter for some dimensions like area:
    - how many users do we have?
    - how much money do we make?
    - how much time are people spending on the app?
  - Trend questions -time related: 
    - How many users did we have thsi year versus last year?
  - Composition questions:
    - What percentage of our users are Android versus IPhone?
    - What percentage of our users are male compared to female?
+ What can tell from numbers
  - total aggregates: count, sum, etc
    - can be used to tell overall performance of business
  - time-based aggregates: this year, last month
    - to identify trends and growth 
  - time & entity-base aggregates: count in this year
    - easily plug into AB testing
    - used by data scientists to see aggregated fact data in a way that is performant
    - often times included in daily master data
  - derivative metrics (week-over-week/ month-over-month/ **year-over-year**)
    - don't do day-over-day
    - more sensitive to changes
    - % increase better than absolute number
  - dimensional mix (e.g. %US vs %India, %Android vs %iPhone): can be track from SCD
    - identifies impact opportunities
    - spot trends in populations, not just over time -> help in root cause analysis
  - Retention / Survivorship (% left after N number of days)
    - J curves
    - Great at predicting lifetime customer value
    - understanding stickiness of the app

## Lab 2



