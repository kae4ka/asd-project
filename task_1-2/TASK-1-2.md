# Task - 1, 2
### Team: ETL-Express

## Description:

```
Task 1

Form a team, come up with a name for the team.

Select tools for the team to develop a software product:
Repo (n.b. Github may ban)
Task tracker 
Wiki/docs storage
Team chat
Modeling tool (see https://tiny.cc/asd-tools)

Task 2

Define product scope as a product customer (“business requirements”). Name the product.

Reminder:

Product name
List of team members

Product description

E.g. My Custom Printer is a mobile app for office workers to quickly print documents from a smartphone over wifi or bluetooth. … 

Similar systems [if topic is new]

e.g. Super Printer App, …

Feature list

Feature 1 (Name + 3-5 sentences)
Feature 2 (Name + 3-5 sentences)
Print a document. Users can print documents on an installed printer using a print dialog.

Constraints

Any technical constraints and requirements

Result - a doc in your repo/wiki, post a link in the course chat.

Scope description - 5-10 sentences.
List of features - 7-12 features.

Report on the product at the blackboard.

```

# ⚡ ETL-Express 

> ETL service that helps to deliver data from corporate systems to MLOps framework.
## Team
- *Tyukavkina Ekaterina*
- *Zhulin Artem*
- *Nguyen Huy*
- *Kuzmin Maxim*
## Project name
ETL service for private data cleansing
## Table of contents 📌
1. [Summary](#summary)
2. [Stakeholders](#stakeholders)
3. [Features](#features)
4. [Constraints](#constraints)
5. [Implementation rules](<#implementation-rules>)
6. [Non-functional requirements](<#non-functional-requirements>)
## Summary
>*This project focuses on developing a complex and large-scale ETL (Extract, Transform, Load) service aimed at cleaning and securing private data. The service will extract data from the company's internal systems, then clean, consolidate, anonymize, and transform the data before loading it into a new version of a data module. These data modules, stored on S3 or in a relational database management system (RDBMS), are described by metadata compatible with json-ld, a data gathering protocol, and versioned data. After the ETL process is complete, the data modules can be utilized by machine learning applications deployed on the framework. Ensuring data quality and accessibility is crucial for the applications operating within this framework.*
## Stakeholders
###### Customer
- **End Users:** Individuals or organizations using the processed data modules for machine learning applications and other purposes. They require secure, privacy-protected, and high-quality data.
###### User
- **Data Scientists:** Use cleaned and anonymized data to perform analysis and build machine learning models. They need accurate and relevant data for analysis.
- **Business Analysts:** Utilize processed data to make strategic decisions. They demand reliable data that meets security standards.
###### Funder
- **Management:** Manage and provide financial resources for the project, while also overseeing the progress and effectiveness of the ETL service implementation.
###### Team
- **Data Engineers:** Design, implement, and maintain ETL processes. They need a robust, complex service that easily integrates with existing systems.
- **Data Security Specialists:** Ensure that the ETL service complies with security and privacy regulations. They are responsible for protecting data throughout the processing stages.
###### Management
- **Legal and Compliance Teams:** Ensure that the project complies with data privacy laws and the company's internal policies.
###### Government
- **Government:** Monitor compliance with legal regulations on privacy and data security (such as GDPR, CCPA) during the implementation of the ETL service.
###### Society
- **Society:** Benefits from the protection of private data and individual rights, ensuring that services and technologies develop in line with ethical and general security standards.
## Features

1. **Table Handling**:
The service should be able to work with tables. The tables will contain columns, which correspond to names for a particular class of values and have a data type provided, and records, which are collections of (possibly empty) values matched to columns. A column is always mapped to a table, so that columns with the same name in different tables are always considered different columns.

2. **Data Modules Management**:
The service should support data modules that contain metadata, the data collection protocol and the version of the module.

3. **Empty Field Processing**:
The metadata should contain the names of tables and columns that will be taken by the service and transformed. The strategy for filling empty fields in a particular column will be provided in the column description in the metadata. The supported strategies will be ignoring the empty value and passing it into the service unchanged, replacing empty values in a particular column with a provided value, or not passing a record with an empty value in a given column into the service.

4. **Range Validation**:
The metadata may contain the allowed value ranges for each column, provided per-column. If such range is provided for a column, the metadata must also specify the strategy of dealing with records that do not conform to the value restriction. Removing the record from the service and replacing the violating value with the maximum or minimum allowed value will be supported.

5. **Primary Key Management**:
The metadata should allow a particular column to be specified as a primary key, meaning the values of that key are unique among all the records processed by the service. If a primary key is specified in the metadata, a strategy for working with records that have the same values of the primary key must be specified in the metadata. The supported options will be adding priorities for sources, so that the record from the highest-ranking conflicting source is processed by the service, removing all records with a conflicting primary key from the service, and adding all records but generating new primary keys for them.

6. **Foreign Key Management**:
The metadata should allow a particular column to be designated a foreign key and mapped to a column in a different table specified in the metadata. The value of a foreign key must be a value that is present in the specified column of the different table, otherwise the record should be removed from the service.

7. **Anonymization Methods**:
All data processed by the service will be anonymized using the well-known generalization, suppression, anatomization, permutation, and perturbation operations.

8. **Data Collection Process**:
The collection protocol in the metadata lists scripts for all tables mentioned in the metadata. Several scripts can be listed for the same table name, in this case the service will merge the data from different sources into one entity according to the rules specified in the metadata. The scripts should return the data they retrieved in the JSON format.

9. **Data Upload and Version Control**:
The data module should contain a data upload script, which will be executed after the data is processed. It should either work in a way that the collection protocol specified in the data module retrieves the new processed data after the upload script completes or rewrite the collection protocol of the data module so that the new collection protocol works with the uploaded data. The data upload script should also update the version part of the data module.

10. **Auditing Logging**:
All operations performed by the service will be recorded in a log for auditing purposes. This logging ensures transparency, traceability, and compliance with applicable standards and regulations.


## Constraints
1. **Data storage:** All data must be stored in a relational database management system (RDBMS) (PostgreSQL).
2. **Unrecoverable anonymization:** The anonymization process should be unrecoverable to ensure protection of confidential data.
3. **Service architecture modularity and scalability:** The architecture should be modular and scalable without requiring a full system overhaul.
4. **Integration with corporate systems:** The service should support integration with other corporate systems without requiring changes to their architectures.
## Implementation rules
###### Documentation
- When the Contractor designs a data module of the service, he documents it's logic in corporate knowledge base of the Customer
	- Metric: Each data module has at least 50 words of description of it's logic
###### Security
- When the Contractor designs a data module of the service, he does not hardcode credentials in source code and uses corporate secrets storage instead
- GitHub Secrets must be supported as a secret storage option
###### Scalability
- The service must have an opportunity to be connected to new data sources or to be expanded with new modules
- The service must have a common class for similar data sources and a template for new modules
###### Maintainability
 - When the Contractor designs a data module of the service, he implements comprehensive error handling and logging mechanisms.
	 - Metric: The service stores logs for the last 30 days.
###### Data quality
- When the Contractor designs a data module of the service, he implements tests for possible data loss, or data duplicating, or empty values.
- The service must ensure that data from various data sources have a commot data format.
- The service outputs JSON-like objects.
###### Reliability
- The Contractor must use Russian or open-source infrastructure and tools for the service developing.
- The service must always deliver reliable and up-to-date data.
	- Metric: The service is scheduled somewhere (Airflow) and runs every day.
## Non-functional requirements
###### Performance
  - Description: The service must be able to process large volumes of data in a timely manner.
	  - Metric: The processing time for 1 TB of data should be less than 24 hours.
###### Scalability
  - Description: The service should support both horizontal and vertical scaling to accommodate increasing data volumes.
	  - Metric: It should be able to handle a 100% increase in data with no more than 20% additional response time (RT).
###### Reliability
  - Description: To ensure accurate data processing, the service must minimize errors.
	  - Metric: Error rate should be no more than 0.01% of total transactions.
###### Availability
  - Description: The service should be available 24/7.
	  - Metric: Availability should be at least 99.9% for a 24-hour period.
###### Recoverability 
  - Description: In the event of a failure, the service should automatically recover and resume processing from the last valid state.
	  - Metric: The recovery time after a system failure should not be more than 5 minutes.
