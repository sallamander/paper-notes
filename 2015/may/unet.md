# [U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)

Tags: task.semantic_segmentation, domain.medical

- The authors are motivated to overcome the two major drawbacks of patch-based approaches for semantic segmentation
    - Drawbacks:
        1. The network is slow and / or there is a lot of wasted compute, since there are significantly overlapping regions among the patches.
        2. There is a tradeoff between larger and smaller patches that has to be optimized for; larger patches offer more context but require more max-pooling layers that may lower the localization accuracy, while smaller patches might not give enough context.
- Instead of building on patch-based classification approaches, they build on the FCN architecture
    - They modify / extend this architecture to have contracting and expanding paths, with "skip" connections in between that copy the input from the contracting path to the expanding path (but also crop it to ensure that it's size matches up; the cropping is necessary because of the use of valid padding)
        - They pass full resolution feature maps through the skip connections
    - They do multiple convolutional layers followed by max pooling, and double the number of feature maps after each max pooling layer
        - They use only the "valid" parts of the image (i.e. they use valid pooling), which allows for easier segmentation of large images at inference time
- They test their network on the EM segmentation challenge (started at ISBI 2012) as well as the ISBI 2014-2015 cell segmentation challenge
    - They use a weighted loss that puts a heavier weight on the separating boundaries between cells, and do this by creating a weight map using morphological operations
    - They favor large input images over large batch sizes, and only train with a batch size of 1
    - They use heavy amounts of data augmentation
    - They outperform all other methods on the Warping Error for the EM segmentation challenge and perform reasonably well (although worse than other methods) for the other metrics
    - They significantly outperform other methods in terms of IOU with respect to the ISBI 2014-2015 challenge
