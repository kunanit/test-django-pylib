

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from skimage.data import imread
import cStringIO

from skimage import filters
from skimage.morphology import erosion, dilation, closing, disk, watershed
from skimage.measure import regionprops
from skimage.feature import peak_local_max
from skimage.segmentation import clear_border
from scipy import ndimage
from numpy import zeros_like, pi, mean, std, sqrt




def clusterDetector(imgstr, filetype, clustercolor):

	def diameter(num_px):
		if filetype=='tiff':
			R = 0.16415411
		elif filetype=='jpeg':
			R = 24.95816
		Apx = (50/R)**2 # area of single pixel, about 4 um^2 / sq px
		A = Apx*num_px
		return ((A/pi)**(0.5))*2

	buf = cStringIO.StringIO(imgstr) 
	
	if clustercolor=='dark':
		img = 255-imread(buf, as_grey=True)
	elif clustercolor=='light':
		img = imread(buf, as_grey=True)

	print "Image read by worker, starting image processing"
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

	offset = 0

	output = []
	for i, prop in enumerate(props):

		box = prop.bbox
	
		fig = Figure()
		canvas = FigureCanvasAgg(fig)
		ax = fig.add_subplot(111)
		ax.imshow(img[box[0]-offset:box[2]+offset, box[1]-offset:box[3]+offset], interpolation='nearest', cmap='Greys')
		ax.imshow(prop.image, cmap="Reds", alpha=0.3)
		ax.axis('off')
		buf = cStringIO.StringIO()
		fig.savefig(buf,format='png')

		data = buf.getvalue().encode("base64").strip()

		diam = diameter(prop.image.sum())

		output.append({'data':data,'diameter':diam})
	print "job finished"
	return output