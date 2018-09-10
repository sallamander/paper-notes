# [Very Deep Convolutional Networks for Large-Scale Image Recognition](https://arxiv.org/abs/1409.1556)

Date: 09/04/2014  
Tags: task.object_classification, task.object_localization, task.action_classification

- The authors are motivated to investigate the effect of convolutional network depth on accuracy in a large-scale image recognition setting (i.e. ImageNet). Their aim is to fix other parameters of the network architecture and steadily increase the depth of the network by adding more convolutional layers.
- The authors propose an architecture built around very small (3x3) convolutional filters, and perform a thorough evaluation on the effect of increasing depth
    - They are motivated to use 3x3 convolutions instead of larger 7x7 ones (i.e. of ZFNet) or 11x11 ones (i.e. of AlexNet). Since a stack of 3x3 conv layers replaces a single 7x7:
        - The network gains additional discriminative power because there are now three non-linear rectification layers instead of one
        - There are fewer parameters in the network, which can be seen has having a regularizing effect (in addition to possible performance gains from fewer parameters)
    - They test convolutional networks with 11 layers, 13 layers, 16 layers, and 19 layers. Each network has 3 fully connected layers, and the rest are convolutional
    - They test two of the 16 layer networks, one with three 1x1 convolutional layers at the end of the last three conv blocks (where blocks are separated by max pooling) and one with three 3x3 convolutional layers for comparison
        - The motivation to test the 1x1 conv layers is to increase the non-linearity of the decision function (i.e. with the addition of an extra rectification function) without effecting the receptive fields of the conv. layers
- They test their proposed method on the classification and localization tasks of ImageNet, as well as the object classification tasks of Pascal VOC 2007, PASCAL VOC 2012, Caltech-101, and Caltech-256, and the action classification task for VOC 2012
    - They place second in the ILSVRC 2014 (ImageNet) classification challenge, but do have the best *single model* results
    - They placed first in the ILSVRC 2014 (ImageNet) localization challenge. For this network they just used a final layer that predicts bounding box locations instead of the class scores.
    - For PASCAL VOC 2007 and 2012, they set SOTA
    - On Caltech-101, they achieve comparable performance to top performing methods, and on Caltech-256 they set SOTA
    - They achieve SOTA on the VOC 2012 action classification task
- Through training / experimentation, they note:
    - Using local response normalization does not improve on a model without any normalization layers
    - Classification error decreases with increasing depth (i.e. from the 11 layer model to the 19 layer model), but saturates when the depth reaches 19 layers
    - Scale jitter at training time leads to significantly better results than training on images with fixed smallest stride, even though a single scale is used at test time
    - Using scale jitter at test time also leads to better performance
    - Averaging the softmax class posteriors from multiple models improves the performance
