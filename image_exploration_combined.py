
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as nd
from scipy.ndimage.filters import median_filter as mf


RED, GREEN, BLUE = (0,1,2)
CLICK_BUF1 = []
AX_DIC = {}
histIsRunning = False
darkenIsRunning = False



def plotHist(sample, fig, ax):
    #clear the axes and replot the histogram
    rangeList = [None,None,None]
    for i,axis in enumerate(ax):
        if axis in AX_DIC:
            rng = AX_DIC[axis]
            del AX_DIC[axis]
            rangeList[i] = ( rng.get_xy()[0][0], rng.get_xy()[2][0] )
        axis.cla()

    ax[0].hist(sample[:,:,RED].flatten(),bins=256,range=[0,255],color='r', edgecolor='none', normed=True)
    ax[1].hist(sample[:,:,GREEN].flatten(),bins=256,range=[0,255],color='g', edgecolor='none', normed=True)
    ax[2].hist(sample[:,:,BLUE].flatten(),bins=256,range=[0,255],color='b', edgecolor='none', normed=True)
    [axis.set_yticklabels('') for axis in ax]
    ax[0].set_ylabel('Red')
    ax[1].set_ylabel('Green')
    ax[2].set_ylabel('Blue')

    #reset the bounds in the image
    for i,r in enumerate(rangeList):
        if r != None:
            rng = ax[i].axvspan(r[0],r[1],facecolor='lime',alpha=0.5)
            AX_DIC[ax[i]] = rng

    fig.canvas.draw()


def handleClick1(xx,yy):
    global CLICK_BUF1
    global fig2
    global ax2
    global histIsRunning

    if histIsRunning == False:


        #if buffer is full, clear it
        if(len(CLICK_BUF1) >= 2):
            CLICK_BUF1 = []

        #if not full, take ac
        if(len(CLICK_BUF1) == 0):
            x1,y1 = np.int16((xx,yy))
            CLICK_BUF1.append((x1,y1))
        elif(len(CLICK_BUF1) == 1):
            x1,y1 = CLICK_BUF1[0]
            x2,y2 = np.int16((xx,yy))

            x1,x2 = min((x1,x2)), max((x1,x2))
            y1,y2 = min((y1,y2)), max((y1,y2))

            if (x1==x2) and (y1==y2):
                histIsRunning = True
                plotHist(img, fig2, ax2)
                histIsRunning = False
            elif( (x1<x2) and (y1<y2) ):
                CLICK_BUF1.append((x2,y2))
                histIsRunning = True
                #create mask
#                 mask = ( (colInd>=x1)*(colInd<=x2) ) * ( (rowInd>=y1)*(rowInd<=y2) )
#                 mask = np.dstack([mask]*3)
                selection = img[y1:y2,x1:x2,:]
                plotHist(selection, fig2, ax2)

                histIsRunning = False
                CLICK_BUF1 = []


def handleClick2(axis,xx):
    global AX_DIC
    global fig2
    global ax2
    global darkenIsRunning
    xval = np.round(xx)
    offset = 5

    #set the box
    low =  max(0,xval-offset)
    high = min(300,xval+offset)
    try:
        rng = AX_DIC[axis]
        spn = rng.get_xy()
        spn[:,0] = [low,low,high,high,low]
        rng.set_xy(spn)
    except KeyError:
        rng = axis.axvspan(low,high,facecolor='lime',alpha=0.5)

    AX_DIC[axis] = (rng)
    fig2.canvas.draw()

    if (len(AX_DIC.keys()) == 3) and darkenIsRunning == False:

        darkenIsRunning = True
        mask = np.ones(img.shape[:2])
        coeff = 0.25*mask

        #create mask
        for i,ax in enumerate(ax2):
            rng = AX_DIC[ax]
            low = rng.get_xy()[0][0]
            high = rng.get_xy()[2][0]
            layer = img[:,:,i]
            mask = mask * (layer <= high) * (layer >= low)


        coeff = coeff + 0.75*mask
        coeff = np.dstack([coeff]*3)
        darkenIsRunning = False
        ax1.imshow(np.uint8(coeff*img))
        fig1.canvas.draw()




def onPicClick(event):
    handleClick1(event.xdata,event.ydata)

def onHistClick(event):
    handleClick2(event.inaxes,event.xdata)



if __name__ == "__main__":
    dpath = 'images'
    fname = 'ml.jpg'
    infile = os.path.join(dpath,fname)
    img = nd.imread(infile)

    nrow, ncol = img.shape[:2]
    rowInd = np.arange(nrow*ncol).reshape(nrow,ncol) / ncol
    colInd = np.arange(nrow*ncol).reshape(nrow,ncol) % ncol
    ysize = 9.
    xsize = ysize*float(img.shape[1])/float(img.shape[0])

    plt.ion()
    fig1, ax1 = plt.subplots(num=1,figsize=(xsize,ysize))
    fig1.subplots_adjust(0,0,1,1)
    connectID1 = fig1.canvas.mpl_connect('button_press_event', onPicClick)

    fig1.canvas.set_window_title(fname)
    ax1.axis('off')
    im1 = ax1.imshow(img)
    fig1.canvas.draw()


    fig2, ax2 = plt.subplots(3,1,num=2,figsize=[12,8])
    connectID2 = fig2.canvas.mpl_connect('button_press_event', onHistClick)
    plotHist(img, fig2, ax2)
    plt.show(block=True)

