# Final task
### Team: ETL-Express

## Personas

### Data engineer

![](diagrams/data-engineer.png)

#### Description:

Alexei, a 27-year-old data engineer based in Moscow, works at a big e-com company. With a Master's degree in Computer Science from Higher School of Economics, Alexey works as a data engineer in a large e-com company. He earns 350,000₽ per month.
Alexei's primary focus is on efficiently processing and cleaning large volumes of transactional data for downstream analytics. His main motivation is to automate data pipelines to reduce manual workload and enhance data quality. Now he is facing a number of challenges: he spends an excessive amount of time on manual data cleaning, struggles with inconsistent data formats, and finds it difficult to integrate data from multiple sources.
Alexei discovers a new ETL service that automates data extraction, transformation, and anonymization. By implementing this solution, he streamlines his workflows, enabling him to focus on more strategic tasks like optimizing data models.



### Data scientist

![](diagrams/data-scientist.png)

#### Description:


Svetlana, a 29-year-old data scientist based in Saint Petersburg, works at a healthcare startup. With a PhD in Data Science from Moscow State University, Svetlana is deeply committed to advancing her field by developing predictive health models. She earns 300,000₽.
Svetlana's key need is access to high-quality, anonymized patient data that allows her to create accurate and reliable predictive models for healthcare. Her main motivation is to minimize the time spent on data preprocessing, so she can focus more on developing and refining algorithms. However, she encounters several challenges: she often works with incomplete or disorganized datasets and has considerable concerns about adhering to data privacy regulations.
Svetlana adopts a new ETL service designed to provide clean and anonymized datasets. This solution reduces her data preparation time and ensures compliance with privacy laws, allowing her to accelerate the development of predictive models and focus on her core expertise.


### Database administrator

![](diagrams/database-admin.png)

#### Description:


Dmitry, a 35-year-old database administrator from Novosibirsk, works at a big e-com company. He holds a Master's degree in Information Systems from Moscow Institute of Physics and Technology. He earns 400,000₽ per month.
Dmitry's primary need is to ensure that sensitive customer data stored in databases is securely anonymized and efficiently prepared for analytics without the need for manual intervention. His main motivation is to automate data anonymization and transformation processes to comply with data privacy laws, while maintaining optimal database performance. He faces several challenges: he is overwhelmed by manual processes required for data masking and anonymization.
Dmitry discovers an ETL service that automates data extraction, anonymization, and loading processes. By integrating this service with his existing PostgreSQL databases, he successfully automates the anonymization of sensitive data, ensuring regulatory compliance. This solution also frees up his time to concentrate on enhancing database performance and security.


## Story map

![](diagrams/story-map-fixed.png)

## Use cases

![](diagrams/uc-fixed.png)


## Class candidates

| Candidate              | Criteria | Stored information                                                                                           | Operations                               |
| ---------------------- | -------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------- |
| Field                  | S        | Source, Name                                                                                                 |                                          |
| Script Repository      | UT       |                                                                                                              | Get, Update, Create (processing scripts) |
| Processing script      | SAT      | Fields, Released, Version                                                                                    | Run, Update                              |
| Extraction script      | SAT      | Fields, Released, Version                                                                                    | Run, Update                              |
| Extraction Service     | UT       |                                                                                                              | Extract                                  |
| Field Rule             | SAT      | Fields, Released, Version, DefaultValue, MinValue, MaxValue, Type                                            | Run, Update                              |
| Cleansing Service      | UT       |                                                                                                              | Clean                                    |
| FieldRuleType          | SU       | FillEmpty, IgnoreEmpty, RemoveEmpty, FillOutOfRangem IgnoreOutOfRange, RemoveOutOfRange                      |                                          |
| Transformation script  | SAT      | UpdateScript, Fields, Released, Version, Type                                                                | Run, Update                              |
| TransformationType     | SU       | Merge, Update                                                                                                |                                          |
| Transformation Service | UT       |                                                                                                              | Transform                                |
| AnonymizationRule      | SAT      | Fields, Released, Version, Type                                                                              | Run, Update                              |
| AnonymizationRule      | SU       | Generalization, Suppression, Anatomization, Permutation, Pertubation                                         |                                          |
| Anonymization Service  | UT       |                                                                                                              | Anonym                                   |
| Uploading script       | SAT      | Fields, Released, Version                                                                                    | Run, Update                              |
| Uploading service      | UT       |                                                                                                              | Upload                                   |
| Log                    | SAT      | Message, DateTime, Version                                                                                   |                                          |
| Log Repository         | UT       |                                                                                                              | Get, Add                                 |
| ETL-Task               | SAT      | Extraction script, Field rules, Transformation scripts, Anonymization rules, Uploading script, Version, Type | Process                                  |
| TaskState              | SU       | Pending, Running, Paused, Stopped, Finished                                                                  |                                          |
| ETL-Task Repository    | UT       |                                                                                                              | Get, Update, Create                      |
| ETL-Task Service       | UT       |                                                                                                              | Process, Pause, Stop                     |
| Data                   | ST       | Content                                                                                                      |                                          |
| Dataset                | ST       | Data list, Version                                                                                           |                                          |
| Dataset Repository     | UT       |                                                                                                              | Get, Create                              |

## Interaction analysis

| Use case         | Cooperation Name     | Used Roles       | Candidate classes                                                                                                                                                                                                                                                                                                                                |
| ---------------- | -------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Manage ETL-Tasks | ETL-Tasks Management | User             | ETL-Task Repositroy, ETL-Task Script Repository, Processing script, Extraction script, Field rule, Transformation script, Anonymization rule, Uploading script                                                                                                                                                                                   |
| Manage Scripts   | Scripts Management   | User             | Script Repository, Processing script, Extraction script, Field rule, Transformation script, Anonymization rule, Uploading script                                                                                                                                                                                                                 |
| Process ETL-Task | ETL-Task Processing  | User, Datamodule | ETL-Task Service, ETL-Task Repositroy, ETL-Task, Script Repository, Processing script, Extraction script, Field rule, Transformation script, Anonymization rule, Uploading script, Extraction Service, Cleansing Service, Transformation Service, Anonymization Service, Uploading Service, Dataset Repository Dataset Repository, Dataset, Data |
| Stop ETL-Task                | ETL-Task Stop            | User                       | ETL-Task Service, ETL-Task Repository                |
| View prepared data           | View data                | User                       | Dataset Repository, Dataset, Data                    |
| Manual managed prepared data | Prepared data management | User                       | Dataset Repository, Dataset, Data                    |
| Upload prepared data         | Upload data              | User, Destination Database | Uploading Service, Dataset Repository, Dataset, Data |
| Audit                        | Audit                    | User                       | Log, Log Repository                                  |


## Class diagram

![](diagrams/class-diagram-fixed.png)

## Detailed behavior - ETL Tasks & Scripts

![](diagrams/behavior-1.png)

## Detailed behavior - Manage ETL-Task & Scripts

![](diagrams/behavior-3.png)

## Detailed behavior - Data/Dataset

![](diagrams/behavior-2.png)

## Detailed behavior - Process ETL-Task

![](diagrams/behavior-4.png)



