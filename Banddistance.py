# -*- coding: utf-8 -*-


from __future__ import print_function
import numpy as np
#np.random.seed(1337)#it will generate the same random number array
from keras.utils  import np_utils
import random
from scipy import io


def distansDensity(data,nbSubpace,nbofBandsSel):     
    nbofSamples=data.shape[0]
    datashape1=data.shape[1]

    if datashape1==1:
        nbofAllBand=data.shape[2]
        data=data.reshape([nbofSamples,nbofAllBand])
         
    
    
    nbofAllBand=data.shape[1]
    
    d_distance=np.zeros((nbofAllBand))
    d_density=np.zeros((nbSubpace))    
    

    dsum=np.sum(data,axis=0)

    for j in range(nbofAllBand-1):
        d_distance[j]=d_distance[j]+np.abs(dsum[j+1]-dsum[j])
    
    nbBandSubpace=nbofAllBand//nbSubpace
    for i in range(nbSubpace):
        sss=np.sum(d_distance[i*nbBandSubpace:(i+1)*nbBandSubpace])
        print(sss)
        d_density[i]=sss//nbBandSubpace
        print(d_density[i])
    
    d_den_sum=np.sum(d_density)
    
    d_selectnumber=np.zeros((nbSubpace)) 
    d_selectnumber=np.round((d_density/d_den_sum)*nbofBandsSel)
    

    if d_selectnumber.sum()==nbofBandsSel:
        return d_selectnumber
    else:        
        if d_selectnumber.sum()>nbofBandsSel:
            d_selectnumber[0]=d_selectnumber[0]-1
        else:
            d_selectnumber[d_selectnumber.size-1]=d_selectnumber[d_selectnumber.size-1]+1
        return d_selectnumber


def getAvergeWave(data,label,classNO):
    nbOneClass=getOneClass(data,label,classNO)#dataOneClass.shape=[n,200]
    
    nb=nbOneClass.shape[0]
    averageWave=np.zeros([nbOneClass.shape[1]])
    
    for i in range(nb):
        averageWave +=nbOneClass[i,:]
    averageWave= averageWave/nb
    return averageWave


def getOneClass(data,label,classNO):
    
    if data.shape[1]==1:
        data=data.reshape([data.shape[0],data.shape[2]])
    dataBandNumber=data.shape[1]
    
    nbClassNumber=0
    for i in range(data.shape[0]):
        if(label[i]==classNO):
            nbClassNumber+=1
    #print(nbClassNumber)
    
    dataOneClass=np.zeros([nbClassNumber,dataBandNumber])#[1428,200]如果是第一类的话
    
    nbClassNumber=0
    for i in range(data.shape[0]):
        if(label[i]==classNO):
            dataOneClass[nbClassNumber,:]=data[i,:]
            nbClassNumber+=1

    return dataOneClass




def getData(datafilepath):
    aaa=np.load(datafilepath)#read from file
    data=aaa["arr_0"]#里面的值是原始值
    label=aaa["arr_1"]
    
    Dtrain=np.empty((1600,1,200),dtype="float32")
    Ltrain=np.empty((1600),dtype="int32")
    #Dtrain1=np.empty((1600,200),dtype="float32")
    
    
    Dtrain=data[:1600,:,:]
    Ltrain=label[:1600]
    #Dtrain1=Dtrain.reshape([1600,200,1])
    
    
    Dtest=np.empty((400,1,200),dtype="float32")
    Ltest=np.empty((400),dtype="int32")
    #Dtest1=np.empty((400,200),dtype="float32")
    
    
    Dtest=data[1600:,:,:]
    Ltest=label[1600:]
    #Dtest1=Dtest.reshape([400,200,1])
    
    Dtrain = Dtrain.astype('float32')
    Dtest = Dtest.astype('float32')
    
    

    Ltrain = np_utils.to_categorical(Ltrain, 10)
    Ltest = np_utils.to_categorical(Ltest, 10)
    return data,Dtrain,Ltrain,Dtest,Ltest


