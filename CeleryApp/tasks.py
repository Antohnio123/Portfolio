# import time
# from celery import Celery
#
#
# app = Celery('tasks', broker='amqp://guest@localhost//')
# app.conf.CELERY_RESULT_BACKEND='amqp://'
#
#
# @app.task
# def add (x,y):
#     print ('add({0}, {1})'.format(x,y))
#     time.sleep(0.1)
#     return x+y
#
#
# @app.task
# def mul (x,y):
#     print('mul ({0}, {1})'.format(x,y))
#     return x*y
#
# if __name__=='__main__':
#     app.worker_main()