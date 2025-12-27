# Free Data Engineer Bootcamp from Zach

source: [The ultimate YouTube DE boot camp](https://github.com/DataExpert-io/data-engineer-handbook/blob/main/bootcamp/introduction.md)

## Lecture 1
**every pipeline has its maintenance cost, so the more pipelines there are, the more expensive they are**
+ To handle ad-hoc requests from analytics
  - They, analytics, need to solve urgent problem
  - suggestion: DE should allocate 5-10% of their time to take ad-hoc requests per quarter and the remainings should be about long-term infrastructure/ pipeline
    - prioritize the requests based on complex and difficulty.
      - if it's simple and doesn't take time too long, can drop current work to do it for a short time.
      - other requests shuold be brought in the next schedule planning meeting
    - having a manager/senior to take a PM role to plan schedule ahead (like monthly, quarterly) is good
+ ownership    
**logging/ exports -> pipeline -> master data -> aggregated master data/ metrics -> dashboards/ experiments**
  - logging and exports: software engineer take this part but sometimes data engineer can share the ownership
  - pipeline/ master data: data engineer take the ownership
  - metrics(aggregated master data): sometimes data engineer has been assigned to be its owner or share with data analyst/ scientist
    - 40% business is here
    - needs business comprehensive skill to know what business needs from the data (must have a conversation about business context)
  - dashboards/ experiments: primary data analyst/ scientist ownership
  - **pipeline + master data + metrics** -> some company doesn't have data engineer so analytics engineer will take the ownership of these
+ Team structure
  - Centralized team: many data engineers in a team
    - pros: oncall is efficient as team have knowledge sharing, so they can handle issues
    - cons: work prioritization can get complex and expensive because of meeting with data requester or stakeholder
  - Embedded team: distribute DE in every team
    - pros: DE must have deep domain knowledge of the team they're in so they can support the team effectively
    - cons: DE can't do oncall for another DE in other teams because of lack of domain knowledge and DE can feel isolated as no DE to talk with
+ Common issues in pipeline
  - Skewed pipelines: some columns have more data than others, causing OOM
    - Use Spark 3.xx or latest and enable adaptive execution
    - Increase memory of the executor temporarily
    - Add a skew join salting in the job
      - [Spark Salting](https://medium.com/curious-data-catalog/sparks-salting-a-step-towards-mitigating-skew-problem-5b2e66791620)
    - Other causes for OOM issue
      - ...
  - Missing data or schema change from upstream data
    - Have pre-quality check for upstream data to save cost from running incomplete/ strange data
      - might have to change a code if not able to contact the data owner
    - Create a ticket to the data owner to fix the issue (long-term fix and unblock case) 
  - Doing new backfill that will impact downstream 
    - small migration
      - do a parallel backfill and create a new table "table_backfill"
      - if it looks good, change their name: production > production_old, table_backfill > production
    - bigger migration
      - build a parallel pipeline to populate data into a new table "table_v2" while production gets migrated
      - Inform owners of downstream to change references to table_v2, and inform again when table_v2 is completed and renamed to production
  - Business questions about where and how to use data
    - Set SLA on when the question will be answered because people can't stay on the monitor all the time
    - take common questions into a faq document
    - business questions on-call should be data analyst/ scientist's job, pipeline on-call is responsible to data engineer
      - to do this, analytics partners must loop in here


## Lecture 2
+ Besides optimization, deprecation is also the way to handle painful pipeline
  - what can be done
    - New technology
      - not always benefit, sometimes it's tradeoff 
        - Hive to Spark: trade some reliability for more efficiency (from disk to memory but memory is prone to OOM issue)
        - Batch processing to Streaming one: sometimes streaming can reduce overall memory usage (OOM issue) because it doesn't have to wait for all data to start processing
    - Better data modeling
    - Bucketing
      - When to use:
        - have an expensive high-cardinality JOIN or GROUP BY
        - have data more than 1 TB
    - Sampling: saving time to not process all data, just a sample
      - When to use sampling:
        - if directionality is a main point, sampling is good to bring it to the table in a meeting with data scientist to get a good number for a sample's size (statistics-wise)
        - e.g. it can be a small percent of all user's transaction or all transactions of a few users (this one can give a clear overview as it get complete history)
      - When to not sample:
        - Audit data: need the entire data
  - deprecating without a replacement can be a hard sell to stakeholder
+ Cloud bills breakdown
  - high cost -> lower cost: I/O > compute > storage
  - Why too much I/O can happen
    - If there are many downstreams that use data from the pipeline, I/O cost will be the highest
      - create a small table for frequently used data to reduce I/O cost from reading the entire data
    - duplicate data models like having many definitions for the same thing
    - inefficient pipelines (reading data for each day instead of reading once from cumulative table)
    - excessive backfills (test backfilling with 1 month data to check its quality before backfilling the whole data)
    - not sampling
    - not subpartitioning data correctly (might use predicate pushdown)
      - reduce I/O cost for the system to know which folder is relevant and read only that
  - but can't focus only how to reduce I/O cost because in some case I/O isn't the highest cost
    - if downstream of pipeline is dashboards, here the highest cost will be compute not I/O
  - Large I/O and compute costs
    - scan too much data (I/O): use cumulative table to reduce an number of reading data
    - process O(n^2) algorithms in UDFs~nested loops (compute)
  - Large I/O and storage costs
    - not using compress file format like Parquet (I/O)
    - duplicative data models (I/O, Storage)
+ A single source of truth
  - Benefit
    - everyone using the same data and having the same understanding about data 
    - easy to use/ find data and update it to the latest version
  - Step:
    - Document all the sources and discrepancies
      - talk wit all relevant stakeholders
      - find similar names of tables to check if they're the same
      - lineage of the shared source data is a good place to start
    - Reconcile the discrepancies to find/ create the right version of source that everyone agrees
      - There's usually a reason why there're multiple data sets
        - organizational: trust issue between team
        - ownership: a team shares spare resources to other teams that lack them, causing confusion to ones who don't know
        - technical and skill: not every team can make use of the data they owe
      - work with stakeholders to find an ownership model that every one is okay
    - Build a spec that outline a new path forward from what everyone agree
      - get what everyone wants in the pipelines
+ Tech debt models
  - Fix as you go: the person or team who created the code, should fix it if there is a bug
  - Allocate dedicated time of the team to fix tech debts, there won't be a meeting to talk about new features
  - On-call person do tech debt: after doing maintenance, if there's some free time, should spend to fix the debt
  ![tech debt models: pros and cons]()
+ Data Migration Models
  - Cautious approach
    - be careful to not break anything
    - run parallel pipelines for months until deprecating the old one (migration completes -> rename old one -> kill it after no problem happen)
  - Bull in a shop approach
    - migrate high-impact pipelines first
    - kill the legacy pipeline as soon as possible (so others will be forced to do the migration)
+ Proper on-call responsibilities
  - set a PROPER and reasonable expectation with your stakeholders
  - document every failure and bug to make it easier for the team to keep track
  - dedicate 20-30 minutes meeting to hand off what you face in your on-call week
  ![on-call document]()
+ Runbooks (similar to spec)
  - like a manual for pipelines, especially complex pipeline
  - important information to have:
    - primary and secondary onwers
    - upstream owners (teams not individuals): when their data quality fails
    - common issues (if any): should put clear description for each issue and how to fix it whether temporarily or permanently
    - critical downstream owners (teams not individuals): to quickly tell them if there is a problem and give them more time to handle it
    - SLAs and agreements
  - might arrange a meeting with upstream and downstream stakeholders to update current situation and each team's future plan to get everyone on the same page
  ![runbook stakeholders diagram]()
