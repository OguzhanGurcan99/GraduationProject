from torch.utils.data import Dataset
import cv2
import numpy as np
from configuration import class_map

class SegmentationDataset(Dataset):
    def __init__(self, imagePaths, maskPaths, transforms):
        # store the image and mask filepaths, and augmentation
        # transforms
        self.imagePaths = imagePaths
        self.maskPaths = maskPaths
        self.transforms = transforms

    def __len__(self):
        # return the number of total samples contained in the dataset
        return len(self.imagePaths)

    def __getitem__(self, idx):
        # grab the image path from the current index
        imagePath = self.imagePaths[idx]
        # load the image from disk, swap its channels from BGR to RGB,
        # and read the associated mask from disk in grayscale mode
        image = cv2.imread(imagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mask = cv2.imread(self.maskPaths[idx], 1)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

        class_label_mask = np.zeros((mask.shape[0], mask.shape[1]), dtype=np.float32) # uint8

        for i in range(mask.shape[0]):
            for j in range(mask.shape[1]):
                pixel_color = tuple(mask[i, j])
                if pixel_color in class_map:
                    class_label_mask[i, j] = class_map[pixel_color]
                else:
                    class_label_mask[i, j] = 255

        # check to see if we are applying any transformations
        if self.transforms is not None:
            # apply the transformations to both image and its mask
            image = self.transforms(image)
            #mask = self.transforms(mask)
        # return a tuple of the image and its mask
        return (image, class_label_mask)
