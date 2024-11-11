# Running

Copy file localy and execute command:

```
python main.py
# or
python3 main.py
```

# KWIC

This solution uses **Pipes and filters approach**.

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

# Queens

This solution uses **Abstract Data Types approach**.

To address this issue, we have chosen to categorize the data into the following categories:
1. **ChessPiece**: An abstract class that represents the general behavior of chess pieces, including potential future developments where not only queens, but other pieces may be involved.
2. **Queen**: A subclass of ChessPiece that simulates the specific behavior of queens as chess pieces.
3. **Board**: Another class that simulates a chessboard.
4. **QueenSolver**: A specific class dedicated to finding solutions to the given problem.

## Comparision with [Tyukavkina Ekaterina](https://github.com/kae4ka/asd-project/blob/main/task_8/Tyukavkina%20Ekaterina/8q.ipynb) 

| Criteria                                      | Abstract Data Types (Method 1) | Pipes-and-Filters (Method 3) | Explanation                                                                                                                                                                                                                |
|-----------------------------------------------|--------------------------------|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ease of changing the implementation algorithm | Moderate                       | High                         | Method 1 organizes functionality within objects, requiring changes in specific class methods to modify the algorithm. Method 3, using independent functions, enables changes to individual steps without impacting others. |
| Ease of changing data representation          | High                           | Low                          | Method 1 allows encapsulation within objects, enabling flexible data representation changes. Method 3 relies on a common data format across steps, making changes to data representation more challenging.                 |
| Ease of adding additional functions           | Moderate                       | High                         | Adding functions in Method 1 often requires adding methods to existing classes or creating new classes. In Method 3, functions can be added as additional steps in the pipeline with minimal effort.                       |
| Performance                                   | High                           | Low                          | Method 1 benefits from structured data handling within objects, which can be more efficient. Method 3, with multiple functional steps, may introduce additional processing overhead, especially with high data volume.     |
| Preference for reuse                          | Moderate                       | High                         | Method 1 is more suited for applications requiring complex data handling within a structured framework. Method 3 is ideal for tasks that benefit from modularity and independent processing steps.                         |

## Comparision with [Nguyen Hyu](https://github.com/kae4ka/asd-project/blob/main/task_8/Nguyen%20Hyu/8Q.py)

| Criteria                                      | Abstract Data Types (Method 1)             | Main/Subroutine (Method 2)              | Explanation                                                                                                                                                                                                                        |
|-----------------------------------------------|--------------------------------------------|-----------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ease of changing the implementation algorithm | Moderate                                   | Low                        | Method 1 organizes functionality within classes, allowing localized changes to class methods. In Method 2, changes may affect multiple steps as functions rely on shared data and a fixed sequence.                                |
| Ease of changing data representation          | High                                       | Moderate                                | Method 1 uses encapsulated objects, making it easy to alter data representation within each class. Method 2 shares data across steps, so changes in data representation could require adjustments throughout the entire procedure. |
| Ease of adding additional functions           | Moderate                                   | Low                                     | Adding functions in Method 1 often involves creating new methods or classes without affecting others. In Method 2, additional functionality may require restructuring the main subroutine and possibly the shared data structure.  |
| Performance                                   | High                                   | High                                    | Method 1, with object handling, might involve slight overhead, especially in larger applications. Method 2 can perform efficiently by directly using shared data with minimal object overhead, making it potentially faster.       |
| Preference for reuse                          | Moderate | Low | Method 1 is more suitable for modular designs with encapsulated data. Method 2 is preferable for straightforward tasks requiring direct access to shared data with a simple procedural flow.                                       |



