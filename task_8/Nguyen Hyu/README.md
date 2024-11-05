## Requirements

 Python 3.13.0

---

## KWIC

Developed a solution for the Key Word in Context problem utilizing the " Implicit Invocation (Event-Driven)" architectural approach.

**Expected Input:**

Input the text, keyword and number of words around keyword.

**Expected Result:**

The program will produce a sorted list of contexts, with the keyword positioned at the each.

---

## 8 Queens

Developed a solution for the 8 Queens problem using the "Main/Subroutine with stepwise refinement (Shared Data)" architectural approach.

**Expected Input:**

Input size of the chessboard

**Expected Result:**

The program will output all solutions to the "8 Queens" problem.

---

## Comparision with [Tyukavkina Ekaterina](https://github.com/kae4ka/asd-project/tree/main/task_8/Tyukavkina%20Ekaterina) (ETL-Express) and [Zhulin Artem](https://github.com/kae4ka/asd-project/tree/main/task_8/Zhulin%20Artem) (ETL-Express)


| **Criteria**                          | **Method 1(ADT - KWIC/Eight Queens)**       | **Method 2 (Main/Subroutine - Eight Queens)**    | **Method 3 (Pipes-and-Filters - KWIC/Eigh Queens)**       | **Method 4 (Event-driven - KWIC)** |
|---------------------------------------|----------------------------------------------|-------------------------------------------------------|-------------------------------------------------------------|---------------------------------------------|
|  **Ease of Changing Algorithm**         | Easy (Encapsulated logic in classes)                | Moderate (Functions depend on each other)        | Difficult (Need to adjust data flow between modules)   | Moderate (Modules need to sync events) |
| **Ease of Changing Data Representation**  | Easy (Independent object structure)              | Difficult (Representation tied to multiple functions)             | Difficult (Need to update the entire filter chain)     | Easy (Each module listens to events with minimal data constraints) |
|  **Ease of Adding New Functions**            | Easy (Can add new methods to class)     | Moderate (New functions need to maintain linkage)    | Difficult (Each new function must handle additional data from filters)   | Easy (New events can be added without affecting other modules) |
| **Performance**                      | High (Reduced overhead due to OOP)          | Moderate (Recursion may add overhead)               | Low (Time cost of passing data through filters)           | High (Event-driven can optimize for async tasks) |
| **Reusability**           | High (Objects are easily reusable)            | Moderate (Requires modification when expanded or reused)  | Low (Structure tied to specific pipeline and filters)     | High (Independent modules, easily extensible) |


