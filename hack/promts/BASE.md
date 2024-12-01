# Base

We have an ETL system project. The following technology stack was previously selected for implementation:
API definition - gRPC
Programming language - python
App framework - Django
Serialization/state format - protobuf + json
Database - postgreSQL
Testing tools - pytest
CI/CD pipeline - Github Actions
Delivery method - Docker
Monitoring - Grafana

Here this small project description.

This project focuses on developing a complex and large-scale ETL (Extract, Transform, Load) service aimed at cleaning and securing private data. The service will extract data from the company's internal systems, then clean, consolidate, anonymize, and transform the data before loading it into a new version of a data module. These data modules, stored on S3 or in a relational database management system (RDBMS), are described by metadata compatible with json-ld, a data gathering protocol, and versioned data. After the ETL process is complete, the data modules can be utilized by machine learning applications deployed on the framework. Ensuring data quality and accessibility is crucial for the applications operating within this framework.

Features:

1. Table Handling: The service should be able to work with tables. The tables will contain columns, which correspond to names for a particular class of values and have a data type provided, and records, which are collections of (possibly empty) values matched to columns. A column is always mapped to a table, so that columns with the same name in different tables are always considered different columns.

2. Data Modules Management: The service should support data modules that contain metadata, the data collection protocol and the version of the module.

3. Empty Field Processing: The metadata should contain the names of tables and columns that will be taken by the service and transformed. The strategy for filling empty fields in a particular column will be provided in the column description in the metadata. The supported strategies will be ignoring the empty value and passing it into the service unchanged, replacing empty values in a particular column with a provided value, or not passing a record with an empty value in a given column into the service.

4. Range Validation: The metadata may contain the allowed value ranges for each column, provided per-column. If such range is provided for a column, the metadata must also specify the strategy of dealing with records that do not conform to the value restriction. Removing the record from the service and replacing the violating value with the maximum or minimum allowed value will be supported.

5. Primary Key Management: The metadata should allow a particular column to be specified as a primary key, meaning the values of that key are unique among all the records processed by the service. If a primary key is specified in the metadata, a strategy for working with records that have the same values of the primary key must be specified in the metadata. The supported options will be adding priorities for sources, so that the record from the highest-ranking conflicting source is processed by the service, removing all records with a conflicting primary key from the service, and adding all records but generating new primary keys for them.

6. Foreign Key Management: The metadata should allow a particular column to be designated a foreign key and mapped to a column in a different table specified in the metadata. The value of a foreign key must be a value that is present in the specified column of the different table, otherwise the record should be removed from the service.

7. Anonymization Methods: All data processed by the service will be anonymized using the well-known generalization, suppression, anatomization, permutation, and perturbation operations.

8. Data Collection Process: The collection protocol in the metadata lists scripts for all tables mentioned in the metadata. Several scripts can be listed for the same table name, in this case the service will merge the data from different sources into one entity according to the rules specified in the metadata. The scripts should return the data they retrieved in the JSON format.

9. Data Upload and Version Control: The data module should contain a data upload script, which will be executed after the data is processed. It should either work in a way that the collection protocol specified in the data module retrieves the new processed data after the upload script completes or rewrite the collection protocol of the data module so that the new collection protocol works with the uploaded data. The data upload script should also update the version part of the data module.

10. Auditing Logging: All operations performed by the service will be recorded in a log for auditing purposes. This logging ensures transparency, traceability, and compliance with applicable standards and regulations.



Use-cases:

### Use Case: Login

**Description:** The user logs into the ETL service using an external Single Sign-On (SSO) system for authentication.

1. **Primary Actor:** User
1. **Goals:** Gain authorized access to the ETL service
1. **Pre-conditions:** User has valid credentials with the external SSO provider
1. **Post-conditions:** User is authenticated and granted access to the ETL service's functionalities

**Basic Flow:**

1. **Access Login Page:**
   1. User navigates to the ETL service login page.
   1. System displays the login interface.
2. **Redirect to SSO Provider:**
   1. User selects the option to log in via the external SSO provider.
   1. System redirects the user to the SSO provider's authentication page.
