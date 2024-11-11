# ETL-Express 

> ETL service that helps to deliver data from corporate systems to MLOps framework.


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