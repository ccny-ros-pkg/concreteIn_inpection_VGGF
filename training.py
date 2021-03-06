#run  THEANO_FLAGS="device=gpu1,floatX=float32" python YL_proj_detection.py
import numpy as np
import theano
import theano.tensor as T
import lasagne


import skimage.transform
import sklearn.cross_validation
import pickle
import os



##build the vgg model

from lasagne.layers import InputLayer, DenseLayer, NonlinearityLayer,DropoutLayer
from lasagne.layers.dnn import Conv2DDNNLayer as ConvLayer
from lasagne.layers import Pool2DLayer as PoolLayer
from lasagne.nonlinearities import softmax
from lasagne.utils import floatX

def build_model():
    net = {}
    net['input'] = InputLayer((None, 3, 224, 224))
    net['conv1_1'] = ConvLayer(net['input'], 64, 3, pad=1,trainable=False)
    net['conv1_2'] = ConvLayer(net['conv1_1'], 64, 3, pad=1,trainable=False)
    net['pool1'] = PoolLayer(net['conv1_2'], 2)
    net['conv2_1'] = ConvLayer(net['pool1'], 128, 3, pad=1,trainable=False)
    net['conv2_2'] = ConvLayer(net['conv2_1'], 128, 3, pad=1,trainable=False)
    net['pool2'] = PoolLayer(net['conv2_2'], 2)
    net['conv3_1'] = ConvLayer(net['pool2'], 256, 3, pad=1,trainable=False)
    net['conv3_2'] = ConvLayer(net['conv3_1'], 256, 3, pad=1,trainable=False)
    net['conv3_3'] = ConvLayer(net['conv3_2'], 256, 3, pad=1,trainable=False)
    net['pool3'] = PoolLayer(net['conv3_3'], 2)
    net['conv4_1'] = ConvLayer(net['pool3'], 512, 3, pad=1,trainable=False)
    net['conv4_2'] = ConvLayer(net['conv4_1'], 512, 3, pad=1,trainable=False)
    net['conv4_3'] = ConvLayer(net['conv4_2'], 512, 3, pad=1,trainable=False)
    net['pool4'] = PoolLayer(net['conv4_3'], 2)
    net['conv5_1'] = ConvLayer(net['pool4'], 512, 3, pad=1,trainable=False)
    net['conv5_2'] = ConvLayer(net['conv5_1'], 512, 3, pad=1)
    net['conv5_3'] = ConvLayer(net['conv5_2'], 512, 3, pad=1)

    net['pool5'] = PoolLayer(net['conv5_3'], 2)
    net['fc6'] = DenseLayer(net['pool5'], num_units=4096)
    net['fc6_dp']=DropoutLayer(net['fc6'],p=0.)
    net['fc7'] = DenseLayer(net['fc6_dp'], num_units=4096)
    net['fc8'] = DenseLayer(net['fc7'], num_units=1000, nonlinearity=None)
    net['prob'] = NonlinearityLayer(net['fc8'], softmax)

    return net




# Load model weights and metadata
d = pickle.load(open('vgg16.pkl'))

#setting batch size for the whole training
BATCH_SIZE = 25
MEAN_IMAGE=np.load('vgg_mean.npy')


# Build the network and fill with pretrained weights
net = build_model()

lasagne.layers.set_all_param_values(net['conv5_1'], d['param values'][0:22],trainable=False)
lasagne.layers.set_all_param_values(net['prob'], d['param values'][22:32],trainable=True)


#testing phase

with np.load('project/detectionOfSpalling/YL_50iter.npz') as f:
    param_values = [f['arr_%d' % i] for i in range(len(f.files))]
    print(range(len(param_values)))
print len(param_values)

lasagne.layers.set_all_param_values(net['fc7_2048'], param_values[:30])


print 'loading successfully...'





##begin to train the model 

##first just configure
half_feature_layer=DenseLayer(net['fc6_dp'],num_units=2048)
half_feature_layer_dp=DropoutLayer(half_feature_layer,p=0.)
output_layer=DenseLayer(half_feature_layer_dp,num_units=2,nonlinearity=softmax)
final_prob=NonlinearityLayer(output_layer, softmax)

# enable this part if you want to continue previous training

#with np.load('/home/ericyanng/ericFiles/deepLN/theano/project/detectionOfSpalling/YL_50iter.npz') as f:
#    param_values = [f['arr_%d' % i] for i in range(len(f.files))]
#lasagne.layers.set_all_param_values(output_layer, param_values)

# Define loss function and metrics, and get an updates dictionary
X_sym = T.tensor4()
y_sym = T.ivector()