3. **Authenticate with SSO:**
   1. User enters their SSO credentials and submits.
   1. SSO provider authenticates the user.
4. **Return to ETL Service:**
   1. SSO provider redirects the user back to the ETL service with authentication tokens.
5. **Establish Session:**
   1. System validates the authentication tokens.
   1. System establishes a session for the user.
   1. User gains access to the ETL service's dashboard and features.

**Note:** Authentication is handled externally; no backend methods are invoked within the ETL service for this use case.

---

### Use Case: Manage Scripts

**Description:** The Task-Editor manages scripts required for ETL processing by utilizing the `ScriptManager` service, including creating, updating, releasing, and retrieving scripts.

1. **Primary Actor:** Task-Editor
1. **Goals:** Create, update, release, and manage scripts for extraction, field rules application, transformation, anonymization, and uploading
1. **Pre-conditions:** User must be logged into the service
1. **Post-conditions:** Scripts are created, updated, or released successfully, ready for use in ETL tasks

**Basic Flow:**

1. **Access Script Management:**
   1. Task-Editor navigates to the script management section in the ETL service interface.
2. **Check Permissions:**
   1. System verifies the Task-Editor's permissions to manage scripts.
   1. (Access verification may involve backend call) *(GetUser - UserManager)*
3. **View Script Options:**
   1. System presents options to create a new script or edit an existing one.
4. **Select Action:**
   1. Task-Editor chooses to create a new script or modify an existing script.
5. **Create New Script:**
   1. If creating, Task-Editor inputs script details such as type and properties.
   1. Task-Editor submits the new script.
   1. System processes the creation request.
   1. *(CreateScript - ScriptManager)*
6. **Edit Existing Script:**
   1. If editing, Task-Editor selects a script to modify.
   1. System retrieves script details.
   1. *(GetScript - ScriptManager)*
   1. Task-Editor updates the script information.
   1. Task-Editor submits the updates.
   1. System processes the update request.
   1. *(UpdateScript - ScriptManager)*
7. **Release Script:**
   1. Task-Editor may choose to release the script for use in ETL tasks.
   1. Task-Editor initiates the release action.
   1. System processes the release.
   1. *(ReleaseScript - ScriptManager)*
8. **Confirmation:**
   1. System confirms that the script is saved and ready for integration.
   1. Task-Editor receives confirmation message.

**Alternate Path:**

- **Validation Errors:**
  1. If the system detects invalid inputs, it informs the Task-Editor and prompts for corrections before proceeding.

---

### Use Case: Manage ETL Task

**Description:** The Task-Editor creates and configures an ETL task by using the `EtlTaskManager` service, including adding scripts via update methods.

1. **Primary Actor:** Task-Editor
1. **Goals:** Create, configure, and update ETL tasks by adding relevant scripts
1. **Pre-conditions:** User must be logged into the service
1. **Post-conditions:** ETL task is created or updated with all necessary scripts, ready for execution

**Basic Flow:**

1. **Access ETL Task Management:**
   1. Task-Editor navigates to the ETL task management section.
2. **Check Permissions:**
   1. System verifies Task-Editor's permissions to manage ETL tasks.
   1. *(GetUser - UserManager)*
3. **Create or Select Task:**
   1.  Task-Editor chooses to create a new ETL task or select an existing one to update.
   1.  If creating, Task-Editor provides basic task details and submits.
   1.  *(CreateTask - EtlTaskManager)*
   1.  If updating, Task-Editor selects the task to modify.
   1.  System retrieves task details.
   1.  *(GetTask - EtlTaskManager)*
4. **Configure Task Scripts:**
   1. Task-Editor attaches relevant scripts to the task:
     1. Adds or updates the Extraction script.
       1. *(UpdateExtractionScript - EtlTaskManager)*
     1. Adds or updates Field Rules.
       1. *(UpdateFieldRules - EtlTaskManager)*
     1. Adds or updates Anonymization rules.
       1. *(UpdateAnonymizationRules - EtlTaskManager)*
     1. Adds or updates Transformation scripts.
       1. *(UpdateTransformationScripts - EtlTaskManager)*
     1. Adds or updates Uploading script.
       1. *(UpdateUploadingScript - EtlTaskManager)*
