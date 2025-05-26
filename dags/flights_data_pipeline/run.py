from airflow.decorators import dag, task_group
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import pendulum
from datetime import timedelta
from flights_data_pipeline.tasks.extract import Extract
from flights_data_pipeline.tasks.load import Load
from helper.minio import MinioClient
from helper.postgres import Execute

BASE_PATH = "/opt/airflow/dags/flights_data_pipeline"

@dag(
    dag_id = 'flights_data_pipeline',
    start_date = pendulum.now(),
    schedule = '@daily',
    catchup = False
)

def flight_data_pipeline():
    @task_group
    def extract():
        tickets = PythonOperator(
            task_id = 'tickets',
            python_callable = Extract._tickets,
            execution_timeout=timedelta(minutes=5)
        )

        aircrafts_data = PythonOperator(
            task_id = 'aircrafts_data',
            python_callable = Extract._aircrafts_data,
            execution_timeout=timedelta(minutes=5)
        )

        airports_data = PythonOperator(
            task_id = 'airports_data',
            python_callable = Extract._airports_data,
            execution_timeout=timedelta(minutes=5)
        )

        boarding_passes = PythonOperator(
            task_id = 'boarding_passes',
            python_callable = Extract._boarding_passes,
            execution_timeout=timedelta(minutes=5)
        )

        bookings = PythonOperator(
            task_id = 'bookings',
            python_callable = Extract._bookings,
            execution_timeout=timedelta(minutes=5)
        )

        flights = PythonOperator(
            task_id = 'flights',
            python_callable = Extract._flights,
            execution_timeout=timedelta(minutes=5)
        )

        seats = PythonOperator(
            task_id = 'seats',
            python_callable = Extract._seats,
            execution_timeout=timedelta(minutes=5)
        )

        ticket_flights = PythonOperator(
            task_id = 'ticket_flights',
            python_callable = Extract._ticket_flights,
            execution_timeout=timedelta(minutes=10)
        )
        
        return [tickets, aircrafts_data, airports_data, boarding_passes, bookings, flights, seats, ticket_flights]

    @task_group
    def load():
        aircrafts_data = PythonOperator(
            task_id = 'aircrafts_data',
            python_callable = Load._aircrafts_data
        )
    
        airports_data = PythonOperator(
            task_id = 'airports_data',
            python_callable = Load._airports_data
        )

        bookings = PythonOperator(
            task_id = 'bookings',
            python_callable = Load._bookings
        )

        tickets = PythonOperator(
            task_id = 'tickets',
            python_callable = Load._tickets
        )
    
        seats = PythonOperator(
            task_id = 'seats',
            python_callable = Load._seats
        )
    
        flights = PythonOperator(
            task_id = 'flights',
            python_callable = Load._flights
        )
    
        ticket_flights = PythonOperator(
            task_id = 'ticket_flights',
            python_callable = Load._ticket_flights
        )

        boarding_passes = PythonOperator(
            task_id = 'boarding_passes',
            python_callable = Load._boarding_passes
        )
        
        aircrafts_data >> airports_data >> bookings >> tickets >> seats >> flights >> ticket_flights >> boarding_passes

    @task_group
    def transform():
        dim_aircraft = PostgresOperator(
            task_id = 'dim_aircraft',
            postgres_conn_id = 'flight_wrh_db',
            sql = 'tasks/transform/dim_aircraft.sql'
        )

        dim_airport = PostgresOperator(
            task_id = 'dim_airport',
            postgres_conn_id = 'flight_wrh_db',
            sql = 'tasks/transform/dim_airport.sql'
        )

        dim_passenger = PostgresOperator(
            task_id = 'dim_passenger',
            postgres_conn_id = 'flight_wrh_db',
            sql = 'tasks/transform/dim_passenger.sql'
        )

        dim_seat = PostgresOperator(
            task_id = 'dim_seat',
            postgres_conn_id = 'flight_wrh_db',
            sql = 'tasks/transform/dim_seat.sql'
        )

        fct_boarding_pass = PostgresOperator(
            task_id = 'fct_boarding_pass',
            postgres_conn_id = 'flight_wrh_db',
            sql = 'tasks/transform/fct_boarding_pass.sql'
        )

        fct_booking_ticket = PostgresOperator(
            task_id = 'fct_booking_ticket',
            postgres_conn_id = 'flight_wrh_db',
            sql = 'tasks/transform/fct_booking_ticket.sql'
        )

        fct_flight_activity = PostgresOperator(
            task_id = 'fct_flight_activity',
            postgres_conn_id = 'flight_wrh_db',
            sql = 'tasks/transform/fct_flight_activity.sql'
        )

        fct_seat_occupied_daily = PostgresOperator(
            task_id = 'fct_seat_occupied_daily',
            postgres_conn_id = 'flight_wrh_db',
            sql = 'tasks/transform/fct_seat_occupied_daily.sql'
        )

        dim_aircraft >> dim_airport >> dim_passenger >> dim_seat >> fct_boarding_pass >> fct_booking_ticket >> fct_flight_activity >> fct_seat_occupied_daily

    extract() >> load() >> transform()

flight_data_pipeline()
        
