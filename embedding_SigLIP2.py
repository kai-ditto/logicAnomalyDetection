import torch
import requests
from PIL import Image
from transformers import AutoProcessor, AutoModel

model = AutoModel.from_pretrained("google/siglip2-base-patch16-512", dtype=torch.float16, device_map="auto")
processor = AutoProcessor.from_pretrained("google/siglip2-base-patch16-512")

image_path = "datasets/juice_bottle/juice_bottle/train/good/000.png"
image = Image.open(image_path).convert("RGB")
candidate_labels = ["yellow orange juice bottle", "red apple juice bottle", "green vegetable juice bottle"]

# follows the pipeline prompt template to get same results
texts = [f'This is a photo of {label}.' for label in candidate_labels]

# IMPORTANT: we pass `padding=max_length` and `max_length=64` since the model was trained with this
inputs = processor(
    text=texts, 
    images=image, 
    padding="max_length", 
    max_length=64,
    return_tensors="pt"
).to(model.device)

with torch.no_grad():
    outputs = model(**inputs)

logits_per_image = outputs.logits_per_image
probs = torch.sigmoid(logits_per_image)
for i, label in enumerate(candidate_labels):
    print(f"{probs[0][i]:.1%} that image 0 is '{label}'")