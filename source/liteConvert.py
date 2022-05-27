import tensorflow as tf


#load
converter = tf.lite.TFLiteConverter.from_keras_model_file('best_model.h5')

#convert
tflite_model = converter.convert()

#save
open('converted_model.tflite','wb').write(tflite_model)
