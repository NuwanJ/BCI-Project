import sys
import numpy as np
import sys
from scipy.fftpack import rfft,fftfreq
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def fileRead(fileName,lineToRemove,leftColToRemove,rightColToRemove):
    file  = open(fileName, 'r')
    fullText=file.read()
    lines=fullText.split('\n')

    #print('Read '+str(len(lines))+' lines')

    for x in range(lineToRemove):
        lines.pop(0)


    ar=[]
    for x in range(len(lines)):
        temp=[]
        fields=lines[x].split(",")
        for xx in range(len(fields)):
            fields[xx]=fields[xx].strip()

        for y in range(leftColToRemove,len(fields)-rightColToRemove):
            #print('converting to float >>>'+fields[y])
            temp.append(float(fields[y]))
        if len(temp)==0:
            continue
        ar.append(temp)
        #print('Reading line '+str(x)+' \r')
        sys.stdout.flush()

    npar=np.zeros((len(ar), len(ar[0])))
    for i in range(len(ar)):
        for j in range(len(ar[0])):
            npar[i][j] = ar[i][j]
    return npar.transpose()

def nextpow2(i):
    """
    Find the next power of 2 for number i
    """
    n = 1
    while n < i:
        n *= 2
    return n


def readFiles(fileNameList):
    NO_OF_CHANNELS=8

    PASS_BAND_LOW=3.0
    PASS_BAND_HIGH=50.0
    NO_OF_BANDS=5

    singleBandWidth=(PASS_BAND_HIGH-PASS_BAND_LOW)/NO_OF_BANDS

    interestingBands=[x for x in range(NO_OF_BANDS)]
    allChannelBandResults=np.zeros((NO_OF_CHANNELS,len(interestingBands)))

    fileNames=fileNameList#["openBCI_2013-12-24_meditation.txt"]
    Y=[1]
    for file in range(len(fileNames)):
        ar=fileRead(fileNames[file],4,1,3)#complete

        for chan in range(len(ar)):
            bandResults = np.zeros(len(interestingBands))
            bandCount = np.zeros(len(interestingBands))

            freqSpectrum=rfft(ar[chan,:])
            timeStep=1.0/250
            n=len(ar[chan])
            freq=fftfreq(n,d=timeStep)

            endIndex=0
            startIndex=0
            while(freq[startIndex]<PASS_BAND_LOW):
                startIndex+=1
            while(freq[endIndex]<PASS_BAND_HIGH):
                endIndex+=1
            endIndex-=1

            freqSpectrum=np.abs((freqSpectrum[startIndex:endIndex]))
            freq=(freq[startIndex:endIndex])
            '''plt.figure()
            plt.plot(freq, freqSpectrum)'''
            #plt.plot(range(len(freq)),freq)
            for f in range(len(freq)):
                if(freq[f]>0):
                    bandResults[int((freq[f]-PASS_BAND_LOW)/singleBandWidth)]+=freqSpectrum[f]
                    '''band=0
                    for bb in range(len(interestingBands)):
                        if interestingBands[bb]>freq[f]:
                            band=bb-1
                            break

                    bandResults[band]+=np.abs(freqSpectrum[f])
                    bandCount[band]+=1'''
            '''
            for x in range(len(bandResults)):
                if bandCount[x]<1:
                    bandResults[x]=0
                else:
                    bandResults[x]=bandResults[x]/(1.0*bandCount[x])'''

            allChannelBandResults[chan]=bandResults
            #print('channel ',chan+1,'of ',len(allChannelBandResults),' channels completed')

        #print(allChannelBandResults)
        #put the plot code here


        '''for i in range(NO_OF_CHANNELS):
            plt.figure()
            plt.plot(interestingBands, allChannelBandResults[i,:])
        plt.show()'''


        return allChannelBandResults.flatten()



def readFileAndMakeFeatureVector(fileName):

    return readFiles([fileName])






#readFiles(sys.argv[1:])


#fileRead(sys.argv[1])



DIMENSIONS=int(sys.argv[1])
TRAINING_DATA_POINTS=int(sys.argv[2])
TEST_DATA_POINTS=int(sys.argv[3])



X=np.zeros((TRAINING_DATA_POINTS,DIMENSIONS))
Y=np.zeros((TRAINING_DATA_POINTS))


for f in range(TRAINING_DATA_POINTS):
    fileName=sys.argv[4+2*f]#input('Enter file name\n')
    X[f]=readFileAndMakeFeatureVector(fileName)
    Y[f]=int(sys.argv[5+2*f])#input('Enter class\n'))
    print('file: ',sys.argv[4+2*f],'class: ',sys.argv[5+2*f])


print('Finished importing data')

from sklearn import svm


#clf = svm.SVC(kernel='poly',degree=1)
clf = svm.SVC()

print('fitting to X,Y',X.shape,Y.shape)
clf.fit(X, Y)


fig=plt.figure()
ax = fig.add_subplot(111, projection='3d')

aa=8
bb=3
cc=1
for zz in range(80):
    if zz%2==0:
        ax.scatter(X[zz:,aa],X[zz:,bb],X[zz:,cc],marker='.',c='r')
    else:
        ax.scatter(X[zz:, aa], X[zz:, bb], X[zz:, cc], marker='.',c='b')
#plt.show()
print(X[:,1])

correct=0
wrong=0

pre=clf.predict(X)
for x in range(len(X)):
    print('y='+str(Y[x])+' prediction='+str(pre[x]))
    if pre[x] == Y[x]:
        correct += 1
    else:
        wrong += 1

accuracy=(correct*100.0)/(correct+wrong)
print('accuracy='+str(accuracy))


XX=np.zeros((TEST_DATA_POINTS,DIMENSIONS))
YY=np.zeros((TEST_DATA_POINTS))
for ff in range(TEST_DATA_POINTS):
    fileName=sys.argv[(4+2*TRAINING_DATA_POINTS+2*ff)]#'Enter file name\n')
    XX[ff]=readFileAndMakeFeatureVector(fileName)
    YY[ff]=int(sys.argv[5+2*TRAINING_DATA_POINTS+2*ff])#input('Enter calss\n'))

    print('file: ',sys.argv[(4+2*TRAINING_DATA_POINTS+2*ff)],'class: ',sys.argv[5+2*TRAINING_DATA_POINTS+2*ff])


correct=0
wrong=0

pred=clf.predict(XX)

for x in range(len(XX)):
    print(' y='+str(YY[x])+' prediction='+str(pred[x]))
    if pred[x] == YY[x]:
        correct += 1
    else:
        wrong += 1

accuracy=(correct*100.0)/(correct+wrong)
print('accuracy='+str(accuracy))
plt.show()

