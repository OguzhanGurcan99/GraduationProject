import torch
import torch.nn as nn

class WeightedCrossEntropyLoss(nn.Module):
    def __init__(self, weight=None):
        super(WeightedCrossEntropyLoss, self).__init__()
        self.weight = weight

    def forward(self, inputs, targets):
        if self.weight is not None:
            # Apply weights to the cross entropy loss
            return nn.CrossEntropyLoss(weight=self.weight)(inputs, targets)
        else:
            return nn.CrossEntropyLoss()(inputs, targets)