5. **Finalize Configuration:**
   1. Task-Editor reviews the task setup.
   1. Task-Editor saves the task configuration.
6. **Release Task:**
   1. Task-Editor may release the task to make it ready for execution.
   1. *(Release - EtlTaskManager)*
7. **Confirmation:**
   1. System validates the task setup.
   1. System confirms the task is ready for execution.

**Alternate Path:**

1. **Missing Scripts:**
  1. If required scripts are not attached, system alerts Task-Editor to complete the setup before the task can be released.

---

### Use Case: Manage External Datamodule Connection

**Description:** The user creates and configures connections to external datamodules by using the `ExtDatamoduleManager` service.

1. **Primary Actor:** User
1. **Goals:** Establish and manage connections to external datamodules for data extraction or interaction
1. **Pre-conditions:** User must be logged into the service and have necessary permissions
1. **Post-conditions:** A new external datamodule connection is created or updated and saved, ready for use in ETL tasks

**Basic Flow:**

1. **Access Connection Management:**
   1. User navigates to the "Manage External Datamodule Connections" section.
2. **Check Permissions:**
   1. System verifies user's permissions to manage connections.
   1. *(GetUser - UserManager)*
3. **Create or Edit Connection:**
   1. User chooses to create a new connection or edit an existing one.
4. **Provide Connection Details:**
   1. User enters necessary information:
     1. Datamodule contract details.
     1. Connection string.
     1. Connection type (e.g., SQL, gRPC, API).
     1. Assigns owners for the connection.
5. **Submit Configuration:**
   1. User submits the connection configuration.
6. **Process Request:**
   1. System validates the input for correctness and conflicts.
   1. System saves the new or updated connection.
   1. *(CreateConnection or UpdateConnection - ExtDatamoduleManager)*
7. **Confirmation:**
   1. System confirms the connection is ready for use.
   1. Notifies assigned owners if applicable.

---

### Use Case: Get External Datamodule Access

**Description:** The user requests access to an existing external datamodule connection by sending a request to the connection's owners via the `UserManager` service.

1. **Primary Actor:** User
1. **Goals:** Obtain permission to use a specific external datamodule connection
1. **Pre-conditions:** User must be logged into the service; the connection exists
1. **Post-conditions:** An access request is sent to the connection's owners for approval

**Basic Flow:**

1. **View Available Connections:**
   1. User navigates to the list of external datamodule connections.
   1. System displays available connections with access status.
   1. *(GetAllConnection - ExtDatamoduleManager)*
2. **Select Connection:**
   1. User identifies a connection they need access to.
3. **Request Access:**
   1. User selects "Request Access" for the chosen connection.
   1. System prompts for reason or additional details.
4. **Submit Request:**
   1. User submits the access request.
   1. System records the request.
   1. *(AddAccess - UserManager)*
5. **Notify Owners:**
   1. System sends notification to the connection's owners.
6. **Confirmation:**
   1. User receives acknowledgment that the request has been sent.

---

### Use Case: Approve External Datamodule Access

**Description:** The connection owners review and approve or deny access requests from users via the `UserManager` service.

1. **Primary Actor:** Connection Owner
1. **Goals:** Manage access requests by approving or denying user requests
1. **Pre-conditions:** Connection owner must be logged into the service; pending access requests exist
1. **Post-conditions:** User access is granted or denied; requester is notified

**Basic Flow:**

1. **Receive Notification:**
   1. Connection owner is notified of a pending access request.
2. **Access Access Requests:**
   1. Owner navigates to the "Access Requests" section.
3. **Check Permissions:**
   1. System verifies owner's permissions for the connection.
   1. *(GetUser - UserManager)*
4. **Review Request:**
   1. System displays pending requests with details.
   1. Owner reviews the requester's information and reason.
5. **Make Decision:**
   1. Owner chooses to approve or deny the request.
6. **Submit Decision:**
   1. Owner submits their decision.
   1. *(ApproveAccessRequest - UserManager)*
7. **Update Permissions:**
   1. System updates access permissions accordingly.
