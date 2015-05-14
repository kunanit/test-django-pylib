import django_rq


def myfun(input):
	return input


django_rq.enqueue(myfun, 'pizza')