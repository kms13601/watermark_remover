from tensorflow.keras import layers
import tensorflow as tf
from tensorflow import keras

def get_norm_layer(norm_type='instance'):
    if norm_type == 'batch':
        return layers.BatchNormalization
    elif norm_type == 'instance':
        return layers.LayerNormalization
    elif norm_type == 'none':
        return lambda: layers.Layer()
    else:
        raise NotImplementedError(f'normalization layer [{norm_type}] is not found')

def resnet_block(dim, norm_layer, use_dropout=False, padding_type='reflect'):
    def block(x):
        # Padding
        if padding_type == 'reflect':
            x = tf.pad(x, [[0,0], [1,1], [1,1], [0,0]], mode='REFLECT')
        elif padding_type == 'replicate':
            x = tf.pad(x, [[0,0], [1,1], [1,1], [0,0]], mode='SYMMETRIC')
        elif padding_type == 'zero':
            x = layers.ZeroPadding2D(padding=1)(x)
        
        # First conv layer with SAME padding
        conv1 = layers.Conv2D(dim, 3, padding='same', use_bias=True)(x)
        norm1 = norm_layer()(conv1)
        relu1 = layers.ReLU()(norm1)
        
        # Dropout if specified
        if use_dropout:
            relu1 = layers.Dropout(0.5)(relu1)
        
        # Second conv layer with SAME padding
        conv2 = layers.Conv2D(dim, 3, padding='same', use_bias=True)(relu1)
        norm2 = norm_layer()(conv2)
        
        # Skip connection
        return layers.Add()([x, norm2])
    
    return block

def build_generator(input_shape=(256, 256, 3), output_shape=(256, 256, 3), 
                    ngf=64, n_blocks=6, norm='batch', use_dropout=False):
    norm_layer = get_norm_layer(norm)
    
    inputs = layers.Input(shape=input_shape)
    
    x = layers.Lambda(lambda x: tf.pad(x, [[0,0], [3,3], [3,3], [0,0]], mode='REFLECT'))(inputs)
    x = layers.Conv2D(ngf, 7, padding='valid', use_bias=True)(x)
    x = norm_layer()(x)
    x = layers.ReLU()(x)
    
    mult = 1
    for _ in range(2):
        mult *= 2
        x = layers.Conv2D(ngf * mult, 3, strides=2, padding='same', use_bias=True)(x)
        x = norm_layer()(x)
        x = layers.ReLU()(x)
    
    for _ in range(n_blocks):
        x = resnet_block(ngf * mult, norm_layer, use_dropout)(x)
    
    for _ in range(2):
        mult //= 2
        x = layers.Conv2DTranspose(ngf * mult, 3, strides=2, padding='same', use_bias=True)(x)
        x = norm_layer()(x)
        x = layers.ReLU()(x)
    
    # Ensure the shape matches the expected output shape
    x = layers.Conv2D(output_shape[-1], 3, padding='same')(x)
    x = layers.Lambda(lambda x: tf.image.resize(x, output_shape[:2], method='bilinear'))(x)
    outputs = layers.Activation('tanh')(x)
    
    return keras.Model(inputs=inputs, outputs=outputs, name='ResNetGenerator')

def build_discriminator(input_shape=(256, 256, 3), ndf=64, n_layers=3, norm='batch'):
    norm_layer = get_norm_layer(norm)
    
    inputs = layers.Input(shape=input_shape)
    
    # First layer
    x = layers.Conv2D(ndf, 4, strides=2, padding='same')(inputs)
    x = layers.LeakyReLU(0.2)(x)
    
    # Subsequent layers
    nf_mult = 1
    for n in range(1, n_layers):
        nf_mult_prev = nf_mult
        nf_mult = min(2 ** n, 8)
        
        x = layers.Conv2D(ndf * nf_mult, 4, strides=2, padding='same', use_bias=True)(x)
        x = norm_layer()(x)
        x = layers.LeakyReLU(0.2)(x)
    
    # Penultimate layer
    nf_mult_prev = nf_mult
    nf_mult = min(2 ** n_layers, 8)
    
    x = layers.Conv2D(ndf * nf_mult, 4, strides=1, padding='same', use_bias=True)(x)
    x = norm_layer()(x)
    x = layers.LeakyReLU(0.2)(x)
    
    # Final classification layer
    outputs = layers.Conv2D(1, 4, strides=1, padding='same')(x)
    
    return keras.Model(inputs=inputs, outputs=outputs, name='PatchGANDiscriminator')
