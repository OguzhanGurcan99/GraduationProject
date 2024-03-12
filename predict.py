from unet_code import config
import matplotlib.pyplot as plt
import numpy as np
import torch
import cv2
import os


def prepare_plot(origImage, origMask, predMask, ct):
    figure, ax = plt.subplots(nrows=1, ncols=3, figsize=(10, 10))
    ax[0].imshow(origImage)
    ax[1].imshow(origMask)
    ax[2].imshow(predMask)
    ax[0].set_title("Image")
    ax[1].set_title("Original Mask")
    ax[2].set_title("Predicted Mask")
    figure.tight_layout()
    figure.savefig(str(ct)+'_foo.png')
    #figure.show()


def make_predictions(model, imagePath, ct):
    model.eval()
    with torch.no_grad():
        image = cv2.imread(imagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype("float32") / 255.0
        image = cv2.resize(image, (128, 128))
        orig = image.copy()
        filename = imagePath.split(os.path.sep)[-1]
        groundTruthPath = os.path.join(config.MASK_DATASET_PATH, filename)
        gtMask = cv2.imread(groundTruthPath, 0)
        gtMask = cv2.resize(gtMask, (config.INPUT_IMAGE_HEIGHT,config.INPUT_IMAGE_HEIGHT))
        image = np.transpose(image, (2, 0, 1))
        image = np.expand_dims(image, 0)
        image = torch.from_numpy(image).to(config.DEVICE)
        predMask = model(image).squeeze()
        predMask = torch.sigmoid(predMask)
        predMask = predMask.cpu().numpy()
        predMask = (predMask > config.THRESHOLD) * 255
        predMask = predMask.astype(np.uint8)
        prepare_plot(orig, gtMask, predMask, ct)




imagePaths = open(config.TEST_PATHS).read().strip().split("\n")
imagePaths = np.random.choice(imagePaths, size=10)

unet = torch.load(config.MODEL_PATH).to(config.DEVICE)

ct=0
for path in imagePaths:
    make_predictions(unet, path, ct)
    ct+=1
