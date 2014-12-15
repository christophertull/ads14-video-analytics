import os, sys, time
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as nd
from scipy.ndimage.filters import median_filter as mf
from collections import Counter

#------------------------------------------------------------
#getCoeffsOLS()
#------------------------------------------------------------
def getCoeffsOLS(avgs,samp):
    PT = avgs
    P  = PT.transpose()
    PTPinv = np.linalg.inv(np.dot(PT,P))
    PTyy = np.dot(PT,samp.flatten())
    avec = np.dot(PTPinv,PTyy)
    return avec

#------------------------------------------------------------
#plotHistograms()
#------------------------------------------------------------
def plotHistograms(histData):
    colors = ['b','r']
    for i in range(10):
        fig0,ax0 = plt.subplots(1,10,figsize=(20,2))
    #     fig0.subplots_adjust(0.05,-0.1,0.95,0.95)
        fig0.canvas.set_window_title("Distribution of coefficients for handwritten %ds"%i)
        [ax0[j].hist(histData[i,j], bins=20, color=colors[j==i]) for j in range(10)]
        [ax0[j].set_yticklabels('') for j in range(10)]
        [ax0[j].set_xlim(-1.5,2) for j in range(10)]
        [ax0[j].xaxis.set_ticks(np.arange(-2,3,1)) for j in range(10)]
        [ax0[j].set_xlabel("Template: %d"%j) for j in range(10)]
    #     fig0.canvas.draw()
        plt.tight_layout()
        plt.show(block=False)

#------------------------------------------------------------
#getIncorrect()
#------------------------------------------------------------
def getIncorrect(histData):
    incorrectSamples = [[]]*10
    for i in range(10):
        wrongAnswers = []
        for j in range(500):
            guess = np.argmax(histData[i,:10,j])
            if guess != i:
                wrongAnswers.append(guess)
                incorrectSamples[i].append((numList[i,j],guess,i))


        cnts = Counter(wrongAnswers)
        outstr = "%0.1f%% of %d's were incorrectly identified, the most common guess for those failures was %d"%                      (100*(len(wrongAnswers)/500.0), i, cnts.most_common(1)[0][0])
        print(outstr)
    return np.array(incorrectSamples)

#------------------------------------------------------------
#getRandomPic()
#------------------------------------------------------------
def getRandomPic(pics):
    num = int(np.random.uniform(0,10))
    return pics[num,int(np.random.uniform(0,len(pics[num])))]

#------------------------------------------------------------
#playVideo()
#------------------------------------------------------------
def playVideo(incorrect, videoDur=30, frameDur=1):
    plt.close(1)
    time.sleep(1)
    fig1, ax1 = plt.subplots(1,2,num=1,figsize=[10,5])
#     fig1.subplots_adjust(0,0,1,1)
    [axis.axis('off') for axis in ax1]
    pic,guess,actual = getRandomPic(incorrect)
    im11 = ax1[0].imshow(pic)
    im12 = ax1[1].imshow(nums_avg[guess])
    ax1[0].set_title('Handwritten %d'%actual)
    ax1[1].set_title('Algorithm guessed %d'%guess)
    fig1.canvas.draw()
    plt.show(block=False)

    t0 = time.time()
    dt = 0.0
    while dt<videoDur:
        pic,guess,actual = getRandomPic(incorrect)
        im11.set_data(pic)
        im12.set_data(nums_avg[guess])
        ax1[0].set_title('Handwritten %d'%actual)
        ax1[1].set_title('Algorithm guessed %d'%guess)
        fig1.canvas.draw()
        time.sleep(frameDur)
        dt = time.time()-t0

    pic,guess,actual = getRandomPic(incorrect)
    im11.set_data(pic)
    im12.set_data(nums_avg[guess])
    ax1[0].set_title('Handwritten %d'%actual)
    ax1[1].set_title('Algorithm guessed %d'%guess)
    fig1.canvas.draw()
    plt.show(block=True)



if __name__ == "__main__":
    img = nd.imread('images/digits.png')
    nrow, ncol = img.shape[0:2]

    #crop into individual images
    nums = img.reshape(50,20,100,20).transpose(0,2,1,3).reshape(5000,20,20)
    #calculate average templates
    nums_avg = np.array([nums[i*500:(i+1)*500].mean(0) for i in range(10)])
    #group the images by the digit they represent
    numList = np.array([nums[i*500:(i+1)*500] for i in range(10)])
    #reshape the templates into matrix for regression
    avg_matrix = nums_avg.reshape(10,400)
    #add on a bunch of ones as our constant
    avg_matrix = np.vstack((avg_matrix, np.ones((1,400))) )

    #populate the histogram data
    histData = np.ndarray((10,10,500))
    for i in range(10):
        #for each picture representing that digit
        for j,pic in enumerate(numList[i]):
            coeffs = getCoeffsOLS(avg_matrix,pic)
            histData[i,:,j] = coeffs[:10]


    #display histograms
    plotHistograms(histData)
    incorrectSamples = getIncorrect(histData)
    playVideo(incorrectSamples)



    #recalculate using the constant row
    histData = np.ndarray((10,11,500))
    for i in range(10):
        #for each picture representing that digit
        for j,pic in enumerate(numList[i]):
            coeffs = getCoeffsOLS(avg_matrix,pic)
            histData[i,:,j] = coeffs[:]



    print('Removing zero point offset')
    adjustedIncorrect = getIncorrect(histData)




