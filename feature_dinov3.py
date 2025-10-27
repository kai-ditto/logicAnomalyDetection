from transformers import AutoImageProcessor, AutoModel
import torch
from PIL import Image

image_path = "datasets/juice_bottle/juice_bottle/train/good/000.png"
image = Image.open(image_path).convert("RGB")
model_name = "facebook/dinov3-vith16plus-pretrain-lvd1689m"
processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModel.from_pretrained(
    model_name, 
    device_map="auto", 
)

inputs = processor(images=image, return_tensors="pt").to(model.device)
with torch.inference_mode():
    outputs = model(**inputs)
    
features = outputs.last_hidden_state
print("Features shape:", features.shape)
pooled_output = outputs.pooler_output
print("Pooled output shape:", pooled_output.shape)