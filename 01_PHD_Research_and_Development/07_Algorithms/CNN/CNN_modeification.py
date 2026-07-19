import tensorflow as tf
from tensorflow.keras import layers, Model
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix



class Config:

    IMG_SIZE = 512
    BATCH_SIZE = 32
    EPOCHS = 50
    NUM_CLASSES = 10

    TRAIN_CSV = "train.csv"
    VAL_CSV = "validation.csv"
    TEST_CSV = "test.csv"



class InsectDataLoader:

    def __init__(self, config):
        self.config = config



    def load_csv(self):

        train_df = pd.read_csv(self.config.TRAIN_CSV)
        val_df = pd.read_csv(self.config.VAL_CSV)
        test_df = pd.read_csv(self.config.TEST_CSV)
        return train_df, val_df, test_df

    def preprocess_image(self, path, label):

        image = tf.io.read_file(path)
        image = tf.image.decode_jpeg(image, channels=3)
        image = tf.image.resize(image,(self.config.IMG_SIZE, self.config.IMG_SIZE))
        image = image / 255.0
        return image, label


    def create_dataset(self, dataframe):

        paths = dataframe["image_path"].values
        labels = dataframe["label"].values
        dataset = tf.data.Dataset.from_tensor_slices((paths, labels))
        dataset = dataset.map(self.preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
        dataset = dataset.shuffle(1000)

        dataset = dataset.batch(self.config.BATCH_SIZE)
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        return dataset

    def get_data(self):

        train_df,val_df,test_df = self.load_csv()
        train_ds=self.create_dataset(train_df)
        val_ds=self.create_dataset(val_df)
        test_ds=self.create_dataset(test_df)
        return train_ds,val_ds,test_ds


# =====================================================
# HEUN INITIALIZER CLASS
# =====================================================

class HeunInitializer(tf.keras.initializers.Initializer):

    def __init__(self, alpha=0.1):
        self.alpha=alpha

    def __call__(self, shape, dtype=None):

        fan_in = shape[0]*shape[1]*shape[2]
        std=np.sqrt(2.0/fan_in)
        weight=tf.random.normal(shape, mean=0, stddev=std, dtype=dtype)
        weight = weight + (self.alpha * tf.sin(weight))
        return weight

# =====================================================
# LOGLOG ACTIVATION CLASS
# =====================================================
class LogLogActivation(layers.Layer):

    def __init__(self):
        super().__init__()

    def call(self,x):
        return tf.math.log(1 + tf.math.log(1 + tf.exp(x)))

# =====================================================
# CLLHNN MODEL CLASS
# =====================================================

class CLLHNN(Model):
    def __init__(self, config):

        super().__init__()
        self.conv1 = layers.Conv2D(32, (3,3), padding="same", kernel_initializer= HeunInitializer())
        self.act1 = LogLogActivation()
        self.pool1 = layers.MaxPooling2D()
        self.conv2 = layers.Conv2D(64, (3,3),padding="same",kernel_initializer=HeunInitializer())
        self.act2 = LogLogActivation()
        self.pool2 = layers.MaxPooling2D()
        self.conv3 = layers.Conv2D(128, (3,3), padding="same", kernel_initializer= HeunInitializer())
        self.act3 = LogLogActivation()
        self.gap = layers.GlobalAveragePooling2D()
        self.fc1 = layers.Dense(256, kernel_initializer= HeunInitializer())
        self.act4 = LogLogActivation()
        self.output_layer = layers.Dense(config.NUM_CLASSES, activation="softmax")

    def call(self,x):
        x=self.conv1(x)
        x=self.act1(x)
        x=self.pool1(x)
        x=self.conv2(x)
        x=self.act2(x)
        x=self.pool2(x)
        x=self.conv3(x)
        x=self.act3(x)
        x=self.gap(x)
        x=self.fc1(x)
        x=self.act4(x)
        x=self.output_layer(x)
        return x

# =====================================================
# TRAINER CLASS
# =====================================================

class Trainer:

    def __init__(self, model, config):
        self.model=model
        self.config=config

    def compile_model(self):
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),loss="sparse_categorical_crossentropy", metrics=["accuracy"])


    def train(self, train_ds, val_ds):
        history=self.model.fit(train_ds,validation_data=val_ds, epochs=self.config.EPOCHS)
        return history

    def evaluate(self,test_ds):
        result=self.model.evaluate(test_ds)
        print("Test Accuracy:",result[1])

# =====================================================
# MAIN PROGRAM
# =====================================================

config=Config()

# Data
data_loader=InsectDataLoader(config)
train_ds,val_ds,test_ds = data_loader.get_data()

# Model
model=CLLHNN(config)

# Build model
model.build((None, config.IMG_SIZE, config.IMG_SIZE, 3))
model.summary()

# Training
trainer=Trainer( model,config)
trainer.compile_model()
trainer.train(train_ds,val_ds)

# Testing
trainer.evaluate(test_ds)

# Save model
model.save("CLLHNN_insect.keras")