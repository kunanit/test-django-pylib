from django.shortcuts import render, redirect
from django.http import HttpResponse

import cStringIO
from clustersizer.forms import UploadFileForm

from utils import clusterDetector

import django_rq


def upload(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		buf = cStringIO.StringIO()
		buf.write(request.FILES['image'].read())
		# send to queue
		job = django_rq.enqueue(clusterDetector,buf)
		return HttpResponse(job.id)
		
	else:
		return render(request, 'clustersizer/upload.html',{'form':form})


def checkstatus(request):
	jobid = request.GET['jobid']
	q = django_rq.get_queue()
	print 'checking for results...'
	if q.fetch_job(jobid).result:

		return HttpResponse('done')
	else:
		return HttpResponse('processing')

def review(request):
	jobid = request.GET['jobid']
	q = django_rq.get_queue()
	result = q.fetch_job(jobid).result
	context = {'clusters':result}
	return render(request,'clustersizer/review.html',context)


def results(request):
	if request.method == 'POST':
		mmts = request.POST['mmts'].split(',')
		mmts = [float(m) for m in mmts]
		mmts_str = ['{0:.2f}'.format(m) for m in mmts]
		context = {'mmts':mmts_str,
					'mean':'{0:.2f}'.format(mean(mmts)),
					'se':'{0:.2f}'.format(std(mmts)/sqrt(len(mmts)))}
		return render(request,'clustersizer/results.html',context)
	else:
		redirect('/clustersizer/upload')
