from tensorflow.python.keras import Input
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.python.keras.models import Model


INPUT_SHAPE = (480, 640, 3)
INITIAL_FILTER_SIZE = 64


def build_autoencoder():
    encoder = Input(shape=INPUT_SHAPE)
    x = Conv2D(filters=INITIAL_FILTER_SIZE, kernel_size=(3, 3), activation="elu", padding="same")(encoder)
    x = MaxPooling2D(pool_size=(2, 2), padding="same")(x)
    x = Conv2D(filters=INITIAL_FILTER_SIZE // 2, kernel_size=(3, 3), activation="elu", padding="same")(x)
    x = MaxPooling2D(pool_size=(2, 2), padding="same")(x)
    x = Conv2D(filters=INITIAL_FILTER_SIZE // 4, kernel_size=(3, 3), activation="elu", padding="same")(x)
    encoded = MaxPooling2D(pool_size=(2, 2), padding="same")(x)

    decoder = Conv2D(filters=INITIAL_FILTER_SIZE // 4, kernel_size=(3, 3), activation="elu", padding="same")(encoded)
    x = UpSampling2D((2, 2))(decoder)
    x = Conv2D(filters=INITIAL_FILTER_SIZE // 2, kernel_size=(3, 3), activation="elu", padding="same")(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(filters=INITIAL_FILTER_SIZE, kernel_size=(3, 3), activation="elu", padding="same")(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(filters=INPUT_SHAPE[-1], kernel_size=(3, 3), activation="sigmoid", padding="same")(x)

    model = Model(encoder, decoded)
    model.compile(optimizer="adam", loss="binary_crossentropy")
    model.summary()
    return model


def build_convolutional():
    input_layer = Input(shape=INPUT_SHAPE)
    x = Conv2D(filters=INITIAL_FILTER_SIZE, kernel_size=(3, 3), activation="elu", padding="same")(input_layer)
    x = MaxPooling2D(pool_size=(2, 2), padding="same")(x)
    x = Conv2D(filters=INITIAL_FILTER_SIZE, kernel_size=(3, 3), activation="elu", padding="same")(x)
    x = UpSampling2D((2, 2))(x)
    output_layer = Conv2D(filters=INPUT_SHAPE[-1], kernel_size=(3, 3), activation="sigmoid", padding="same")(x)

    model = Model(input_layer, output_layer)
    model.compile(optimizer="adam", loss="binary_crossentropy")
    model.summary()
    return model
