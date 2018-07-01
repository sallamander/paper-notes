# [Deeply Supervised Nets](https://arxiv.org/abs/1409.5185)

Tags: task.object_classification, topic.deep_supervision

- They are motivated by two different things:
    - Learning more discriminative and robust features in earlier layers, and in particular features that are more transparent (i.e. more easily understood)
    - Trying to alleviate the problem of vanishing / exploding gradients
- They propose adding supervision (a "companion loss") to the hidden layers, naming it "deep supervision"
    - In the paper, they formulate it using SVMs to perform the final classification, and use hinge loss, which means that ultimately it drops out of the total loss once it hits some threshold ($\gamma$)
    - They also formulate the companion losses with weights that they discuss decaying throughout the training process (although they don't discuss what they do in practice)
- They perform experiments on MNIST, CIFAR-10, CIFAR-100, and SVHN, where the baseline is a CNN without the deep supervision:
    - TLDR; they don't really see improved performance on the training set, but achieve SOTA on the test sets (compared to Maxout networks, Network in Network, and Stochastic Pooling). They claim the features learned are more discriminative (and show visuals), but I think this is open to interpretation.
    - MNIST: 25% better test error than baseline CNN, 13% better than next best (Maxout networks)
    - CIFAR-10: 6% better test error than next best (Network in Network)
    - CIFAR-100: 3% better test error than next best (Network in Network)
    - SVHN: 1% better test error than next best (Dropconnect)
