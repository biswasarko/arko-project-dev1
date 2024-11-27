from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


# Function to demonstrate integer parameter
def process_integer(number):
    print(f"Processing integer: {number}")


# Function to demonstrate string parameter
def process_string(string):
    print(f"Processing string: {string}")


# Function to demonstrate list parameter
def process_list(items):
    for item in items:
        print(f"Processing item: {item}")


# DAG definition
with DAG(
        'demo_taskgroup_dag',
        default_args=default_args,
        description='Demo DAG with TaskGroup and various parameters',
        schedule_interval='*/3 * * * *',  # Every 3 minutes
        start_date=datetime(2024, 11, 27),
        catchup=False,
) as dag:
    # TaskGroup to group related tasks
    with TaskGroup("parameter_processing", tooltip="Processing different parameters") as parameter_processing:
        # Task 1: Process an integer
        process_int_task = PythonOperator(
            task_id='process_integer',
            python_callable=process_integer,
            op_args=[42],  # Example integer
        )

        # Task 2: Process a string
        process_str_task = PythonOperator(
            task_id='process_string',
            python_callable=process_string,
            op_args=["Hello, Airflow!"],  # Example string
        )

        # Task 3: Process a list
        process_list_task = PythonOperator(
            task_id='process_list',
            python_callable=process_list,
            op_args=[[1, 2, 3, 4, 5]],  # Example list
        )

    # Task outside TaskGroup
    start_task = PythonOperator(
        task_id='start_task',
        python_callable=lambda: print("DAG started!"),
    )

    # Define task dependencies
    start_task >> parameter_processing
