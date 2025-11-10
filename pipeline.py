import torch
import dotenv
import json

from google import genai
from PIL import Image
from transformers import AutoProcessor, AutoModel
from memory import MemoryBank
from schema import (
    JuiceBottle
)

dotenv.load_dotenv() 

class AnomalyDetection:
    def __init__(self, device='cuda:0', verbose=False):
        """
        Initialize the AnomalyDetection pipeline.

        Args:
            model_name (str): The name of the vision-language model to use.
        """
        self.device = device
        self.verbose = verbose
        self.memory_bank = None
        self.models = self.load_models(device)

    def load_models(self, device='cuda:0'):
        """
        Load the vision-language models.
        Args:
            device (str): The device to load the models onto.

        Returns:
            The loaded models.
        """
        models = {}

        gemini_path = "gemini-2.5-flash"
        siglip2_path = "google/siglip2-base-patch16-512"
        dinov3_path = "facebook/dinov3-vith16plus-pretrain-lvd1689m"

        gemini_client = genai.Client()  

        siglip2_model = AutoModel.from_pretrained(
            siglip2_path, 
            dtype=torch.float16, 
            device_map="auto"
        )
        siglip2_processor = AutoProcessor.from_pretrained(
            siglip2_path
        )

        # dinov3_model = AutoModel.from_pretrained(
        #     dinov3_path, 
        #     device_map="auto"
        # )
        # dinov3_processor = AutoProcessor.from_pretrained(
        #     dinov3_path
        # )

        models['gemini'] = {
            'client': gemini_client,
            'model_path': gemini_path
        }
        models['siglip2'] = {
            'model': siglip2_model.to(device),
            'processor': siglip2_processor
        }
        # models['dinov3'] = {
        #     'model': dinov3_model.to(device),
        #     'processor': dinov3_processor
        # }
        if self.verbose:
            print(f"All models({list(models.keys())}) loaded.")
            print(f"Device: {device}")
                

        return models

    def _raw_text(self, image):
        """
        Generate raw text description for the given image using Gemini model.

        Args:
            image: The input image.
        Returns:
            The generated raw text description.
        """

        gemini_client = self.models['gemini']['client']
        model_path = self.models['gemini']['model_path']
        prompt_text = "이 이미지에 대해 최대한 상세하게 설명해 주세요."

        contents = [prompt_text, image]
        raw_text = ""
        # response = gemini_client.models.generate_content_stream(
        #     model=model_path,
        #     contents=contents,
        # )
        # for chunk in response:
        #     print(chunk.text, end='', flush=True)
        #     raw_text += chunk.text
        # print()
        response = gemini_client.models.generate_content(
            model=model_path,
            contents=contents,
        )
        raw_text = response.text

        return raw_text
    
    def _fmt_text(self, raw_text, image, format_schema=None):
        """
        Format the raw text description using gemini model.

        Args:
            raw_text: The raw text description.
            image: The input image.

        Returns:
            The formatted text description.
        """
        gemini_client = self.models['gemini']['client']
        model_path = self.models['gemini']['model_path']
        prompt_text = f"다음은 이미지에 대한 설명입니다: {raw_text}\n이 설명을 바탕으로 이미지의 주요 특징을 간결하고 명확하게 요약해 주세요."

        contents = [prompt_text, image]

        response = gemini_client.models.generate_content(
            model=model_path,
            contents=contents,
            config=genai.types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=format_schema,
            )
        )
        return json.loads(response.text)

    def build_memory_bank(self, images, texts, bank_id='default_bank'):
        """
        Build a memory bank from the provided images and texts.

        Args:
            images: The images to build the memory bank from.
            texts: The texts to build the memory bank from.
            bank_id (str): Identifier for the memory bank.
        """
        pass

    def infer(self, image, format_schema=None):
        """
        Perform inference on the provided image using the memory bank.

        Args:
            image: The input image for inference.

        Returns:
            The inference results.
        """
        if self.memory_bank is None:
            # raise ValueError("Memory bank is not created. Please create it before inference.")
            pass

        raw_text = self._raw_text(image)
        if self.verbose:
            print("Raw text:", raw_text)
        formatted_text = self._fmt_text(raw_text, image, format_schema=format_schema)
        if self.verbose:
            print("Formatted text:", formatted_text)
        text = format_schema.decode(formatted_text)
        if self.verbose:
            print("Decoded text:", text)
        siglip2_inputs = self.models['siglip2']['processor'](
            text=[text],
            images=image, 
            padding="max_length",  
            max_length=64,
            return_tensors="pt"
        ).to(self.device)
        with torch.no_grad():
            siglip2_outputs = self.models['siglip2']['model'](**siglip2_inputs)
        logits_per_image = siglip2_outputs.logits_per_image
        logits = torch.sigmoid(logits_per_image)
        print("prob : ", logits * 100)
        
        return formatted_text


def main():
    pipeline = AnomalyDetection(device='cuda:0', verbose=True)
    #image_path = "datasets/juice_bottle/juice_bottle/train/good/000.png"
    image_path = "datasets/juice_bottle/juice_bottle/test/logical_anomalies/015.png"
    #image_path = "datasets/juice_bottle/juice_bottle/test/structural_anomalies/021.png"
    image = Image.open(image_path).convert("RGB")
    result = pipeline.infer(image, format_schema=JuiceBottle)

if __name__ == "__main__":
    main()

    