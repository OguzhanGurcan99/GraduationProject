from unet_code import config
import matplotlib.pyplot as plt
import numpy as np
import torch
import cv2
import os

def prepare_plot(origImage, origMask, predMask, ct, filename):
    figure, ax = plt.subplots(nrows=1, ncols=3, figsize=(10, 10))
    ax[0].imshow(origImage)
    ax[1].imshow(origMask)
    ax[2].imshow(predMask)
    ax[0].set_title("Image")
    ax[1].set_title("Original Mask")
    ax[2].set_title("Predicted Mask")
    figure.suptitle(filename)
    figure.tight_layout()
    figure.savefig(str(ct)+'_foo.png')
    #figure.show()


def make_predictions(model, imagePath, ct):
    model.eval()
    with torch.no_grad():
        numpy_array = np.load(imagePath)
        image = torch.tensor(numpy_array, dtype=torch.float32)
        filename = imagePath.split(os.path.sep)[-1].replace("npy", "png")
        groundTruthPath = os.path.join(config.MASK_DATASET_PATH, filename)
        gtMask = cv2.imread(groundTruthPath, 0)
        gtMask = torch.tensor(gtMask, dtype=torch.float32)
        image = image.unsqueeze(0)
        predMask = model(image)
        predMask = predMask.squeeze()
        output_probs = torch.sigmoid(predMask)
        output_probs_np = output_probs.cpu().numpy()
        output_probs_np = (output_probs_np > config.THRESHOLD) * 255
        output_probs_np = output_probs_np.astype(np.uint8)
        ones_array = np.ones((64, 64, 3))
        prepare_plot(ones_array, gtMask, output_probs_np, ct, filename)



imagePaths = open(config.TEST_PATHS).read().strip().split("\n")
imagePaths = np.random.choice(imagePaths, size=10)

unet = torch.load(config.MODEL_PATH).to(config.DEVICE)

ct=0
for path in imagePaths:
    make_predictions(unet, path, ct)
    ct+=1