def getDataindiafrom_mat():
    datafilepath="Indian_pines_corrected.mat"
    labelfilepath="Indian_pines_gt.mat"
    
    a=io.loadmat(datafilepath)
    aa=io.loadmat(labelfilepath)
    d=a['indian_pines_corrected']
    dOri=a['indian_pines_corrected']

    l=aa['indian_pines_gt']
    d=np.float32(d)
    
    
    
    d /= d.max()
    

    
    dataNormal=np.empty((10249,1,200),dtype="float32")#21025=145*145 ; 其中的0标签是没有标记的标签,有10776个，要剔除
    dataOringin=np.empty((10249,1,200),dtype="float32")
    label=np.empty((10249),dtype="int32")
    
    
    indexofclass=np.array((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16))#class number
    dictofclass={0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}

    
    
    
    index=0
    for i in range(145):#find the no.14 class
        for j in range(145):        
            if (l[i,j]!=0):           
                dataNormal[index,0,:]=d[i,j,:]#获得数据
                dataOringin[index,0,:]=dOri[i,j,:]#获得原始数据
                label[index]=l[i,j]-1#为了后续训练方便，挑出的像素标签相应减1
                #print(i,j,l[i,j],label[index])
                dictofclass[label[index]] += 1 #相应类别数量加1            
                index += 1
    
    
    
    return dataNormal,dataOringin,label




def getDataindia(filepath):
    aaa=np.load(filepath)#read from file
    data=aaa["arr_0"]#里面的值是原始值
    label=aaa["arr_1"]
    
    
    
    return data,label



        

def getLabel(filepath):
    aaa=np.load(filepath)#read from file
    data=aaa["arr_0"]#里面的值是原始值
    label=aaa["arr_1"]
    
    Dtrain=np.empty((1600,1,200),dtype="float32")
    LtrainOri=np.empty((1600),dtype="int32")
    #Dtrain1=np.empty((1600,200),dtype="float32")
    
    
    Dtrain=data[:1600,:,:]
    LtrainOri=label[:1600]
    #Dtrain1=Dtrain.reshape([1600,200,1])
    
    
    Dtest=np.empty((400,1,200),dtype="float32")
    LtestOri=np.empty((400),dtype="int32")
    #Dtest1=np.empty((400,200),dtype="float32")
    
    
    Dtest=data[1600:,:,:]
    LtestOri=label[1600:]
    #Dtest1=Dtest.reshape([400,200,1])
    
    Dtrain = Dtrain.astype('float32')
    Dtest = Dtest.astype('float32')
    
    
    #print(data.shape[0],' samples')
    #print(label.shape[0],'labels')
    
    
    #把整形数值变成向量
    LtrainVex = np_utils.to_categorical(LtrainOri, 10)
    LtestVex = np_utils.to_categorical(LtestOri, 10)
    
    
    
    return LtrainOri,LtrainVex,LtestOri,LtestVex
    


def getalldataLabel(filepath):
    aaa=np.load(filepath)
    data=aaa["arr_0"]
    labelOri=aaa["arr_1"]   
    

    labelvex = np_utils.to_categorical(labelOri, 10)   
    
    
    return data,labelOri,labelvex
    




def generateLocationBandSel(d_selectnumber,nbAllbands):

    location=range(nbAllbands)
    nbZone=d_selectnumber.size
    nbBandofZone=int(nbAllbands/nbZone)
    nbSelect=np.array([])

    for i in range(nbZone):

        nb=random.sample(location[i*nbBandofZone:(i+1)*nbBandofZone-1],int(d_selectnumber[i]))
        
        nbSelect=np.append(nbSelect,nb)
    nbS=np.sort(nbSelect)
    return nbS


def generateLocBandSelRandom200(m):

    location=np.arange(200)
    nbZone=1
    nbBandofZone=200
    nbSelect=np.array([])
    nb=random.sample(location,m)
    nb=np.array(nb)
    return nb





def reverseCategorical(LtestVex):
    uniques=np.array([0,1,2,3,4,5,6,7,8,9])
    a=uniques[Ltest.argmax(1)]
    return a#  

    
def getoneclassdatalabel(nDtest,LtestOri,indexofclass):
    #首先统计每一类的个数
    nbofclass=0
    for i in range(LtestOri.size):
        if (LtestOri[i]==indexofclass):
            nbofclass=nbofclass+1
    
    dataofoneclass=np.empty((nbofclass,200,1))
    
    j=0
    for i in range(LtestOri.size):
        if (LtestOri[i]==indexofclass):
            #print(LtestOri[i])
            dataofoneclass[j,:,:]=nDtest[i,:,:]
            j=j+1
    
    return dataofoneclass,nbofclass
    

def getDataOnlyBS(dataAll,nbBSelect):
    dataBS=np.zeros((dataAll.shape[0],200,1),dtype="float32")
    for i in range(nbBSelect.size):
        dataBS[:,int(nbBSelect[i]),:]=dataAll[:,int(nbBSelect[i]),:]
    return dataBS
    
def getDataOnlyBS2(dataAll,nbBSelect):
    dataBS=np.zeros((10249,200),dtype="float32")
    for i in range(nbBSelect.size):
        dataBS[:,int(nbBSelect[i])]=dataAll[:,0,int(nbBSelect[i])]
    return dataBS


