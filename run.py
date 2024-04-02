import torch


mask = torch.randint(0, 4, (4, 4), dtype=torch.long)

targets = torch.randint(0, 10, (16, 64, 64))

print(targets.shape)

import torch
import torch.nn.functional as F

# Example output from the U-Net model (shape: 8, 64, 64)
output = torch.randn(8, 64, 64)

# Apply softmax along the channel dimension to convert logits to probabilities
output_probs = F.softmax(output, dim=0)

# Get the predicted class for each pixel by taking the argmax along the channel dimension
predicted_class_map = torch.argmax(output_probs, dim=0)
print(predicted_class_map)
