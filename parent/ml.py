from tensorflow import keras
import numpy as np

class MLModel():

	def generateSingle(scores):
		model = keras.models.load_model('parent/model.h5')

		careers={
		    0:'IT',
		    1:'Writing and Content Creation',
		    2:'Design and Architecture',
		    3:'Administrative functions',
		    4:'Education',
		    5:'Business'
		}

		if len(scores) == 23:
			pred = model.predict([scores])
			order = np.argsort(pred[0])
			options=[careers.get(order[4]), careers.get(order[3]), careers.get(order[2])]
			return options

		else:
			return False;
