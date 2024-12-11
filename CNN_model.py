from tensorflow.keras import models, layers
import tensorflow as tf

class CNN1(models.Model):
    def __init__(self, in_channels=3, out_channels=3):
        super(CNN1, self).__init__()

        # Encoder layers
        self.encoder1 = self._block(in_channels, 64)
        self.encoder2 = self._block(64, 128)
        self.encoder3 = self._block(128, 256)
        
        # Decoder layers
        self.decoder = models.Sequential([
            layers.Conv2D(128, kernel_size=3, padding='same', activation='relu'),
            layers.Conv2D(64, kernel_size=3, padding='same', activation='relu'),
            layers.Conv2D(out_channels, kernel_size=3, padding='same')
        ])
    
    def _block(self, in_channels, out_channels):
        return models.Sequential([
            layers.Conv2D(out_channels, kernel_size=3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.ReLU()
        ])

    def call(self, inputs):
        x1 = self.encoder1(inputs)
        x2 = self.encoder2(x1)
        x3 = self.encoder3(x2)
        
        out = self.decoder(x3)
        return out

class CNN2(models.Model):
    def __init__(self):
        super(CNN2, self).__init__()
        self.c_layer = self._build_c_layer()
        self.conv_layer = self._build_conv_layer()

    def _build_wavelet_layer(self):
        return layers.Conv2D(64, kernel_size=3, padding='same', input_shape=(None, None, 3))

    def _build_conv_layer(self):
        return models.Sequential([
            layers.Conv2D(128, kernel_size=3, padding='same'),
            layers.ReLU(),
            layers.Conv2D(3, kernel_size=3, padding='same')
        ])

    def call(self, x):
        x_conv = self.c_layer(x)
        out = self.conv_layer(x_conv)
        return out

class CNN3(models.Model):
    def __init__(self, in_channels=3, out_channels=3):
        super(CNN3, self).__init__()
        
        # U2Net Encoder
        self.encoder1 = self._block(in_channels, 64)
        self.encoder2 = self._block(64, 128)
        self.encoder3 = self._block(128, 256)
        
        # MWCNN Wavelet layer
        self.c_layer = self._build_c_layer()
        
        # Decoder to reconstruct the output
        self.decoder = models.Sequential([
            layers.Conv2D(128, kernel_size=3, padding='same', activation='relu'),
            layers.Conv2D(64, kernel_size=3, padding='same', activation='relu'),
            layers.Conv2D(out_channels, kernel_size=3, padding='same', activation='sigmoid')  # Output in [0, 1]
        ])
        
    def _block(self, in_channels, out_channels):
        """Define a simple convolutional block."""
        return models.Sequential([
            layers.Conv2D(out_channels, kernel_size=3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.ReLU()
        ])
    
    def _build_c_layer(self):
        return layers.Conv2D(64, kernel_size=3, padding='same', activation='relu')
    
    def call(self, inputs):
        # Encoder
        x1 = self.encoder1(inputs)
        x2 = self.encoder2(x1)
        x3 = self.encoder3(x2)
        
        # Wavelet feature extraction
        c_features = self.c_layer(x3)
        
        # Decoder to reconstruct the final output
        out = self.decoder(wavelet_features)
        
        # Ensure the output size matches (None, 256, 256, 3)
        if out.shape[1:3] != (256, 256):
            out = tf.image.resize(out, (256, 256))  # Resize to target shape
        return out