8. **Notify Requester:**
   1. System sends notification to the requester with the decision.

---

### Use Case: Process ETL Task

**Description:** The Task-Manager initiates the processing of an ETL task by using the `EtlTaskManager` service, and the system executes the ETL processing steps.

1. **Primary Actor:** Task-Manager
1. **Goals:** Execute ETL processing, prepare data for eventual upload
1. **Pre-conditions:** ETL task is fully configured and validated
1. **Post-conditions:** Data is processed and stored, awaiting user confirmation for upload

**Basic Flow:**

1. **Initiate Task Processing:**
   1. Task-Manager selects an ETL task to process.
2. **Check Permissions:**
   1. System verifies Task-Manager's permissions.
   1. *(GetUser - UserManager)*
3. **Start ETL Task:**
   1. Task-Manager initiates the task processing.
   1. *(Start - EtlTaskManager)*
4. **Execute Extraction:**
   1. System runs the Extraction script to pull data.
5. **Apply Field Rules:**
   1. System applies Field Rules to clean and standardize data.
6. **Run Transformation:**
   1. System executes Transformation scripts.
7. **Apply Anonymization:**
   1. System applies Anonymization rules to data.
8. **Store Processed Data:**
   1. System saves the processed data in the Outbox.
9. **Confirmation:**
   1. System notifies Task-Manager that processing is complete.

**Alternate Path:**

1. **Processing Error:**
  1. If an error occurs, system logs the error.
  1. System informs Task-Manager of the issue.
  1. Processing is halted.

---

### Use Case: Stop ETL Task

**Description:** The Task-Manager can pause or completely stop an ETL task using the `Pause` or `Stop` methods in the `EtlTaskManager` service and decide on handling data in the Outbox.

1. **Primary Actor:** Task-Manager
1. **Goals:** Pause or terminate an active ETL task
1. **Pre-conditions:** ETL task is in progress
1. **Post-conditions:** ETL task is paused or terminated; Outbox data is handled as per user choice

**Basic Flow:**

1. **Initiate Stop/Pause:**
   1. Task-Manager chooses to pause or stop the ETL task.
2. **Check Permissions:**
   1. System verifies Task-Manager's permissions.
   1. *(GetUser - UserManager)*
3. **Execute Command:**
   1. System processes the pause or stop command.
   1. *(Pause or Stop - EtlTaskManager)*
4. **Handle Outbox Data:**
   1. If stopping, system prompts Task-Manager to confirm deletion of Outbox data.
   1. Task-Manager decides whether to clear the data.
5. **Process Decision:**
   1. System deletes Outbox data if confirmed.
6. **Confirmation:**
   1. System confirms the task is paused or stopped.

---

### Use Case: View Run History

**Description:** The user views the history of executed ETL tasks by retrieving audit logs using the `AuditLogger` service.

1. **Primary Actor:** User
1. **Goals:** Monitor and review the execution history of ETL tasks, including performance metrics
1. **Pre-conditions:** User must be logged into the service
1. **Post-conditions:** User successfully views the run history and relevant details

**Basic Flow:**

1. **Access Run History:**
   1. User navigates to the "Run History" section.
2. **Retrieve Audit Logs:**
   1. System fetches audit logs related to ETL tasks.
   1. *(ListAuditLogs - AuditLogger)*
3. **Display Summary:**
   1. System displays a list of executed tasks with summaries.
4. **View Details:**
   1. User selects a task to view more information.
   1. System retrieves detailed log.
   1. *(GetAuditLog - AuditLogger)*
5. **Present Information:**
   1. System displays execution details, data processed, and current state.

---

### Use Case: View Prepared Data

**Description:** The Data-Manager reviews data that has been processed and saved in the Outbox by using the `DataManager` service.

1. **Primary Actor:** Data-Manager
1. **Goals:** Access and review processed data
1. **Pre-conditions:** Processed data is available in the Outbox
1. **Post-conditions:** User can view data details stored in the Outbox

**Basic Flow:**

1. **Access Outbox:**
   1. Data-Manager navigates to the Outbox section.
2. **Check Permissions:**
   1. System verifies Data-Manager's permissions.
   1. *(GetUser - UserManager)*
