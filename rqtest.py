# import django_rq

from redis import Redis
from rq import Queue

from time import sleep

# # django_rq.enqueue(myfun, 'pizza')



# print testfun('Andrew')

q = Queue(connection=Redis())
job= q.enqueue(testfun,'Andrew')
print job.result
sleep(5)
print job.result