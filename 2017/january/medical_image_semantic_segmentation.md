# [CNN-based Segmentation of Medical Imaging](https://arxiv.org/abs/1701.03056)

Tags: task.semantic_segmentation, domain.medical

- The authors are motivated to study specific challenges that are present in medical image segmentation (e.g. scarcity of labeled data and class imbalance) and how successfully (or unsuccessfully) different approaches might handle these challenges
    - Very good lit. review in this paper; lots of good references for future reading
- They utilize a 3D UNet type architecture on a bone (hand) segmentation task as well as BRATs, studying particular things for each:
    - For hand segmentation, they looked at:
        - Jaccard loss versus categorical cross entropy
            - Both loss functions perform well on classes that are relatively common in the dataset, but the jaccard loss performs significantly better on the less frequent classes (no tables present, though)
        - Use of long skip connections versus not
            - Removing these drastically reduced performance
        - Use of combining multiple segmentation maps (from the upsampling side) versus using a single segmentation map
            - Both multiple and single segmentation maps showed similar performance on the validation set, but multiple segmentation maps showed better performance on the test set (no tables present, though)
            - Networks using multiple segmentation maps converged much more quickly than those using a single segmentation map
            - For these, they just applied a set of 1x1x1 convolutions followed by upsampling (using bilinear interpolation) before summing / concatenating the additional segmentation map
        - Element-wise summation versus concatenation of the skip connections
            - Concatenation of the features outperformed summation
            - Visualization of the feature maps from each of these scenarios showed that the feature maps generated from concatenating where more unique and also more representative of the final segmentation maps
    - For BRATs, they looked at the performance using each modality on its own as well as the performance achieved using different combinations of the modalities
        - They found that different modalities highlight different features, and that there isn't a single combination of them that gives the best performance across all classes
- Other network details: 
    - Strided convolutions were used in place of max-pooling because they showed slightly better performance on initial experiments
    - They use same padding instead of valid padding (i.e. so that only conv / deconv operations change the size of feature maps)
    - They use PReLU activation functions
    - Convolutions are all 3x3x3, except those used to produce the final segmentation maps as well as those used to reduce the number of feature maps prior to a deconvolution
