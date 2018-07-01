# [Cardiac Motion Scoring with Segment- and Subject-level Non-Local Modeling](https://arxiv.org/abs/1806.05569)

Tags: task.cardiac_motion_scoring, domain.medical, topic.non_local_neural_networks

- The authors are motivated to create an automated method for motion scoring of the cardiac myocardium; they aim to generate actual motion scores (normal, hpyokinetic, akinetic, or dyskinetic), whereas all previous work has simply performed binary classification for whether motion was abnormal or not
- They use a method with two parts, naming it Cardiac-MOS. Since a cardiac motion score is determined by motion patterns within segments but also relative to other segments, they use two CNNS to capture these different kinds of information:
    1. `seg-NL`: This uses a CNN that captures non-local relationships within a cardiac segment
    2. `sub-NL`: This uses a CNN that captures non-local relationships across cardiac segments
- They use two custom / novel layers in their network:
    1. `NL` (non-local) layers: These compute the response at a given position as a weighted sum of the features at all positions.
    2. kernel-interpolation based convolution layer: this extracts motion information from segment sequences of different lengths and uses interpolation of the kernels to enable it to work on sequences of different lengths. In the paper they simply use bi-linear interpolation.
- They test their method on 90 subjects (5775 images) from multiple vendors and with multiple pathologies present.
    - They achieve a 77.4% accuracy across all the motion scores (34% relative accuracy over the baseline CNN they trained)
    - They achieve a better Kappa for the binary "abnormality prediction" compared to other methods
