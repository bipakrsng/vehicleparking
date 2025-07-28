broker_url = 'redis://localhost:6379/1' #task need to be done is stored
result_backend = 'redis://localhost:6379/2' # result of the task will be stored
timezone="Asia/kolkata"
broker_connection_retry_on_startup = True