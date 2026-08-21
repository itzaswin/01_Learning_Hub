# Learning_Hub

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def tsallis_eswish(x, beta=1.5, q=1.5):
    sigmoid_part = tf.sigmoid(beta * x)
    return x * tf.pow(sigmoid_part, q)

class TsallisESwish(layers.Layer):
    def __init__(self, beta=1.5, q=1.5, **kwargs):
        super(TsallisESwish, self).__init__(**kwargs)
        self.beta = beta
        self.q = q
        
    def call(self, inputs):
        return tsallis_eswish(inputs, self.beta, self.q)
    
    def get_config(self):
        config = super().get_config()
        config.update({'beta': self.beta, 'q': self.q})
        return config

class ConvNeXTBlock(layers.Layer):
    def __init__(self, filters, kernel_size=7, stride=1, expansion=4, 
                 beta=1.5, q=1.5, dropout_rate=0.1, **kwargs):
        super(ConvNeXTBlock, self).__init__(**kwargs)
        
        hidden_dim = filters * expansion
        
        self.dwconv = layers.DepthwiseConv2D(
            kernel_size=kernel_size,
            strides=stride,
            padding='same'
        )
        
        self.ln1 = layers.LayerNormalization(epsilon=1e-6)
        
        self.pwconv1 = layers.Conv2D(hidden_dim, kernel_size=1)
        self.activation = TsallisESwish(beta=beta, q=q)
        self.pwconv2 = layers.Conv2D(filters, kernel_size=1)
        self.dropout = layers.Dropout(dropout_rate)
        self.skip = layers.Add()
        
        self.stride = stride
        self.filters = filters
        
    def call(self, inputs, training=None):
        x = self.dwconv(inputs)
        x = self.ln1(x)
        x = self.pwconv1(x)
        x = self.activation(x)
        x = self.dropout(x, training=training)
        x = self.pwconv2(x)
        x = self.dropout(x, training=training)
        
        if self.stride == 1 and inputs.shape[-1] == self.filters:
            x = self.skip([inputs, x])
            
        return x

class TsallisESwishConvNeXT(Model):
    def __init__(self, input_shape, num_classes, num_blocks=[3, 3, 9, 3], 
                 filters=[96, 192, 384, 768], beta=1.5, q=1.5, dropout_rate=0.1):
        super(TsallisESwishConvNeXT, self).__init__()
        
        self.stem = keras.Sequential([
            layers.Conv2D(filters[0], kernel_size=4, strides=4, padding='same'),
            TsallisESwish(beta=beta, q=q),
            layers.LayerNormalization(epsilon=1e-6)
        ])
        
        self.stages = []
        for stage_idx, (num_blocks, stage_filters) in enumerate(zip(num_blocks, filters)):
            stage_blocks = []
            
            stride = 2 if stage_idx > 0 else 1
            stage_blocks.append(
                ConvNeXTBlock(stage_filters, stride=stride, expansion=4,
                             beta=beta, q=q, dropout_rate=dropout_rate)
            )
            
            for _ in range(1, num_blocks):
                stage_blocks.append(
                    ConvNeXTBlock(stage_filters, stride=1, expansion=4,
                                 beta=beta, q=q, dropout_rate=dropout_rate)
                )
            
            self.stages.append(keras.Sequential(stage_blocks))
        
        self.global_pool = layers.GlobalAveragePooling2D()
        
        self.head = keras.Sequential([
            layers.Dense(512, activation='relu'),
            layers.Dropout(dropout_rate),
            layers.Dense(256, activation='relu'),
            layers.Dropout(dropout_rate),
            layers.Dense(num_classes, activation='softmax')
        ])
        
    def call(self, inputs, training=None):
        x = self.stem(inputs)
        
        for stage in self.stages:
            x = stage(x, training=training)
        
        x = self.global_pool(x)
        x = self.head(x, training=training)
        
        return x

def load_and_preprocess_data(lesion_file, vessel_file, fussy_file, target_file=None):
    lesion_data = pd.read_csv(lesion_file)
    vessel_data = pd.read_csv(vessel_file)
    fussy_data = pd.read_csv(fussy_file)
    
    print(f"Lesion data shape: {lesion_data.shape}")
    print(f"Vessel data shape: {vessel_data.shape}")
    print(f"Fussy data shape: {fussy_data.shape}")
    
    features = pd.concat([lesion_data, vessel_data, fussy_data], axis=1)
    
    if target_file:
        targets = pd.read_csv(target_file)
        return features, targets
    
    return features

