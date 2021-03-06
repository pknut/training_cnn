from PIL import Image
from keras.callbacks import Callback
from deepsense import neptune

ctx = neptune.Context()


def array_2d_to_image(array, autorescale=True):
    assert array.min() >= 0
    assert len(array.shape) in [2, 3]
    if array.max() <= 1 and autorescale:
        array = 255 * array
    array = array.astype('uint8')
    return Image.fromarray(array)


class NeptuneCallback(Callback):
    def __init__(self, x_test, y_test):
        self.epoch_id = 0
        self.x_test = x_test
        self.y_test = y_test

    def on_epoch_end(self, epoch, logs={}):

        self.epoch_id += 1

        ctx.channel_send('Log-loss training', self.epoch_id, logs['loss'])
        ctx.channel_send('Log-loss validation', self.epoch_id, logs['val_loss'])
        ctx.channel_send('Accuracy training', self.epoch_id, logs['acc'])
        ctx.channel_send('Accuracy validation', self.epoch_id, logs['val_acc'])



        # # image
        # validation_predictions = self.model.predict_classes(self.x_test)
        # scores = self.model.predict(self.x_test)
        #
        # image_per_epoch = 0
        # for index, (prediction, actual) in enumerate(zip(validation_predictions, self.y_test.argmax(axis=1))):
        #     if prediction != actual:
        #         if image_per_epoch == self.images_per_epoch:
        #             break
        #         image_per_epoch += 1
        #
        # ctx.channel_send('false_predictions', neptune.Image(
        #     name=str(self.epoch_id),
        #     data=array_2d_to_image(self.x_test[index, :, :])))
