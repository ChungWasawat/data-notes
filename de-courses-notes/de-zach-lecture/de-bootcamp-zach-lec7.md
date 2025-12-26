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




