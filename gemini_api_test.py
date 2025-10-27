import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from pydantic import BaseModel
import dotenv

dotenv.load_dotenv() # .env 파일에서 GENAI_API_KEY 로드
client = genai.Client()

image_path = "datasets/juice_bottle/juice_bottle/train/good/000.png"
prompt_text = "이 이미지에 대해 설명해 주세요."

image = Image.open(image_path)

contents = [prompt_text, image]

print(f"모델 호출 중: 텍스트='{prompt_text}', 이미지='{image_path}'")
# structured output
class Bottle(BaseModel):
    color: str
    image_label: str
    text_label: str
class Recipe(BaseModel):
    recipe_name: str
    description: str
    ingredients: list[str]
    steps: list[str]
try:
    # 스트리밍 응답
    response = client.models.generate_content_stream(
        model='gemini-2.5-flash',
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=Bottle,
        ) # 구조화된 출력 설정
    )
    for chunk in response:
        print(chunk.text, end='', flush=True)


    # # 단일 응답
    # response = client.models.generate_content(
    #     model='gemini-2.5-flash',
    #     contents=contents,
    # )
    # print("-" * 30)
    # print("(Output):")
    # print(response.text)
    # print("-" * 30)
except Exception as e:
    print(f"API 호출 중 오류 발생: {e}")