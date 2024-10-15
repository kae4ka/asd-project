# Task - 7
### Team: ETL-Express

## Description:

```
Solve behavior modeling tasks using UML2. This is a research and self-study activity. You will need to find out about new concepts using the references and links provided.

You will get individual points for studying and explaining new concepts to other students. Prepare a short 5-7 minutes report on the topic. A report shall include a correct solution of the bullet from the task as an example. 

The most elaborate and precise report for each new concept gets the point.

A team gets a project point if it correctly solves all of the tasks and bullets in a chosen category. 

There are a total of eight new concepts in four modeling tasks (one in a bullet). There are three categories. No more than four teams per category. You may coordinate concepts and categories with the other teams. Please, at most two reports on the same concept.

There is an extra Task 3 for activity modeling. Solve it at will.

Results of the task include
- a PDF with solved tasks in the chosen category and rationale for the solution
- a video recording with an explanation of a new concept (if not reported at class)
```

## Task - 1

![](diagrams/1-base.png)


![](diagrams/1-a.png)

### Description:

Added an association between two classes Salesman and Customer

![](diagrams/1-b.png)

### Description:

Created a new cooperation, where the Intermediate Broker is connected to Salesman and Customer via the Sale cooperation from point A. When connected to Salesman, the Intermediate Broker acts as Customer, and when connected to Customer, it acts as Salesman.

![](diagrams/1-c.png)

### Description:

A visualization of cooperation is presented in the form of a sequence diagram.

![](diagrams/1-d.png)

### Description:

In the cooperation diagram from point B, we add an indication that there can be many brokers and they interact with several salesmen and customers.

## Task - 2

![](diagrams/2-base.png)

![](diagrams/2-a.png)

### Description:

We change the parameter of the pressButton method from integer to enum, where enum consists of values ​​from 1 to 5. We also limit the number of executions in the cycle to a maximum of 5 repetitions.

![](diagrams/2-b.png)

### Description:

Added pressDoors() before pressButton() is called.

![](diagrams/2-c.png)

### Description:

For each iteration of the loop we attach ignore to the call to pressDoors

![](diagrams/2-d.png)

### Description:

We impose a duration constraint on the execution of the iteration between the startMoving and floorReached operations

![](diagrams/2-e.png)


## Task - 4

![](diagrams/4-base.png)

![](diagrams/4-a.png)

### Description:

Added new states TakeOff and Landing. The diagram is looped on the transition to Landing -> Boarding, because we have no other conditions under which the transitions by states will stop.

![](diagrams/4-b.png)

### Description:

Updated TakeOff and Landing states to "do / radioComm" and "exit / freeRunway"

![](diagrams/4-c.png)

### Description:

We have transformed InAir into a complex state by adding a substate that is nested and orthogonal, which specifies a subchart for dinner service. The subchart includes a check to determine if the flight is expected to last more than 3 hours. If so, passengers are offered a meal at any point during the flight.


![](diagrams/4-d.png)

### Description:

Similar to point C, a new orthogonal region is added, where the transition by substates from Normal to Damaged is indicated. Since the condition does not specify what happens to the aircraft after damage, we assume that the statechart stops at this point and everything goes to the final state

![](diagrams/4-e.png)


![](diagrams/4-f.png)


![](diagrams/4-g.png)

## Task - 5

![](diagrams/5-base.png)

![](diagrams/5-a.png)

![](diagrams/5-b.png)

### Desciption:

Added a new transition from Closed to ActiveOpen and then to Established.

![](diagrams/5-c.png)

### Description:

Added an additional transition from the PassiveClose state to the FinalState by the close event, from the SYN_RCVD state by the close event added a new transition to the ActiveClose state, in addition, a new transition from the ActiveOpen state to the Closed state by the close event was added

![](diagrams/5-d.png)

### Description:

For transitions with effect, intermediate states were added, so the states SYN_RCVD / SYN + ACK were added on the transition from Listen to SYN_RCVD, SYN_RCVD / FIN on the transition from SYN_RCVD to ActiveClose, and PassieveClose / FIN on the transition from PassieveClose to FinalState
