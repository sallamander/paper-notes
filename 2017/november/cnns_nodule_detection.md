# [3D Deep Convolution Neural Network Application in Lung Nodule Detection on CT Images](http://luna16.grand-challenge.org/serve/public_html/pdfs/20171128_034629_LUNA16FONOVACAD_NDET.pdf/)

Date: 11/28/2017  
Tags: task.object_detection, task.object_classification, domain.medical

- The authors are motivated to develop a state-of-the-art nodule detection system
- The authors propose a two stage pipeline that consists of:
    - Nodule Candidate Detection Network: They use a 3D U-Net like network that takes as input cropped cubes (they use a 128x128x128 cube that represents 20mmx20mmx20mm in world space) from the lung scan and predict the probability of the patch containing a nodule as well as a nodule center (x, y, z) and radius
    - False Positive Reduction Networks: They ensemble (average) the results from three networks - one that is a fairly vanilla 3D CNN, one that is a 3D residual network, and one that is a 3D cascaded CNN.
    - For overall probability of a nodule being a true nodule or false positive, they use a weighted average of the classification scores from the nodule candidate detection network and false positive reduction networks (at a ratio of 0.4 to 0.6).
- They test their proposed method using the LUNA challenge, and achieve an average FROC of 0.947 (third place at the time of writing).