prediction = lasagne.layers.get_output(final_prob, X_sym)
loss = lasagne.objectives.categorical_crossentropy(prediction, y_sym)
loss = loss.mean()

acc = T.mean(T.eq(T.argmax(prediction, axis=1), y_sym),
                      dtype=theano.config.floatX)

# you can set adpative weight here

params = lasagne.layers.get_all_params(final_prob, trainable=True)
updates = lasagne.updates.nesterov_momentum(
        loss, params, learning_rate=0.0001, momentum=0.9)


# Compile functions for training, validation and prediction
train_fn = theano.function([X_sym, y_sym], loss, updates=updates)
val_fn = theano.function([X_sym, y_sym], [loss, acc])
pred_fn = theano.function([X_sym], prediction)



# generator splitting an iterable into chunks of maximum length N
def batches(iterable, N):
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk)==N:
            rst=chunk
            chunk=[]
            yield rst
    if chunk:
        yield chunk

# We need a fairly small batch size to fit a large network like this in GPU memory

def train_batch():
    trdata,trlb=imdata(imglist)
    trdata=trdata-MEAN_IMAGE
    return train_fn(trdata,trlb)

def test_batch():
    tsdata,tslb=imdata(ixx)
    tsdata=tsdata-MEAN_IMAGE
    return val_fn(tsdata,tslb)

def val_batch():
    ix = range(len(y_val))
    np.random.shuffle(ix)
    ix = ix[:BATCH_SIZE]
    return val_fn(X_val[ix], y_val[ix])

def testbatch(fls):
    Num=len(fls)
    datablob=np.ndarray((Num,3,224,224))
    datalb=np.zeros((Num,))
    im224=np.zeros((3,224,224))
    for i,f in enumerate(fls):
        fname,flabel=f.split(',')
        imi=cv2.imread('/path/to/testing/imags/folder/'+fname)
        #cv2 read img as 3xNxN and with BGR

        for t in range(3):
            im224[t,:,:]=cv2.resize(imi[t,:,:],(224,224))
        datablob[i,:,:,:]=im224

        #then the label 
        datalb[i]=int(flabel)
    datablob=datablob.astype('float32')
    datalb=datalb.astype('int32')
    return datablob,datalb

#load the files first then deliver thedata when needed.

import random
import cv2
def imdata(fls):
    datablob=np.ndarray((BATCH_SIZE,3,224,224))
    datalb=np.zeros((BATCH_SIZE,))
    n=len(fls)
    random.shuffle(fls)
    fls=fls[:BATCH_SIZE]
    im224=np.zeros((3,224,224))
    for i,f in enumerate(fls):
        fname,flabel=f.split(',')
        imi=cv2.imread('/path/to/training/imags/folder/'+fname)
        #cv2 read img as 3xNxN and with BGR

        for t in range(3):
            im224[t,:,:]=cv2.resize(imi[:,:,t],(224,224))
        datablob[i,:,:,:]=im224
        #then the label 
        datalb[i]=int(flabel)
    datablob=datablob.astype('float32')
    datalb=datalb.astype('int32')
    return datablob,datalb


listtrainpath='/path/to/train_list.txt'
listtestpath='/path/to//test_list.txt'
impath='/path/to/detectionOfSpalling'

fp=open(listtrainpath)
imglist=fp.readlines()

#reading test list,ixx contain all the test image names
ft=open(listtestpath)
ixx=ft.readlines()


trdata,trlb=imdata(ixx)



# print 'begin training'

for epoch in range(0):
    for batch in range(20):
        loss = train_batch()
        # print loss
    print 'epoch ',epoch, ',Train loss is ', loss
    loss,acc=test_batch()
    print 'Test loss and acc:',loss,acc
    # enable this if you want to save the model every 50 steps
    # if (epoch+1)%50==0:
    #     np.savez('data/model_YL_'+str(epoch+1)+'.npz', *lasagne.layers.get_all_param_values(output_layer))
    
loss_tot = 0.
acc_tot = 0.

print 'direct testing'
for chunk in batches(ixx, BATCH_SIZE):
    #got all the data based on index
    tsdata,tslb=imdata(chunk)
    tsdata=tsdata-MEAN_IMAGE
    loss, acc = val_fn(tsdata, tslb)
    print loss,acc
    loss_tot += loss * len(chunk)
    acc_tot += acc * len(chunk)

loss_tot /= len(ixx)
acc_tot /= len(ixx)
print  loss_tot, acc_tot * 100

# save the model
np.savez('data/'+'YL_50iter'+'.npz', *lasagne.layers.get_all_param_values(output_layer))
