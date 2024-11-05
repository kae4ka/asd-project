# Running

Copy file localy and execute command:

```
python main.py
# or
python3 main.py
```

# KWIC

This study uses the author's approach in the article by David Gahan and Mary Shaw : Pipes and filters.

## Comparision with [Tyukavkina Ekaterina](https://github.com/kae4ka/asd-project/blob/main/task_8/Tyukavkina%20Ekaterina/kwic.ipynb) 

|                    Criteria                   |  Pipes-and-Filters (Method 3)  | Abstract Data Types (Method 1) |                                                                                                     Explanation                                                                                                     |
|:---------------------------------------------:|:------------------------------:|:------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| Ease of changing the implementation algorithm | High                           | Moderate                       | In Method 1, changing the algorithm requires modifying class internals, which may be interdependent. Method 3 uses independent filters, making it easier to adjust or swap algorithms without affecting others.     |
| Ease of changing data representation          | Low                            | High                       | Method 1 supports encapsulated data structures, making changes in data representation relatively straightforward. In Method 3, data must conform to a common structure across filters, limiting flexibility.        |
| Ease of adding additional functions           | High                           | Moderate                       | Adding functions in Method 1 often means modifying existing classes or creating new ones, potentially increasing complexity. In Method 3, additional filters can be appended with minimal changes to existing code. |
| Performance                                   | Low                            | High                       | Method 1 may be more efficient due to fewer intermediate data transformations. Method 3 may incur overhead from multiple filter executions, impacting performance depending on data volume.                         |
| Preference for reuse                          | High                           | Moderate                            | Method 1 is reusable in scenarios with complex data manipulation needs. Method 3 is reusable for cases prioritizing modularity, flexibility, and independent function chaining.                                     |

## Comparision with [Pan Zhengwu (mETaL)](https://github.com/abrosov-sergey/Micro-SD/blob/main/Tasks/task8/Pan%20Zhengwu/Problem%20A/kwic.py) 

| Criteria                                      | Pipes-and-Filters (Method 3) | Main/Subroutine (Shared Data) (Method 2) | Explanation                                                                                                                                                                                                       |
|-----------------------------------------------|------------------------------|------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ease of changing the implementation algorithm | High                         | Moderate                                 | Method 2 uses a main control routine, so changes to individual algorithms impact interdependent modules. In Method 3, filters are independent, allowing easy modification of each stage without affecting others. |
| Ease of changing data representation          | Low                          | Moderate                                 | In Method 2, shared data structures allow flexible changes to data representation. Method 3 requires consistent data formats across filters, making representation changes more challenging.                      |
| Ease of adding additional functions           | High                         | Moderate                                 | In Method 2, adding functions often requires modifying the main control and other modules. Method 3’s modular filters can be added seamlessly to the pipeline, enhancing extensibility.                           |
| Performance                                   | Low                          | High                                 | Method 2’s centralized data handling can be more efficient. Method 3, with data moving through multiple filters, may experience overhead depending on filter complexity and data volume.                          |
| Preference for reuse                          | High                         | Low                                      | Method 2 is more suited for complex scenarios needing centralized data control. Method 3 is ideal for applications prioritizing modularity and ease of function chaining.                                         |

