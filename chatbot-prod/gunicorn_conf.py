from multiprocessing import cpu_count

# Socket Path

bind = 'unix:/home/gpt41/ml-development/chatbot-prod/api.sock'

# Worker Options

workers = cpu_count() + 1

worker_class = 'uvicorn.workers.UvicornWorker'

loglevel = 'debug'

accesslog = '/home/gpt41/ml-development/chatbot-prod/access_log'

errorlog =  '/home/gpt41/ml-development/chatbot-prod/error_log'
