# ETL-Express 

> ETL service that helps to deliver data from corporate systems to MLOps framework.

## DFD

![](diagrams/DFD.png)

## Class Diagram

![](diagrams/class-diagram.png)

## Data Glossary

1. **Data Source** - The origin from which data is extracted. Data sources can include databases, files, APIs, or other systems within the corporate infrastructure. The metadata specifies how to connect to and extract data from these sources using extraction scripts.

1. **Data Module** - A packaged unit of processed data that includes both the data itself and associated metadata. Data modules are stored in a relational database management system (RDBMS) like PostgreSQL or in S3 storage. Each data module is versioned and contains metadata compatible with JSON-LD, detailing the structure and processing rules of the data.

1. **Metadata** - Descriptive information associated with a data module that defines how data should be processed by the service. Metadata includes compulsory elements like table and column names, data types, null value handling strategies, and optional elements like value ranges. It also specifies scripts for data extraction and upload, and strategies for handling primary and foreign keys.

1. **Data Module Version** - A version identifier within the data module that tracks changes over time. Each time data is processed and the upload script is executed, the version number is updated. This allows users to reference specific iterations of the data module.

1. **Extraction script** - a script specified in the metadata as the script run by the service that produces records in the Pandas DataFrame form retrieved from an external database.

1. **Field (Column) rules** - information provided in the metadata related to the tables and columns used in the data module. This includes compulsory elements like table and column names, column data types, and null value handling strategies per column, as well as optional elements like value ranges for validation.

1. **Anonymization rules** - rules that are provided in the metadata for the table, which describe the process of data transformation to protect confidential data.

1. **Transformation script** - a script provided in the metadata for a specific table that describes the process of transforming data into a single data format.

1. **Upload script** - a script specified in the metadata file, run when the cleansing and anonymization of the data is complete, which puts the data into an external permanent storage(file or database) and updates the extraction script and data module version so that the cleansed data is now retrieved.