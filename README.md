# Automated Data Pipeline Project

This project is designed to build an automated data pipeline that extracts data from a source database stores it temporarily in an object store, and loads it into a data warehouse. The pipeline will be orchestrated using Apache Airflow.

---
---

# Objective 

In this repository, I'll focus specifically on how I developed the ELT pipeline, including:

- Developing the ELT script

- Orchestrating and automating the pipeline with Apache Airflow

---

# Pipeline Workflow

Before diving into the main, take a look at the image below. This illustrates the workflow I followed to build this project.

![ELT_DESIGN](records/elt_design.png)

- ## How The Pipeline Works

Pipeline ini menggunakan Apache Airflow untuk orkestrasi dan automisasi. Pipeline ini akan menggunakan skrip untuk membuat DAG yang berisi 3 task

- ### Extract Task
    The Extract task pulls raw data from the source database (flight_src_db) and saves it as CSV files. The output of this task is a set of CSV files containing raw data for each table from the source database and is stored in MinIO

- ### Load Task
    The Load task takes the extracted data (CSV files) and loads it into 'stg' schema in the warehouse database (flight_wrh_db). Stg schema will stores the raw data exactly as it came from the source database.

- ### Transform Task
    The Transform Task performs data transformations based on the design of the data warehouse.

    In this step, the raw data from the 'stg' schema is processed and transformed to match the structure and requirements of the data warehouse. Once transformed, the data is loaded into the final schema.

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
    Set up the project directory structure to organize all project scripts. There is no strict rule where to put the folder and file. Still, make the directory understandable

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

    Create and activate python environment to isolate project dependencies.

    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```

---

- ## Install requirements.txt

    Install the dependencies from _requirements.txt_ in the created environment.
  
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

    - Create [_docker_compose.yml_](docker-compose.yml) file to set up databases, minio, and apache airflow.
    Then store database credentials in [_.env_](.env) file  

    - Run the _docker-compose.yml_ file 
    
        ```
        docker compose up --build --detach
        ```

- ## Activate the container

    - Connect the database to DBeaver
        - Click **Database** > select **New Database Connection**

        - Select postgreSQL

        - Fill in the port, database, username, and password **as defined in your _.env_**

        - Click **Test Connection**

        - If no errors appear, the database connection is successful  
    
    - Check MinIO and Apache Airflow connection on localhost based on docker configuration. On this project is localhost:8081 and localhost:9001

---
---

# ELT Scripts

    - ## Extract
    
  