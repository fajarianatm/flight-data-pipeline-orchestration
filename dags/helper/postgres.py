from airflow.providers.postgres.hooks.postgres import PostgresHook
import psycopg2.extras
import pandas as pd
BASE_PATH = "/opt/airflow/dags"


class Execute:
    def _query(connection_id, query_path):
        hook = PostgresHook(postgres_conn_id = connection_id)
        connection = hook.get_conn()
        cursor = connection.cursor()
        
        with open(f'{BASE_PATH}/{query_path}', 'r') as file:
            query = file.read()

        cursor.execute(query)
        cursor.close()
        connection.commit()
        connection.close()

    def _get_dataframe(connection_id, query_path):
        pg_hook = PostgresHook(postgres_conn_id = connection_id)
        connection = pg_hook.get_conn()
        cursor = connection.cursor()
        
        with open(f'{BASE_PATH}/{query_path}', 'r') as file:
            query = file.read()

        cursor.execute(query)
        result = cursor.fetchall()
        column_list = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns = column_list)

        cursor.close()
        connection.commit()
        connection.close()
        
        return df


    def _insert_dataframe(connection_id, query_path, dataframe):
        BASE_PATH = "/opt/airflow/dags"
        
        pg_hook = PostgresHook(postgres_conn_id = connection_id)
        connection = pg_hook.get_conn()
        cursor = connection.cursor()
        
        with open(f'{BASE_PATH}/{query_path}', 'r') as file:
            query = file.read()

        for index, row in dataframe.iterrows():
            record = row.to_dict()
            pg_hook.run(query, parameters = record)

        cursor.close()
        connection.commit()
        connection.close()

    def _upsert_dataframe(connection_id, dataframe, target_table, conflict_columns):
        hook = PostgresHook(postgres_conn_id=connection_id)
        conn = hook.get_conn()
        cursor = conn.cursor()

        # Convert DataFrame to list of dicts
        records = dataframe.to_dict(orient='records')

        if not records:
            print(f"No data to upsert into {target_table}")
            return

        columns = list(records[0].keys())
        columns_str = ', '.join(columns)
        placeholders = ', '.join([f"%({col})s" for col in columns])
        
        update_assignments = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col not in conflict_columns])

        query = f"""
            INSERT INTO {target_table} ({columns_str})
            VALUES ({placeholders})
            ON CONFLICT ({', '.join(conflict_columns)})
            DO UPDATE SET {update_assignments};
        """

        try:
            psycopg2.extras.execute_batch(cursor, query, records)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error in upsert: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
