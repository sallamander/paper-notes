# [On the Automatic Generation of Medical Imaging Reports](https://arxiv.org/abs/1711.08195)

Date: 11/22/2017
Tags: task.image_captioning, domain.medical, topic.soft_attention

- The authors are motivated to provide automated generation of medical imaging reports to alleviate errors that may arise during report-writing, as well as alleviate the large amounts of time that physicians may spend writing reports
- The authors propose a multi-task framework that performs tag prediction (for medical text indicator tags) and paragraph generation (of report *impressions* and *findings*); their system is trained end to end and consists of multiple parts:
    - They use a CNN that takes as input an image and performs multi-label classification to predict MTI (medical text indicator) tags
        - The feature maps from the last convolutional layer of the CNN serve as "visual features" for a co-attention network
        - The predicted tags are then turned into word-embeddings that serve as "semantic features" for a co-attention network
    - They use a co-attention network that takes in the visual and semantic features and produces soft visual and semantic attention vectors; they combine these via concatenation
    - They use a hierarchical LSTM to generate paragraphs. It consists of:
        - A sentence LSTM that takes in the concatenated context vectors and generates topic vectors and a stop control (i.e. when to stop generating topics with the sentence LSTM, and words with the word LSTM).
        - A word LSTM that takes in the topic vector and produces words for sentences.
- The loss function used is a weighted combination of:
    - Cross-entropy loss for the multi-label classification of tags
    - Cross-entropy loss for the stop / continue prediction of the LSTM
    - Cross-entropy for the word predictions of the word LSTM
- They test their method using two publicly available sets: IU X-Ray and PIER (pathology) against a number of prior image captioning baselines. They perform better on both datasets compared to all baselines for BLEU-1, BLEU-2, BLEU-3, BLEU-4, METEOR, ROUGE, and CIDER scores
    - They see that their approach produces paragraphs that are noticeably longer than the ground truth (which is not true relative to other approaches)
    - In ablation studies with models that use only the semantic features for the attention mechanism or only the visual features, they find that these models perform worse than the co-attention model
