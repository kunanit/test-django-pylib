from django.shortcuts import render
from django.http import HttpResponse
from scipy.stats import uniform
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from skimage.data import imread
import cStringIO

def show_image(im, **kwargs):
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111)
    ax.imshow(im, **kwargs)
    return fig, ax

# Create your views here.
def home(request):
	# return render(request,'testapp/home.html')
	return HttpResponse('hello world')

def testpage(request):
	# matplotlib.use('Agg')
	img1 = 'F1-S0d3-H.JPG'
	img2 = 'F2-S0d3-H.JPG'

	img_filename = img1
	img = 255-imread(img_filename)
	fig = show_image(img, cmap='jet')
	canvas = FigureCanvasAgg(fig)

	buf = cStringIO.StringIO()
	canvas.print_png(buf)
	data = buf.getvalue()

	response = HttpResponse(data,content_type='image/png',content_length=len(data))
	# response['Content-Disposition'] = 'attachment; filename=flowassaydata.csv'
	return HttpResponse(response)