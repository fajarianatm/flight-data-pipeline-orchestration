# Automated Data Pipeline Project

This project is designed to automate the process of extracting data from a source database, temporarily storing it in an object store, and loading it into a data warehouse. The pipeline is orchestrated using Apache Airflow to ensure seamless and efficient task automation.


---
---

# Objective 

This repository demonstrates the development of an ELT (Extract, Load, Transform) pipeline, focusing on the following key aspects:

- Designing and implementing the ELT process
- Automating and orchestrating the pipeline using Apache Airflow

---

# Pipeline Workflow

Before diving into the details, please refer to the following diagram to understand the workflow used to construct this project.

![ELT_DESIGN](records/elt_design.png)

- ## How The Pipeline Works

The pipeline leverages Apache Airflow for orchestration and automation. The process involves three primary tasks:

- ### Extract Task
    This task extracts raw data from the source database (`flight_src_db`) and stores it as CSV files in MinIO. The output consists of individual CSV files for each table from the source database, which are stored in a structured directory within MinIO.

- ### Load Task
    The Load task retrieves the extracted data (CSV files) and loads it into the `stg` schema of the warehouse database (`flight_wrh_db`). The data in the `stg` schema is kept in its raw form, reflecting the data structure of the source database.

- ### Transform Task
    The Transform task processes and transforms the raw data into a format suitable for the data warehouse, following the warehouse's design.

    In this step, the raw data in the `stg` schema is processed and transformed to meet the structure and requirements of the data warehouse. The transformed data is then loaded into the final schema.

---

# Requirements

    - OS :
        - Linux
    
    - Tools :
        - Docker
        - MinIO
        - DBeaver (for PostgreSQL)
        - Apache Airflow
    
    - Programming Language
        - Python
        - SQL

    - Python Library:
        - pandas
        - pendulum
        - minio
        - cryptography

---


# Preparations

- ## Directory structure
   Organize the project files to maintain a clean and understandable structure. While there are no rigid guidelines, ensure that the directory is intuitive.

    ```
    flight-data-pipeline/
    ├── dags/
    │   ├── flights_data_pipeline/
    │   │   ├── query/
    │   │   │   ├── aircrafts_data.sql
    │   │   │   ├── airports_data.sql
    │   │   │   ├── boarding_passes.sql
    │   │   │   ├── bookings.sql
    │   │   │   ├── flights.sql
    │   │   │   ├── seats.sql
    │   │   │   ├── ticket_flights.sql
    │   │   │   └── tickets.sql
    │   │   ├── run.py                     # Main DAG file
    │   │   └── tasks/
    │   │       ├── __init__.py
    │   │       ├── extract.py             # Extract logic
    │   │       ├── load.py                # Load logic
    │   │       └── transform/
    │   │           ├── dim_aircraft.sql
    │   │           ├── dim_airport.sql
    │   │           ├── dim_passenger.sql
    │   │           ├── dim_seat.sql
    │   │           ├── fct_boarding_pass.sql
    │   │           ├── fct_booking_ticket.sql
    │   │           ├── fct_flight_activity.sql
    │   │           └── fct_seat_occupied_daily.sql
    │   └── helper/
    │       ├── __init__.py
    │       ├── minio.py                  # MinIO client helper
    │       └── postgres.py               # Postgres helper
    ├── flight_src_db/
    │   └── init.sql                      # Source DB initialization SQL
    ├── flight_wrh_db/
    │   ├── init.sql                      # Warehouse DB initialization SQL
    │   └── stg_schema.sql                # Staging schema setup SQL
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    ├── README.md
    ├── .env
    ├── start.sh
    └── fernet.py                         # Optional, to encrypt the privacy data on connection in Apache Airflow
    ```

---