def preprocess_data(features, targets=None, test_size=0.2, val_size=0.1):
    X = features.values if hasattr(features, 'values') else features
    y = None
    
    if targets is not None:
        label_encoder = LabelEncoder()
        if isinstance(targets, pd.DataFrame):
            y = label_encoder.fit_transform(targets.iloc[:, 0].values)
        else:
            y = label_encoder.fit_transform(targets)
        
        y = keras.utils.to_categorical(y)
        
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=np.argmax(y, axis=1)
        )
        
        val_size_actual = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=val_size_actual, random_state=42, 
            stratify=np.argmax(y_train, axis=1)
        )
        
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)
        
        return X_train, X_val, y_train, y_val, scaler, label_encoder
    
    return X

def reshape_for_cnn(X):
    num_samples = X.shape[0]
    num_features = X.shape[1]
    
    grid_size = int(np.ceil(np.sqrt(num_features)))
    
    padded_size = grid_size * grid_size
    if num_features < padded_size:
        padding = np.zeros((num_samples, padded_size - num_features))
        X = np.hstack([X, padding])
    
    X_reshaped = X.reshape(num_samples, grid_size, grid_size, 1)
    
    return X_reshaped

def train_model(X_train, X_val, y_train, y_val, input_shape, num_classes,
                epochs=100, batch_size=32, learning_rate=1e-4):
    
    model = TsallisESwishConvNeXT(
        input_shape=input_shape,
        num_classes=num_classes,
        beta=1.5,
        q=1.5,
        dropout_rate=0.1
    )
    
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7)
    ]
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1
    )
    
    return model, history

def evaluate_model(model, X_test, y_test, label_encoder=None):
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)
    
    accuracy = accuracy_score(y_true_classes, y_pred_classes)
    print(f"\nAccuracy: {accuracy * 100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_true_classes, y_pred_classes, 
                               target_names=label_encoder.classes_ if label_encoder else None))
    
    cm = confusion_matrix(y_true_classes, y_pred_classes)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()
    
    return accuracy, y_pred_classes

def plot_training_history(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.plot(history.history['accuracy'], label='Train Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    
    ax2.plot(history.history['loss'], label='Train Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

def generate_synthetic_data(n_samples=1000, n_features=99):
    np.random.seed(42)
    
    lesion_features = np.random.randn(n_samples, n_features // 3)
    vessel_features = np.random.randn(n_samples, n_features // 3)
    fussy_features = np.random.randn(n_samples, n_features // 3)
    
    targets = np.random.randint(0, 3, n_samples)
    
    pd.DataFrame(lesion_features).to_csv('lesion_features.csv', index=False)
    pd.DataFrame(vessel_features).to_csv('vessel_features.csv', index=False)
    pd.DataFrame(fussy_features).to_csv('fussy_features.csv', index=False)
    pd.DataFrame({'target': targets}).to_csv('targets.csv', index=False)
    
    print("Synthetic data generated and saved to CSV files.")

def main():
    generate_synthetic_data(n_samples=1000, n_features=99)
    
    lesion_file = 'lesion_features.csv'
    vessel_file = 'vessel_features.csv'
    fussy_file = 'fussy_features.csv'
    target_file = 'targets.csv'
    
    print("Loading data...")
    features, targets = load_and_preprocess_data(lesion_file, vessel_file, fussy_file, target_file)
    
    X_train, X_val, y_train, y_val, scaler, label_encoder = preprocess_data(
        features, targets, test_size=0.2, val_size=0.1
    )
    
    X_train_reshaped = reshape_for_cnn(X_train)
    X_val_reshaped = reshape_for_cnn(X_val)
    
    input_shape = X_train_reshaped.shape[1:]
    num_classes = y_train.shape[1]
    
    print(f"Input shape: {input_shape}")
    print(f"Number of classes: {num_classes}")
    print(f"Training samples: {X_train_reshaped.shape[0]}")
    print(f"Validation samples: {X_val_reshaped.shape[0]}")
    
    print("\nTraining model...")
    model, history = train_model(
        X_train_reshaped, X_val_reshaped, y_train, y_val,
        input_shape, num_classes,
        epochs=100,
        batch_size=32,
        learning_rate=1e-4
    )
    
    plot_training_history(history)
    
    print("\nEvaluating on validation set:")
    accuracy, _ = evaluate_model(model, X_val_reshaped, y_val, label_encoder)
    
    model.save('tsallis_eswish_convnext_cnn.h5')
    print("\nModel saved as 'tsallis_eswish_convnext_cnn.h5'")
    
    return model, history, accuracy

if __name__ == "__main__":
    model, history, accuracy = main()
