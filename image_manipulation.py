import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as nd
from scipy.ndimage.filters import median_filter as mf

if __name__ == '__main__':
	dpath = 'images'
	fname = 'ml.jpg'
	infile = os.path.join(dpath,fname)

	#fancy image read line
	img_ml = np.uint8( mf( np.float64(255-nd.imread(infile)[::2,::2,::-1]), (8,2,1)) )

	#display the image
	ysize = 9.
	xsize = ysize*float(img_ml.shape[1])/float(img_ml.shape[0])

	plt.ion()
	fig, ax = plt.subplots(figsize=(xsize,ysize))
	fig.subplots_adjust(0,0,1,1)
	fig.canvas.set_window_title('modified Mona Lisa')
	ax.axis('off')
	im = ax.imshow(img_ml)
	fig.canvas.draw()
	plt.show(block=True)