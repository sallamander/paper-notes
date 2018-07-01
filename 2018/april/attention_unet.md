# [Attention U-Net: Learning Where to Look for the Pancreas](https://arxiv.org/abs/1804.03999)

Tags: task.semantic_segmentation, domain.medical, topic.deep_supervision, topic.soft_attention

- Their major goal / motivation is be able to avoid the multi-scale / hierarchical / complex networks that are typically cooked up for segmentation tasks to capture objects at different scales
- Take the soft attention mechanism proposed in [Learn to Pay Attention](https://arxiv.org/abs/1804.02391) a step further by proposing grid-based gating that is conditioned on image spatial information
    - The gating signal is conditioned on down-sampled feature maps and only applied to the skip connection image (rather than the final out (e.g. of a dense layer) in previous work)
    - They use additive attention (as formulated in [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473)) rather than multiplicative attention
    - They utilize sigmoid activations in the attention gates instead of softmax to avoid successive applications of a softmax leading to excessive sparsity
- They benchmark it against a standard UNet on multi-class abdominal CT segmentation
    - All networks use deep supervision to force the intermediate feature-maps to be semantically discriminative at each image scale
    - They see ~3-4% improvements on dice for some tasks (statistically significant for CT-150 tasks), which is largely due to higher recall
    - For the CT-82 tasks, they did not improve upon SOTA, but many of the SOTA approaches are multi-stage approaches and / or much more intricate (e.g 2D RNN based)
    - They visualize some of the attention maps, which do appear to be focused on the relevant regions of interest
