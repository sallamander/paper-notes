# [ENet: A Deep Neural Network Architecture for Real-Time Semantic Segmentation](https://arxiv.org/abs/1606.02147) 

Tags: task.semantic_segmentation, domain.mobile, topic.efficiency

- The authors were motivated to find a segmentation network architecture that had good performance but also could operate in real time on low-power devices (e.g. mobile). Current networks do not operate well on low-power devices without some kind of pruning.
- They utilize an encoder-decoder type network that is created specifically for tasks requiring low latency operation (its 18x faster, requires 75x less FLOPS, and has 79x fewer parameters than a comparison SegNet).
    - Their network has two unique blocks / modules to it:
        1. Initial block: It applies 2 separate pathways to the input and then concats the results at the end.
            1. Pathway A: 3x3 conv. with stride 2
            2. Pathway B: Max pooling
        2. Bottleneck modules, which consist of three convolutional layers: a 1x1 projection that reduce the dimensionality, a main convolutional layer (dilated or asymmetric), followed by a 1x1 expansion layer.
    - In the decoder, max pooling is replaced with max unpooling, done saving the indices of elements chosen in max pooling layers (following the SegNet approach)
    - Design decisions included: 
        1. Early downsampling in the initial blocks, motivated by considering that visual information is highly redundant and hypothesizing that this information could be compressed into a more efficient representation. They found that increasing the number of initial feature maps from 16 to 32 didn't help (on Cityscapes), although I don't know why this supports early downsampling.
        2. A small decoder, motivated by the thought that the role of the decoder is to upsample the output of the encoder and simply fine-tune the details.
        3. Replacing all ReLUs with PReLUs. They initially found that using ReLUs and Batch Normalization before convolutions has negative effects. They found that in the encoder, most PReLUs behaved like ReLUs, but that in the decoder they acted more like an identity function (e.g. with slope of 1 in the < 0 part); they claim that this supports their hypothesis that the decoder is simply used to fine-tune details, but their plot doesn't show that a good number of the slopes are close to 1.
        4. Factorizing filters (i.e using a $1 x n$ followed by a $n x 1$), allowing them to learn a more diverse set of functions and increase the receptive field (because they could use a $1 x 5$ followed by a $5 x 1% instead of a 3x3). 
        5. Using dilated convolutions in some of the bottleneck modules - they found that interleaving these with other kinds of convolutions worked best. 
        6. Spatial Dropout; this worked better than L2 regularization and stochastic depth.
- They tested on CamVid, Cityscapes, and SUN RGB-D datasets against a SegNet baseline.
    - Their network was significantly faster and used much less memory.
    - ENet generally performed better (with most IoU metrics - class, class instance-level, category, and category instance-level) on Cityscapes, in 6 / 11 classes on CamVid (and on overall class avg. but not on class IoU), and worse on SUN RGB-D on all metrics
