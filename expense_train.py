import tensorflow
from src import config
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Flatten,Dense,Dropout,Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from imutils import paths
import numpy as np
import picle
from cv2 import cv2
import os

#load the contents of annotated csv file
print("[INFO] loading dataset ..")
data = []
labels = []
targets = []
imagePaths = []

#for csvPath in paths.list_files(config.ANNOTS_PATH,validExts=(".csv")):
    #rows = open(csvPath).read().strip().split("\n")

rows = open(config.EXPENSE_TABLE_ANNOTS_PATH).read().strip().strip("\n")

k=0
	for row in rows:
		# break the row into the filename, bounding box coordinates,
		# and class label
		row = row.split(",")
		(filename, startX, startY, endX, endY, label) = row
        # derive the path to the input image, load the image (in OpenCV
        # format), and grab its dimensions
        imagePath = os.path.sep.join([config.IMAGES_PATH,label,filename])
        print("imagepath",imagepath)
        image = cv2.imread(imagePath)
        k = k+1
        print("FOUND AND READ IMAGE: ",imagepath,"with k:",k)
        crop_image = image[int(startY): int(endY),int(startX): int(endX)]
        
        (h, w) = image.shape[:2]
        # scale the bounding box coordinates relative to the spatial dimensions of the input image
        startX = float(startX) / w
        startY = float(startY) / h
        endX = float(endX) / w
        endY = float(endY) / h
        
		# load the image and preprocess it
		image = load_img(imagePath, target_size=(224, 224))
		image = img_to_array(image)
		# update our list of data, class labels, bounding boxes, and
		# image paths
		data.append(image)
		labels.append(label)
		bboxes.append((startX, startY, endX, endY))
		imagePaths.append(imagePath)
        
# convert the data, class labels, bounding boxes, and image paths to
# NumPy arrays, scaling the input pixel intensities from the range
# [0, 255] to [0, 1]
data = np.array(data, dtype="float32") / 255.0
labels = np.array(labels)
bboxes = np.array(bboxes, dtype="float32")
imagePaths = np.array(imagePaths)
# perform one-hot encoding on the labels
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
# only there are only two labels in the dataset, then we need to use
# Keras/TensorFlow's utility function as well
if len(lb.classes_) == 2:
	labels = to_categorical(labels)
    
# partition the data into training and testing splits using 80% of
# the data for training and the remaining 20% for testing
split = train_test_split(data, labels, bboxes, imagePaths,test_size=0.20, random_state=42)

# unpack the data split
(trainImages, testImages) = split[:2]
(trainLabels, testLabels) = split[2:4]
(trainBBoxes, testBBoxes) = split[4:6]
(trainPaths, testPaths) = split[6:]
# write the testing image paths to disk so that we can use then
# when evaluating/testing our object detector
print("[INFO] saving testing image paths...")
f = open(config.TEST_PATHS, "w")
f.write("\n".join(testPaths))
f.close()

# load the VGG16 network, ensuring the head FC layers are left off
vgg = VGG16(weights="imagenet", include_top=False,
	input_tensor=Input(shape=(224, 224, 3)))
# freeze all VGG layers so they will *not* be updated during the
# training process
vgg.trainable = False
# flatten the max-pooling output of VGG
flatten = vgg.output
flatten = Flatten()(flatten)

# construct a fully-connected layer header to output the predicted
# bounding box coordinates
bboxHead = Dense(256, activation="relu")(flatten)
bboxHead = Dropout(0.2)(bboxHead)
bboxHead = Dense(128, activation="relu")(bboxHead)
bboxHead = Dropout(0.2)(bboxHead)
bboxHead = Dense(64, activation="relu")(bboxHead)
bboxHead = Dropout(0.2)(bboxHead)
bboxHead = Dense(32, activation="relu")(bboxHead)
bboxHead = Dropout(0.2)(bboxHead)
bboxHead = Dense(4, activation="sigmoid",name="bounding_box")(bboxHead)
# construct a second fully-connected layer head, this one to predict the class label
#softmaxHead = Dense(512, activation="relu")(flatten)
#softmaxHead = Dropout(0.5)(softmaxHead)
#softmaxHead = Dense(512, activation="relu")(softmaxHead)
#softmaxHead = Dropout(0.5)(softmaxHead)
#softmaxHead = Dense(len(lb.classes_), activation="softmax",name="class_label")(softmaxHead)

# construct the model we will fine tune for bbox regression
model = Model(inputs=vgg.input,outputs=(bboxHead))

losses = {"bounding_box":"mean_squared_error"}

lossWeights = {"bounding_box": 1.0}

# initialize the optimizer, compile the model, and show the model summary
opt = Adam(lr=config.INIT_LR)
model.compile(loss=losses, optimizer=opt, metrics=["accuracy"], loss_weights=lossWeights)
print(model.summary())

# construct a dictionary for our target training outputs
trainTargets = {
	"bounding_box": trainBBoxes
}
# construct a second dictionary, this one for our target testing
# outputs
testTargets = {
	"bounding_box": testBBoxes
}

# train the network for bounding box regression
print("[INFO] training bounding box regression...")
checkpoint_path = "training_4/cp-{epoch:04d}.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
model.save_weights(checkpoint_path.format(epoch=0))

cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path, 
    verbose=1, 
    save_weights_only=True,
    save_freq=25*config.BATCH_SIZE)
    
H = model.fit(
	trainImages, trainTargets,
	validation_data=(testImages, testTargets),
	batch_size=config.BATCH_SIZE,
	epochs=config.NUM_EPOCHS,
    callback= [cp_callback],
	verbose=1)
# serialize the model to disk
print("[INFO] saving object detector model...")
model.save(config.EXPENSE_TABLE_MODEL_PATH)
# serialize the label binarizer to disk
f = open(config.EXPENSE_TABLE_LB_PATH, "wb")
f.write(pickle.dumps(lb))
f.close()
    
# plot the total loss, label loss, and bounding box loss
lossNames = ["loss"]
N = np.arange(0, config.NUM_EPOCHS)
plt.style.use("ggplot")
(fig, ax) = plt.subplots(3, 1, figsize=(13, 13))
# loop over the loss names
for (i, l) in enumerate(lossNames):
	# plot the loss for both the training and validation data
	title = "Loss for {}".format(l) if l != "loss" else "Total loss"
	ax[i].set_title(title)
	ax[i].set_xlabel("Epoch #")
	ax[i].set_ylabel("Loss")
	ax[i].plot(N, H.history[l], label=l)
	ax[i].plot(N, H.history["val_" + l], label="val_" + l)
	ax[i].legend()
# save the losses figure and create a new figure for the accuracies
plt.tight_layout()
plotPath = os.path.sep.join([config.BASE_OUTPUT, "losses.png"])
plt.savefig(plotPath)
plt.close()

N = config.NUM_EPOCHS

plotPath = os.path.sep.join([config.BASE_OUTPUT, "acc.png"])
plt.savefig(plotPath)

plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.title("Bounding box regression loss on training set")
plt.xlabel("Epoch #")
plt.ylabel("Loss")
plt.legend(loc="lower left")
plt.savefig(config.PLOT_PATH)

        