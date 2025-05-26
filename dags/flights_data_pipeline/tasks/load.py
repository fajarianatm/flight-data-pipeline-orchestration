from helper.minio import MinioClient
from helper.postgres import Execute
import pandas as pd
import json

BASE_PATH = "/opt/airflow/dags"

class Load:
    def _tickets():
        minio_client = MinioClient._get()
        bucket_name = 'extracted-data'
        object_name = f"extracted-data/temp/tickets.csv"

        data = minio_client.get_object(
            bucket_name = bucket_name,
            object_name = object_name
        )

        df_tickets = pd.read_csv(data)

        df_tickets['contact_data'] = df_tickets['contact_data'].apply(json.dumps)

        Execute._upsert_dataframe(
            connection_id = 'flight_wrh_db', 
            dataframe = df_tickets, 
            target_table = 'stg.tickets', 
            conflict_columns = ['ticket_no']
            )
    
    def _aircrafts_data():
        minio_client = MinioClient._get()
        bucket_name = 'extracted-data'
        object_name = f"extracted-data/temp/aircrafts_data.csv"

        data = minio_client.get_object(
            bucket_name = bucket_name,
            object_name = object_name
        )

        df_aircrafts_data = pd.read_csv(data)

        df_aircrafts_data['model'] = df_aircrafts_data['model'].apply(json.dumps)

        Execute._upsert_dataframe(
            connection_id = 'flight_wrh_db', 
            dataframe = df_aircrafts_data, 
            target_table = 'stg.aircrafts_data', 
            conflict_columns = ['aircraft_code']
            )
    
    def _airports_data():
        minio_client = MinioClient._get()
        bucket_name = 'extracted-data'
        object_name = f"extracted-data/temp/airports_data.csv"

        data = minio_client.get_object(
            bucket_name = bucket_name,
            object_name = object_name
        )

        df_airports_data = pd.read_csv(data)

        df_airports_data['airport_name'] = df_airports_data['airport_name'].apply(json.dumps)
        df_airports_data['city'] = df_airports_data['city'].apply(json.dumps)

        Execute._upsert_dataframe(
            connection_id = 'flight_wrh_db', 
            dataframe = df_airports_data, 
            target_table = 'stg.airports_data', 
            conflict_columns = ['airport_code']
            )
        
    def _boarding_passes():
        minio_client = MinioClient._get()
        bucket_name = 'extracted-data'
        object_name = f"extracted-data/temp/boarding_passes.csv"

        data = minio_client.get_object(
            bucket_name = bucket_name,
            object_name = object_name
        )

        df_boarding_passes = pd.read_csv(data)

        Execute._upsert_dataframe(
            connection_id = 'flight_wrh_db', 
            dataframe = df_boarding_passes, 
            target_table = 'stg.boarding_passes', 
            conflict_columns = ['ticket_no', 'flight_id']
            )

    def _bookings():
        minio_client = MinioClient._get()
        bucket_name = 'extracted-data'
        object_name = f"extracted-data/temp/bookings.csv"

        data = minio_client.get_object(
            bucket_name = bucket_name,
            object_name = object_name
        )

        df_bookings = pd.read_csv(data)

        Execute._upsert_dataframe(
            connection_id = 'flight_wrh_db', 
            dataframe = df_bookings, 
            target_table = 'stg.bookings', 
            conflict_columns = ['book_ref']
            )    
    
    def _flights():
        minio_client = MinioClient._get()
        bucket_name = 'extracted-data'
        object_name = f"extracted-data/temp/flights.csv"

        data = minio_client.get_object(
            bucket_name = bucket_name,
            object_name = object_name
        )

        df_flights = pd.read_csv(data)

        datetime_columns = ['scheduled_departure', 'scheduled_arrival', 'actual_departure', 'actual_arrival']
        for col in datetime_columns:
            df_flights[col] = pd.to_datetime(df_flights[col], errors='coerce')
            df_flights[col] = df_flights[col].replace({pd.NaT: None})       

        Execute._upsert_dataframe(
            connection_id = 'flight_wrh_db', 
            dataframe = df_flights, 
            target_table = 'stg.flights', 
            conflict_columns = ['flight_id']
            )
    
    def _seats():
        minio_client = MinioClient._get()
        bucket_name = 'extracted-data'
        object_name = f"extracted-data/temp/seats.csv"

        data = minio_client.get_object(
            bucket_name = bucket_name,
            object_name = object_name
        )

        df_seats = pd.read_csv(data)

        Execute._upsert_dataframe(
            connection_id = 'flight_wrh_db', 
            dataframe = df_seats, 
            target_table = 'stg.seats', 
            conflict_columns = ['aircraft_code', 'seat_no']
            )
        
    def _ticket_flights():
        minio_client = MinioClient._get()
        bucket_name = 'extracted-data'
        object_name = f"extracted-data/temp/ticket_flights.csv"

        data = minio_client.get_object(
            bucket_name = bucket_name,
            object_name = object_name
        )

        df_ticket_flights = pd.read_csv(data)

        Execute._upsert_dataframe(
            connection_id = 'flight_wrh_db', 
            dataframe = df_ticket_flights, 
            target_table = 'stg.ticket_flights', 
            conflict_columns = ['ticket_no', 'flight_id']
            )