3. **Retrieve Data Entries:**
   1. System fetches a list of processed data.
   1. *(GetAll - DataManager)*
4. **Select Data Entry:**
   1. Data-Manager selects a data entry to view.
5. **View Details:**
   1. System displays detailed information of the selected data.

---

### Use Case: Manage Prepared Data

**Description:** The Data-Manager manages the processed data in the Outbox by using the `Modifie` method in the `DataManager` service to add, edit, or delete entries.

1. **Primary Actor:** Data-Manager
1. **Goals:** Modify or manage prepared data entries in the Outbox
1. **Pre-conditions:** Processed data entries are available in the Outbox
1. **Post-conditions:** Data is updated, added, or removed as per user instructions

**Basic Flow:**

1. **Access Data Management:**
   1. Data-Manager navigates to the data management section in Outbox.
2. **Check Permissions:**
   1. System verifies Data-Manager's permissions.
   1. *(GetUser - UserManager)*
3. **Select Action:**
   1. Data-Manager chooses to add, edit, or delete a data entry.
4. **Perform Action:**
   1. Data-Manager makes the desired changes.
   1. Submits the modifications.
   1. *(Modifie - DataManager)*
5. **Process Changes:**
   1. System validates and applies the changes.
6. **Confirmation:**
   1. System confirms that the data has been updated.

---

### Use Case: Upload Prepared Data

**Description:** The Task-Manager decides to upload processed data from the Outbox to the destination by initiating the upload process using the `Start` or `Resume` methods in `EtlTaskManager`.

1. **Primary Actor:** Task-Manager
1. **Goals:** Confirm and initiate data upload from the Outbox
1. **Pre-conditions:** Data is processed and available in the Outbox
1. **Post-conditions:** Data is uploaded to the destination or handled based on user action

**Basic Flow:**

1. **Review Prepared Data:**
   1. Task-Manager reviews data entries in the Outbox.
   1. *(GetAll - DataManager)*
2. **Initiate Upload:**
   1. Task-Manager decides to upload the data.
   1. Starts the upload process.
   1. *(Start or Resume - EtlTaskManager)*
3. **Check Permissions:**
   1. System verifies Task-Manager's permissions.
   1. *(GetUser - UserManager)*
4. **Execute Uploading Script:**
   1. System runs the Uploading script attached to the task.
5. **Transfer Data:**
   1. Data is transferred to the destination service.
6. **Update Outbox:**
   1. System marks the data as uploaded.
7. **Confirmation:**
   1. System notifies Task-Manager of successful upload.

**Alternate Path:**

1. **No Action Taken:**
  1. If Task-Manager takes no action, system retains data for a predefined period.
  1. After the retention period, system automatically deletes the data.

---

### Use Case: Audit

**Description:** The system records all actions by users and the system itself. Users can review the history of changes and actions by using the `AuditLogger` service.

1. **Primary Actor:** User
1. **Goals:** Track and review audit logs for all actions
1. **Pre-conditions:** Audit logs are enabled and accessible
1. **Post-conditions:** User can view a detailed record of actions in the system

**Basic Flow:**

1. **Access Audit Logs:**
   1. User navigates to the audit log section.
2. **Retrieve Logs:**
   1. System fetches audit logs.
   1. *(ListAuditLogs - AuditLogger)*
3. **Search and Filter:**
   1. User searches or filters logs based on criteria.
4. **Select Log Entry:**
   1. User selects specific entries to view details.
5. **View Details:**
   1. System displays action details, including timestamp, actor, and changes.
   1. *(GetAuditLog - AuditLogger)*

It is assumed that the project will include 6 main features:
1. ETL-Task Manager - ETL Task management: creating, modifying, adding scripts and running tasks.
2. Script Manager - Script management: creation, modification
3. Data Manager - Executing ETL tasks, saving and managing prepared data, and sending it to the destination system.
4. ExtDataModule Manager - Describing connections to external storage systems.
5. User Manager - Managing user roles and access to external systems.
6. Audit Logger - Auditing user actions within the ETL system.

Just remember this information. Next, I will give you commands.
