# Free Data Engineer Bootcamp from Zach

source: [The ultimate YouTube DE boot camp](https://github.com/DataExpert-io/data-engineer-handbook/blob/main/bootcamp/introduction.md)

## Lecture 1
+ Repeatable analysis: reduce cognitive load of thinking about SQL, streamline impact\
  - common pattern
    - aggregation-based: 
      - "group by" dimensions to do sum, count, average, percentile
      - upstream dataset is often daily metrics
      - type
        - trend analysis: used to tell if it's a increase of decrease
        - root cause analysis: use other dimensions to get the root cause from first result like total users=1m but 1.5m in US and -500k in India (in this case additional dimension is country)
        - composition
      - should have daily aggregation for daily fact data and create new dimension for it
        - like aggregate data to get daily total comments and classify users based on it (active class A, class B, etc.)
      - think about the dimension combinations that matter the most
        - when using percentage, don't forget to look at the actual count as well
        - don't forget that combine high cardinality dimensions willl return many rows back
      - careful looking at many-dimension combination, long-time analysis(> 90days)
    - cumulative-based
      - time is significant to see how different dimensions change compared to others
      - Full outer join is used a lot for cumulative tables
        - no data counts as data unlike aggregaton-based
      - type:
        - state transition tracking
          - growth accounting
            - states of users
              - New ( not exist yesterday, active today )
              - Retained ( active yesterday, active today )
              - Churned ( active yesterday, inactive today )
              - Resurrected ( inactive yesterday, active today )
              - Stale ( inactive yesterday, inactive today )
              - Deleted ( active/inactive yesterday, not exist today ): specific for privacy legal.
                - if using anonymous data, may use Stale instead
            - (New + Resurrected) / Churned = growth rate
            - work very well with ML classifier to track its performance
            - example usage
              - to label fake account:
                - new -> not label fake before, fake today
                - reclassified (resurrected) -> labeled fake before, not fake today (pass challenges to prove not fake)
                - fake reclassified -> not fake before, fake today
                - churned -> fake account leaving
            ![growth accounting example chart]()
        - survival analysis/ retention/ J curves
          - used as reference to create a future plan
          ![survival analysis chart]()
          - curve_name, state check (interesting state), reference date (start counting date)
          ![survival analysis example]()
    - windown-based
      - keyword is rolling (use from n .. ago)
      - most use: FUNCTION() OVER (PARTITION BY keys ORDER BY sort_keys ROWS BETWEEN 'n PRECEDING' AND 'CURRENT ROW'
        - not use: BETWEEN CURRENT ROW AND n/UNBOUNDED FOLLOWING
      - type
        - DoD / WoW/ MoM/ YoY
          - DoD is the most sensitive to change, chart will fluctuate a lot
          - will become less sensitive when using a big unit D<W<M<Y
          - YoY is used a lot 
        - Rolling sum/ Average
          - can decrease volatility of the chart by not using the data directly but do sum or average from n days ago until current
        - Ranking

## Lecture 2
+ questions in sql interviews that will almost never do on the job
  - rewrite the query without window functions
    - lead, lag is like doing self-join
    - only use when the question gives keyword like rank, row_number
  - write a query that leverages recursive common table expresions
    - rare case like join three layers hierarchy (3 tables)
  - use correlated subqueries in any capacity
+ must do this if they don't give some restrictions
  - care about the number of table scans (I/O cost)
    - use count(case when)
    - use cumulative table design
  - wrtie clean SQL code
    - use common table expressions (with ..)
    - use alias (as  ..)
  - suggestion: should use explain() to see how each query works
    - AST: Abstract Syntax Tree
      - lower layer of SQL -> make how SQL run in order (where -> Group By, etc)
+ Advanced SQL techniques
  - GROUPING SETS/ GROUP BY CUBE/ GROUP BY ROLLUP
  - self-joins
  - window functions: lag, lead, rows
  - cross join unnest (called by sql-based) / lateral view explode (called by hive-based)