- ## Setup project environment

    Create and activate a Python virtual environment to isolate project dependencies:

    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```

---

- ## Install requirements.txt

    Install the required dependencies from the `requirements.txt`:
  
    ```
    pip install -r requirements.txt
    ```

---

- ## Setup Database

    - [Source Database](flight_src_db/init.sql)
    - Warehouse Database
        - [Staging Schema](flight_wrh_db/stg_schema.sql)
        - [Final Schema](flight_wrh_db/init.sql)

- ## Create and Run a Docker Compose
    - The [_docker_compose.yml_](docker-compose.yml) file is used to set up the databases, MinIO, and Apache Airflow.
    - Database credentials are stored in the [`.env`](.env) file.

    - To run the services, execute:
        ```
        docker compose up --build --detach
        ```

- ## Create _.env_ file
  - The `.env` file contains credentials and configuration details for various services.
  
  ```
  touch .env
  ```

  - Add the following credentials to the `.env` file: 
    
        - Airflow Metadata
        AIRFLOW_DB_USER=
        AIRFLOW_DB_PASSWORD=
        AIRFLOW_DB_NAME=
        AIRFLOW_FERNET_KEY=''
        AIRFLOW_DB_URI=postgresql+psycopg2://<username>:<password>@<host>:<port>/<database>
    
        - Source
        FLIGHT_SRC_DB_USER=
        FLIGHT_SRC_DB_PASSWORD=
        FLIGHT_SRC_DB_NAME=

        - Data Warehouse
        FLIGHT_WRH_DB_USER=
        FLIGHT_WRH_DB_PASSWORD=
        FLIGHT_WRH_DB_NAME=

        - MinIO
        MINIO_ROOT_USER=
        MINIO_ROOT_PASSWORD=
        

- ## Activate the container
    - **Connect to the Database in DBeaver:**
        1. Open DBeaver and go to **Database** > **New Database Connection**.
        2. Select **PostgreSQL** as the database type.
        3. Enter the required details such as port, database name, username, and password (as defined in your `.env` file).
        4. Click **Test Connection** to verify the connection.
        5. If no errors occur, the connection setup is successful.

    - **Check MinIO and Apache Airflow Connections:**
        - You can check the status of MinIO and Apache Airflow connections on `localhost` based on the configuration in the Docker setup:
            - MinIO: `localhost:9001`
            - Apache Airflow: `localhost:8081`

- ## Make Connections on Apache Airflow
    - After ensuring that Apache Airflow, MinIO, and the databases are properly set up and running, the next step is to configure connections in Apache Airflow. Storing these
      connection credentials and parameters in Apache Airflow will allow easier management of access to external systems such as MinIO and PostgreSQL, which will be used across         different tasks and workflows.
    - To create connections in Apache Airflow, follow these steps:
        1. Go to **Admin** in the Airflow UI.
        2. Select **Connections**.
        3. Click **Add New Record**.
        4. Fill in the required details for each connection.
    - Once the connections are created, you can verify them by checking the `connection` table in the `airflow_metadata` database. Below is an illustration of the connections table:
      ![connection_table](records/connection_table.png)
      
---
---

# ELT Scripts
I developed each task separately to facilitate better management and clarity in the pipeline process. All task scripts are stored in the [tasks folder](dags/flights_data_pipeline/tasks). The pipeline is orchestrated using Apache Airflow, which requires scripting to run the Directed Acyclic Graph (DAG). To make the code more modular and easier to manage, I created separate modules and folders, particularly for the transformation process.

### [EXTRACT Task](dags/flights_data_pipeline/tasks/extract.py)

- The **Extract** task is responsible for extracting data from the source PostgreSQL database and exporting it as CSV files to MinIO.
- The source database is the **bookings** schema.
- The task uses Airflow's **PythonOperator** to handle the extraction process.
- Each table’s data is saved into a structured path in MinIO: `/extracted-data/temp/<table_name>.csv`.
- The extraction tasks are designed to run in parallel for efficiency.

### [LOAD Task](dags/flights_data_pipeline/tasks/load.py)

- The **Load** task reads the CSV files generated by the Extract task and loads them into the staging schema of the warehouse database.
- The task uses the MinIO client to read the CSV files stored in MinIO.
- The data is loaded into the **staging** schema (upsert process) within the warehouse database.
- The task follows a **PythonOperator** approach.
- The tables are loaded sequentially in the following order: `aircrafts_data → airports_data → bookings → tickets → seats → flights → ticket_flights → boarding_passes`.

### [TRANSFORM Task](dags/flights_data_pipeline/tasks/transform/)

- The **Transform** task is responsible for transforming raw data from the **staging** schema into dimension and fact tables in the data warehouse.
- For the transformation process, I did not create a `transform.py` module as it was unnecessary. Instead, I used **PostgresOperator** to execute the transformation SQL queries directly.
- Each SQL file (stored in the `transform` folder) performs the transformation and cleans the data according to the requirements of the data warehouse schema.
- The output tables are stored in the warehouse schema and follow specific naming conventions, such as `dim_airport`, `dim_seat`, `dim_passenger`, `fct_booking_ticket`, and `fct_flight_activity`.
- The transformations are executed in the correct sequence to ensure that the dependencies between the tasks are respected.

This modular approach not only ensures a more organized codebase but also simplifies the management of the ELT pipeline in Airflow.

---
---
# Run The Pipeline
To run the pipeline, create [the script](dags/flights_data_pipeline/run.py) that will wrap all the orchestration. Here is the DAG detail:
```
DAG ID	     : flights_data_pipeline
Schedule	 : Daily
Start date	 : Now
Catchup 	 : False
```

After that, access apache airflow on localhost:[apache_port] and run the dag _flights_data_pipeline_. Below are the visualizations for successful task executions:
![DAG](records/dag.png)
![extract](records/extract_graph.png)
![load](records/load_graph.png)
![transform](records/transform_graph.png)

---
---
# Conclusion

Thank you for exploring this project. I hope the details provided help you understand the workflow and execution of the ELT pipeline. Should you have any questions, feedback, or suggestions, feel free to reach out.

For more projects and insights, visit:

- [My Medium](https://medium.com/@fajariana.tm)

---

This version of your `README.md` is more concise, professional, and presents the information in a clearer, more structured format. Let me know if you'd like to make further adjustments!

    
  
