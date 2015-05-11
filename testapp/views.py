from django.shortcuts import render, redirect
from django.http import HttpResponse
from scipy.stats import uniform
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from skimage.data import imread
import cStringIO
from testapp.forms import UploadFileForm
from skimage import filters
from skimage.morphology import erosion, dilation, closing, disk, watershed
from skimage.measure import regionprops
from skimage.feature import peak_local_max
from skimage.segmentation import clear_border
from scipy import ndimage
from numpy import zeros_like, pi, mean, std


def show_image(im, **kwargs):
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111)
    ax.imshow(im, **kwargs)
    return fig, ax

# Create your views here.
def home(request):
	# return render(request,'testapp/home.html')
	return HttpResponse('hello world')

def testpage1(request):
	fig = Figure()
	plt.plot([1,2,3])
	buf = cStringIO.StringIO()
	plt.savefig(buf,format='png')
	data = buf.getvalue().encode("base64").strip()


	context = {'figure':data}
	return render(request,'testapp/testpage.html',context)

def testpage(request):
	img1 = 'F1-S0d3-H.JPG'
	buf = cStringIO.StringIO()
	# fig = Figure()
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.imshow(imread(img1))
	ax.axis('off')
	fig.savefig(buf,format='png')
	data = buf.getvalue().encode("base64").strip()
	context = {'figure':data}
	return render(request,'testapp/testpage.html',context)

def uploadfile(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			inbuf = cStringIO.StringIO()
			inbuf.write(request.FILES['image'].read())

			fig = plt.figure()
			ax = fig.add_subplot(111)
			outbuf = cStringIO.StringIO()
			ax.imshow(imread(inbuf))
			fig.savefig(outbuf,format='png')
			data = outbuf.getvalue().encode("base64").strip()
			context = {'figure':data}
			return render(request,'testapp/testpage.html',context)
	else:
		form = UploadFileForm()
	return render(request, 'testapp/uploadfile.html',{'form':form})

	



def diameter(num_px):
    R = 24.95816
    Apx = (50/R)**2 # area of single pixel, about 4 um^2 / sq px
    A = Apx*num_px
    return ((A/pi)**(0.5))*2

def clusterDetector(buf):
	# img1 = 'F1-S0d3-H.JPG'
	# img_filename = img1
	img = 255-imread(buf, as_grey=True)
	med_img = filters.median(img, disk(3))


	scharr_edges = filters.scharr(med_img)
	edges = scharr_edges > filters.threshold_otsu(scharr_edges)

	foreground = med_img > 50

	watershed_image = closing(closing(foreground, disk(2)) ^ (edges), disk(2))

	distance = ndimage.distance_transform_edt(watershed_image)
	filtered_distance = ndimage.gaussian_filter(distance, 3)

	local_maxi = peak_local_max(filtered_distance, indices=False,
	                             min_distance=20, exclude_border=False)
	markers = dilation(ndimage.label(local_maxi)[0], disk(10))
	labels = watershed(-distance, markers, mask=erosion(watershed_image, disk(2)))

	j = 1
	cleared_labels = zeros_like(labels)
	for i in range(1, labels.max()+1):
		cleared = clear_border(labels==i).astype(int)
		if cleared.max()>0:
			cleared_labels += cleared * j
			j += 1

	props = regionprops(cleared_labels)


	# offset = 0
	# cnum = 0
	# prop = props[cnum]
	# box = prop.bbox
	# imbox = img[box[0]-offset:box[2]+offset, box[1]-offset:box[3]+offset]
	# plt.imshow(imbox, interpolation='nearest', cmap='Greys')
	# plt.imshow(prop.image,cmap="Reds",alpha=0.3)
	# plt.axis('off')

	offset = 0

	# fig = plt.figure(figsize=(15,15))
	output = []
	for i, prop in enumerate(props):

		box = prop.bbox
	
		# a = fig.add_subplot(12, 12, i+1)
		fig = Figure()
		canvas = FigureCanvasAgg(fig)
		ax = fig.add_subplot(111)
		ax.imshow(img[box[0]-offset:box[2]+offset, box[1]-offset:box[3]+offset], interpolation='nearest', cmap='Greys')
		ax.imshow(prop.image, cmap="Reds", alpha=0.3)
		ax.axis('off')
		buf = cStringIO.StringIO()
		fig.savefig(buf,format='png')
		# plt.clf()
		data = buf.getvalue().encode("base64").strip()

		diam = diameter(prop.image.sum())

		output.append({'data':data,'diameter':diam})

	return output
	# context = {'clusters':output}
	# return render(request,'testapp/testpage.html',context)


def clustersizer(request):

	form = UploadFileForm()
	return render(request, 'testapp/clustersizer.html',{'form':form})


def reviewclusters(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			buf = cStringIO.StringIO()
			buf.write(request.FILES['image'].read())
			# return HttpResponse('thanks')
			clusters = clusterDetector(buf)
			# for cluster in clusters:
			# 	data = cluster.getvalue().encode("base64").strip()
			context = {'clusters':clusters}
			return render(request,'testapp/reviewclusters.html',context)
	else:
		redirect('/testapp/clustersizer')

def clusterresults(request):
	if request.method == 'POST':
		mmts = request.POST['mmts'].split(',')
		mmts = [float(m) for m in mmts]
		mmts_str = ['{0:.2f}'.format(m) for m in mmts]
		context = {'mmts':mmts_str,
					'mean':'{0:.2f}'.format(mean(mmts)),
					'se':'{0:.2f}'.format(std(mmts)**(.5))}
		return render(request,'testapp/clusterresults.html',context)
	else:
		redirect('/testapp/clustersizer')
