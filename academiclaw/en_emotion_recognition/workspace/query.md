### [Query Image Classification - Facial Emotion Recognition]
You will be provided with a baseline TensorFlow/Keras implementation for a 5-class facial emotion recognition task using the samithsachidanandan/human-face-emotions Kaggle dataset. The current model is a simple CNN with three convolutional layers, dropout, and a small fully connected layer, trained on 128x128 RGB images with early stopping based on validation loss.

Your goal is to redesign and improve the training pipeline and/or model architecture to significantly enhance validation performance, focusing on model quality and generalization capability.

**Implementation Requirements:**
1. Create a Python script named `train_improved_model.py`
2. The script must train the model and save two files:
   - `emotion_model.h5`: The final trained Keras model
   - `metrics.json`: A JSON file containing the following keys:
     {
       "val_acc": float (validation accuracy, e.g., 0.8955),
       "train_acc": float (training accuracy, e.g., 0.9200),
       "macro_f1": float (macro-average F1 score, e.g., 0.8800),
       "per_class_f1": list (per-class F1 scores, e.g., [0.85, 0.90, 0.88, 0.82, 0.91])
     }

**Training Requirements:**
1. Use the same data loading protocol:
   - Image size: 128x128 RGB
   - Validation split: 0.2 (20% validation)
   - Seed: 281 (for reproducibility)
   - Batch size: 64 (recommended)
   - Label mode: 'categorical'

2. Dataset directory structure:
   - Load from kagglehub: `kagglehub.dataset_download('samithsachidanandan/human-face-emotions')`
   - Or use the provided local path
   - Dataset contains 5 emotion classes

**Improvement Strategies (choose one or more):**
1. **Transfer Learning**: Use a pretrained backbone (MobileNetV2, EfficientNetB0, ResNet50V2)
2. **Data Augmentation**: RandomFlip, RandomRotation, RandomZoom, RandomContrast
3. **Advanced Architecture**: Deeper CNN, residual connections, attention mechanisms
4. **Regularization**: Dropout, L2 regularization, batch normalization
5. **Optimization**: Learning rate scheduling, tuned Adam parameters
6. **Callbacks**: EarlyStopping, ReduceLROnPlateau, ModelCheckpoint


### [Context]
- 0-8955-human-face-emotions-with-simple-conv2d.ipynb (baseline implementation)
- Dataset: samithsachidanandan/human-face-emotions (via Kaggle)
