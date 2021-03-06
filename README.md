#updated a pytorch version, please check here
Requires pytorch 0.3 or 0.4
https://github.com/ccny-ros-pkg/pytorch_Concrete_Inspection.git

## Concrete Inpection Dataset and Baseline @ [CCNY Robotics Lab](https://ccny-ros-pkg.github.io/)

Authors: [Liang Yang](https://ericlyang.github.io/),  [Bing LI](https://robotlee2002.github.io/), [Wei LI](http://ccvcl.org/~wei/), Zhaoming LIU, Guoyong YANG, [Jizhong XIAO](http://www-ee.ccny.cuny.edu/www/web/jxiao/jxiao.html)


CCNY Concrete Structure Spalling and Crack database (CSSC) that aims to assist the civil inspection of performing in an automatical approach. In the first generate of our work, we mainly focusing on dataset creation and prove the concepts of innovativity. We provide the first complete the detailed dataset for concrete spalling and crack defects witht the help from Civil Engineers, where we also show our sincere thanks to the under-graduate student at Hostos Community College for their effort on data labeling. For our experiments, we deliever an UAV to perform field data-collection and inspection, and also perform a 3D semantic metric resconstructiont. 


### If you find this could be helpful for your project, please cite the following related papers:

[IROS 2017] Liang YANG, Bing LI, Wei LI, Zhaoming LIU, Guoyong YANG,Jizhong XIAO (2017). Deep Concrete Inspection Using Unmanned Aerial Vehicle Towards CSSC Database. 2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), [PDF](https://ericlyang.github.io/img/IROS2017/IROS2017.pdf).


[ROBIO 2017] Liang YANG, Bing LI, Wei LI, Zhaoming LIU, Guoyong YANG,Jizhong XIAO (2017). A Robotic System Towards Concrete Structure Spalling And Crack Database. 2017 IEEE Int. Conf. on Robotics and Biomimetics (ROBIO 2017), [Project](https://ericlyang.github.io/project/deepinspection/).


### The under going project

If you are interested in this project, please check the [project link](https://ericlyang.github.io/project/deepinspection/) and our current 3D semantic pixel-level reconstruction [project](https://ericlyang.github.io/project/robot-inspection-net/). Also, you can shoot [Liang Yang](https://ericlyang.github.io/) an email any time for other authors.


#### Check our latest progress with demo:

If you have interests, please visit the project [repository link](https://github.com/ccny-ros-pkg/inspectionNet_Segmentation).

<a href="https://www.youtube.com/watch?v=DZJNjF2r0G0" target="_blank"><img src="https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/blob/master/resultImages/resultImages/0054.png" 
alt="InspectionNet" width="640" height="480" border="10" /></a>

#### Check our previous progress with demo:
<a href="https://www.youtube.com/watch?v=4_001iFYgJo" target="_blank"><img src="https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/blob/master/resultImages/resultImages/2.jpg" 
alt="InspectionNet" width="640" height="480" border="10" /></a>

## 1. Prerequisites

The inspection network is trained based on [theano](http://deeplearning.net/software/theano/) and using [Lasagne Api](https://github.com/Lasagne/Lasagne). We performed training and evaluation on version:

>-  Tested Theano Version: '0.8.2'
>-  Lasagne version: '0.1'

If you change to the latest version, it should work with minor modification.


### 1.1 To enable a customized fine tuning, we  modified the Lasagne

Please follow the [instruction we provided](https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/tree/master/changeForLasagne) to modify your lasagne to be able to train in your our computer.


### 1.2 The Computer

Our computer is a desktop with a GTX 1080 8G GPU inside and 32G memory, and it cann achieve 150 frames per second. We also tested on Dell Xps 15 with GTX 960M 2G GPU it can also achieve a 50 frames per second rate.

### 1.3 Other libraries

> - [Opencv](https://github.com/opencv/opencv) any verson is good, recomend the latest.
> - sudo pip install skimage
> - sudo pip install pickle
> - sudo pip install sklearn


## 2. Data set

For training, the region detection approach we proposed in paper [IROS 2017](https://ericlyang.github.io/img/IROS2017/IROS2017.pdf) are sub-cropped images with 'true' or 'false' label. We provide two kind of data for your consideration:1) the orginal image and the labeled data, where spalling images are labeled with erosed-rebar and cracking images are labeled with the crack region. 

Here is an example of the orginal image and labeled image for cracking and spalling, respectively:

(1) Cracking:

![](https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/blob/master/resultImages/labeled_images/crack/045.jpg)
![](https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/blob/master/resultImages/labeled_images/crack/045_GT.jpg)

(2) Spalling:

![](https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/blob/master/resultImages/labeled_images/spalling/001.jpg)
![](https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/blob/master/resultImages/labeled_images/spalling/001.png)

Also, here is an example of our sub-cropped images for region based training and testing purposed, which is mainly used for our papers purpose. We put this part of dataset in DropBox, and here are links for [Crack Sub-images](https://www.dropbox.com/s/m5zg2s0gxu6ygor/crackSubImageForTraining.rar?dl=0) and [Spalling Sub-images](https://www.dropbox.com/s/r3sxj33mz1gkt2a/spallSubImageForTraining.rar?dl=0). Please be noted that if you use the dataset for publication purpose, please cite the above papers.

We also open access our crack/spalling original and labeled iamges without sub-croping, please email [Liang Yang](https://ericlyang.github.io/) for the dataset.


## 3. Training and Testing

For training, we provid the simple demo which is based on VGG-16. Please download the data provided above and put into the folder [deepLearningBridgeInspection](https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/tree/master/deepLearningBridgeInspection), also please generate the corresponding training and testing list as explained in [generate_training_and_testing_img_list.py](https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/blob/master/generate_training_and_testing_img_list.py), and we also provide an example list [train_list.txt](https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/blob/master/train_list.txt) and [test_list.txt](https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/blob/master/test_list.txt) for your consideration.


To train the model, you also need to download the [vgg-16 pre-trainined model](https://mega.nz/#!YU1FWJrA!O1ywiCS2IiOlUCtCpI6HTJOMrneN-Qdv3ywQP5poecM), and modify the path in [training.py]()!! Very important!!, then:

>- python training.py


The demo can be run as:

> - python demo.py


The region detection results is as following:

![](https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/blob/master/resultImages/resultImages/1.jpg)

![](https://github.com/ccny-ros-pkg/concreteIn_inpection_VGGF/blob/master/resultImages/resultImages/4.jpg)
