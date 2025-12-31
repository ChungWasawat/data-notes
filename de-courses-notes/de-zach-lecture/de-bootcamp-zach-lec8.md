# Free Data Engineer Bootcamp from Zach

source: [The ultimate YouTube DE boot camp](https://github.com/DataExpert-io/data-engineer-handbook/blob/main/bootcamp/introduction.md)

## Lecture 1
+ Metrics must be simple to avoid complex data models
+ types of metrics
  - Aggregates / Counts
    - common use for fact data and some dimension
    - example
      - count of user activities
  - Ratios
    - data engineer should supply numerators and denominators, not the ratios (analysts' job)
    - example
      - conversion rate (carefull about additive/ non-additive data
      - purchase rate
      - cost to acquire a customer
  - Percentiles (p10, p50, p80)
    - useful for measuring the experience at the extremes
    - but still only supply daily aggregate, not the percentiles
    - example
      - p99 Latency: show the value at the best/ worst and consider a level of the problem
      - p10 engagement of active users: most of users are inactive or lurker, so can target only active users or engage those inactive/ passively active to be more active
+ Metrics can be gamed (short-term oriented goals?) but must be balance with long-term goals (cost, monthly metric)
+ How does an experiment work
  - make a hypothesis
    - Null hypothesis: no difference (try to reject it)
    - Alternative hypothesis: significant difference from the changes (need to experiment again)
  - group assignment (consider test vs control)
    - ~2 or 3 groups
    - who is eligible
      - are these users in a long-term holdouts from another experiment
        - e.g. no noti users can't be in any noti experiments
      - what percentage of users do we want to experiment on?
        - gradually increase (1% -> half -> all users) or all at first experiment depends on a total number of users
  - collect data
    - For privacy, should hash personal data like IP address or username
      - Stable ID in Statsig
    - the smaller the effect, the longer you'll have to wait
    - some small effects might not give clear result
  - look at the difference between groups
    - statistical significance
      - P value to determine if a coincidence is actually a coincidence or not
        - P < 0.05 is standard
        - the lower p value is, the higher certainty you get
        - but still there might be other factors like significant but tiny delta, contrast results
    - beware about skewness
      - winsorization can help to cut the extreme case out
      - change measure like event count -> user count

## Lecture 2
+ Leading vs Lagging metrics
  - metrics should be linked to money
  - questions
    - measure input or output?
    - input is correlated output? i.e. conversion rate
  - example
    - leading:
      - hours spent practising SQL
      - cost of ads spent on an impression
    - lagging:
      - job offers received
      - how many students got better jobs from the lessons
      - a testimonial or a repeat purchase
    - conversion rate: 
      - hours applying divided by job interviews
+ funnel
  - create a flow of an objective
  - each layers in the flow can have its own metrics
    - think through a product manager view: what spark joy or pain for users
  - example
    - impression -> sign ups/ get a contact -> purchase -> engaged/ retained -> referal/ testimonial 






















