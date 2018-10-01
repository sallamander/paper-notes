# [YOLOv3: An Incremental Improvement](https://arxiv.org/abs/1804.02767)

Date: 4/11/2018  
Tags: task.object_detection, topic.efficiency

- The authors are motivated to make improvements to YOLO9000
- The authors mainly implement existing ideas on top of YOLO9000
    - Unlike Faster R-CNN, they only assign one bounding box prior for each ground truth object
    - Each box predicts the class using independent logistic classifiers instead of a softmax, since this better models data sources that might have many overlapping labels.
    - They predict boxes at 3 different scales, using a similar concept to feature pyramid networks
    - They use a new network for performing feature extraction; it's a hybrid approach between the network used in YOLOv2, Darknet-19, and some of the more recent residual based networks
        - This network is much more powerful than Darknet-19 (used in previous iterations of YOLO) but more efficient than both ResNet-101 and ResNet-152 (~50% more frames per second than ResNet-101 and nearly 100% more frames per second than ResNet-152)
- The authors test their method using COCO
    - On the mean AP metric across multiple IOUs, their method performs on par with SSD, but is significantly faster
    - On the mean AP metric across multiple IOUs, their method still lags quite a bit behind models like RetinaNet
    - On the "old" detection metric of mean AP at IOU=0.5, their method is quite strong, and nearly on part with RetinaNet (57.9 AP compared to 61.1)
- Through training / experimentation, they note a few things that didn't work:
    - Using the normal anchor box prediction mechanism where you predict the x, y offset as a multiple of the box width or height using a linear activation (i.e. as in R-CNN, Fast R-CNN, Faster-RCNN, RetinaNet, etc.)
    - Using linear predictions to predict the offset instead of logistic activations; this led to a couple point drop in mAP
    - Using focal loss; this led to a ~2 point drop in mAP
    - Using dual IOU thresholds, where positive examples are those greater than some threshold (e.g. 0.7), negative examples are those below some threshold (e.g. 0.3), and examples in between are ignored


## YOLOv3 Performance

![](./images/yolov3_performance.png)
