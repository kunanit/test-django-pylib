from django.shortcuts import render, redirect
from django.http import HttpResponse

import cStringIO
from clustersizer.forms import UploadFileForm

from utils import clusterDetector

import django_rq

# def diameter(num_px):
# 	R = 24.95816
# 	Apx = (50/R)**2 # area of single pixel, about 4 um^2 / sq px
# 	A = Apx*num_px
# 	return ((A/pi)**(0.5))*2


# def clusterDetector(buf):

# 	img = 255-imread(buf, as_grey=True)
# 	med_img = filters.median(img, disk(3))


# 	scharr_edges = filters.scharr(med_img)
# 	edges = scharr_edges > filters.threshold_otsu(scharr_edges)

# 	foreground = med_img > 50

# 	watershed_image = closing(closing(foreground, disk(2)) ^ (edges), disk(2))

# 	distance = ndimage.distance_transform_edt(watershed_image)
# 	filtered_distance = ndimage.gaussian_filter(distance, 3)

# 	local_maxi = peak_local_max(filtered_distance, indices=False,
# 	                             min_distance=20, exclude_border=False)
# 	markers = dilation(ndimage.label(local_maxi)[0], disk(10))
# 	labels = watershed(-distance, markers, mask=erosion(watershed_image, disk(2)))

# 	j = 1
# 	cleared_labels = zeros_like(labels)
# 	for i in range(1, labels.max()+1):
# 		cleared = clear_border(labels==i).astype(int)
# 		if cleared.max()>0:
# 			cleared_labels += cleared * j
# 			j += 1

# 	props = regionprops(cleared_labels)

# 	offset = 0

# 	output = []
# 	for i, prop in enumerate(props):

# 		box = prop.bbox
	
# 		fig = Figure()
# 		canvas = FigureCanvasAgg(fig)
# 		ax = fig.add_subplot(111)
# 		ax.imshow(img[box[0]-offset:box[2]+offset, box[1]-offset:box[3]+offset], interpolation='nearest', cmap='Greys')
# 		ax.imshow(prop.image, cmap="Reds", alpha=0.3)
# 		ax.axis('off')
# 		buf = cStringIO.StringIO()
# 		fig.savefig(buf,format='png')

# 		data = buf.getvalue().encode("base64").strip()

# 		diam = diameter(prop.image.sum())

# 		output.append({'data':data,'diameter':diam})

# 	return output


def upload(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			buf = cStringIO.StringIO()
			buf.write(request.FILES['image'].read())
			return HttpResponse('thanks')


			# send to queue
			django_rq.enqueue(clusterDetector,buf)
			worker = django_rq.get_worker()
	else:
		form = UploadFileForm()
		return render(request, 'clustersizer/upload.html',{'form':form})

def checkjob(request):
	worker = django_rq.get_worker()
	result = worker.work()
	if not result:
		return HttpResponse('processing')
	else:
		return HttpResponse('done')

def review(request):
	worker = django_rq.get_worker()
	clusters = worker.work()
	if clusters:
		context = {'clusters':clusters}
		return render(request,'clustersizer/review.html',context)

	else: 
		return HttpResponse('data not found')
		# redirect('/clustersizer/upload')

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
