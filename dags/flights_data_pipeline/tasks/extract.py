from helper.minio import MinioClient
from helper.postgres import Execute
from io import BytesIO

BASE_PATH = "/opt/airflow/dags"

class Extract:
    def _tickets():
        df = Execute._get_dataframe(
            connection_id = 'flight_src_db',
            query_path = 'flights_data_pipeline/query/tickets.sql'
        )

        bucket_name = 'extracted-data'
        minio_client = MinioClient._get()

        csv_bytes = df.to_csv(index = False).encode('utf-8')
        csv_buffer = BytesIO(csv_bytes)

        minio_client.put_object(
            bucket_name = bucket_name,
            object_name = f'/extracted-data/temp/tickets.csv',
            data = csv_buffer,
            length = len(csv_bytes),
            content_type = 'application/csv'
        )

    def _aircrafts_data():
        df = Execute._get_dataframe(
            connection_id = 'flight_src_db',
            query_path = 'flights_data_pipeline/query/aircrafts_data.sql'
        )

        bucket_name = 'extracted-data'
        minio_client = MinioClient._get()

        csv_bytes = df.to_csv(index = False).encode('utf-8')
        csv_buffer = BytesIO(csv_bytes)

        minio_client.put_object(
            bucket_name = bucket_name,
            object_name = f'/extracted-data/temp/aircrafts_data.csv',
            data = csv_buffer,
            length = len(csv_bytes),
            content_type = 'application/csv'
        )

    def _airports_data():
        df = Execute._get_dataframe(
            connection_id = 'flight_src_db',
            query_path = 'flights_data_pipeline/query/airports_data.sql'
        )

        bucket_name = 'extracted-data'
        minio_client = MinioClient._get()

        csv_bytes = df.to_csv(index = False).encode('utf-8')
        csv_buffer = BytesIO(csv_bytes)

        minio_client.put_object(
            bucket_name = bucket_name,
            object_name = f'/extracted-data/temp/airports_data.csv',
            data = csv_buffer,
            length = len(csv_bytes),
            content_type = 'application/csv'
        )

    def _boarding_passes():
        df = Execute._get_dataframe(
            connection_id = 'flight_src_db',
            query_path = 'flights_data_pipeline/query/boarding_passes.sql'
        )

        bucket_name = 'extracted-data'
        minio_client = MinioClient._get()

        csv_bytes = df.to_csv(index = False).encode('utf-8')
        csv_buffer = BytesIO(csv_bytes)

        minio_client.put_object(
            bucket_name = bucket_name,
            object_name = f'/extracted-data/temp/boarding_passes.csv',
            data = csv_buffer,
            length = len(csv_bytes),
            content_type = 'application/csv'
        )

    def _bookings():
        df = Execute._get_dataframe(
            connection_id = 'flight_src_db',
            query_path = 'flights_data_pipeline/query/bookings.sql'
        )

        bucket_name = 'extracted-data'
        minio_client = MinioClient._get()

        csv_bytes = df.to_csv(index = False).encode('utf-8')
        csv_buffer = BytesIO(csv_bytes)

        minio_client.put_object(
            bucket_name = bucket_name,
            object_name = f'/extracted-data/temp/bookings.csv',
            data = csv_buffer,
            length = len(csv_bytes),
            content_type = 'application/csv'
        )

    def _flights():
        df = Execute._get_dataframe(
            connection_id = 'flight_src_db',
            query_path = 'flights_data_pipeline/query/flights.sql'
        )

        bucket_name = 'extracted-data'
        minio_client = MinioClient._get()

        csv_bytes = df.to_csv(index = False).encode('utf-8')
        csv_buffer = BytesIO(csv_bytes)

        minio_client.put_object(
            bucket_name = bucket_name,
            object_name = f'/extracted-data/temp/flights.csv',
            data = csv_buffer,
            length = len(csv_bytes),
            content_type = 'application/csv'
        )

    def _seats():
        df = Execute._get_dataframe(
            connection_id = 'flight_src_db',
            query_path = 'flights_data_pipeline/query/seats.sql'
        )

        bucket_name = 'extracted-data'
        minio_client = MinioClient._get()

        csv_bytes = df.to_csv(index = False).encode('utf-8')
        csv_buffer = BytesIO(csv_bytes)

        minio_client.put_object(
            bucket_name = bucket_name,
            object_name = f'/extracted-data/temp/seats.csv',
            data = csv_buffer,
            length = len(csv_bytes),
            content_type = 'application/csv'
        )

    def _ticket_flights():
        df = Execute._get_dataframe(
            connection_id = 'flight_src_db',
            query_path = 'flights_data_pipeline/query/ticket_flights.sql'
        )

        bucket_name = 'extracted-data'
        minio_client = MinioClient._get()

        csv_bytes = df.to_csv(index = False).encode('utf-8')
        csv_buffer = BytesIO(csv_bytes)

        minio_client.put_object(
            bucket_name = bucket_name,
            object_name = f'/extracted-data/temp/ticket_flights.csv',
            data = csv_buffer,
            length = len(csv_bytes),
            content_type = 'application/csv'
        )