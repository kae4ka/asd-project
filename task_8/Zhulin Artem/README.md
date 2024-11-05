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
| Ease of changing data representation          | Low                            | Moderate                       | Method 1 supports encapsulated data structures, making changes in data representation relatively straightforward. In Method 3, data must conform to a common structure across filters, limiting flexibility.        |
| Ease of adding additional functions           | High                           | Moderate                       | Adding functions in Method 1 often means modifying existing classes or creating new ones, potentially increasing complexity. In Method 3, additional filters can be appended with minimal changes to existing code. |
| Performance                                   | Low                            | Moderate                       | Method 1 may be more efficient due to fewer intermediate data transformations. Method 3 may incur overhead from multiple filter executions, impacting performance depending on data volume.                         |
| Preference for reuse                          | High                           | Low                            | Method 1 is reusable in scenarios with complex data manipulation needs. Method 3 is reusable for cases prioritizing modularity, flexibility, and independent function chaining.                                     |

## Comparision with []() 
