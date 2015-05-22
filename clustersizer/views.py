from django.shortcuts import render, redirect
from django.http import HttpResponse
from numpy import mean, std, sqrt
import cStringIO
from clustersizer.forms import UploadFileForm

from utils import clusterDetector

import django_rq


def upload(request):
	if request.method == 'POST':
		# form = UploadFileForm(request.POST, request.FILES)
		buf = cStringIO.StringIO()
		buf.write(request.FILES['image'].read())
		imgstr = buf.getvalue()#.encode("base64").strip()
		# send to queue
		job = django_rq.enqueue(clusterDetector,imgstr,
			filetype=request.POST['filetype'],
			clustercolor=request.POST['clustercolor'])
		return HttpResponse(job.id)
		
	else:
		# form = UploadFileForm(request.POST, request.FILES)
		return render(request, 'clustersizer/upload.html')


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
	print "retrieved queue"
	result = q.fetch_job(jobid).result
	print "retrived result"
	context = {'clusters':result}
	print "starting render"
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
