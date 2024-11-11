# ETL-Express 

> ETL service that helps to deliver data from corporate systems to MLOps framework.

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


