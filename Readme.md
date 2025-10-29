
[MVTec_Loco](https://www.mvtec.com/company/research/datasets/mvtec-loco/downloads)

```
juice bottle example

wget -O juice_bottle.tar.xz "https://www.mydrive.ch/shares/48239/3ad28d48636eada48f0caded666a804a/download/430647100-1646843074/juice_bottle.tar.xz"

mkdir datasets/juice_bottle
tar -xJf juice_bottle.tar.xz -C datasets/juice_bottle
```

```
cp .env.example .env

# .env 파일 내용 예시:
GEMINI_API_KEY=your_gemini_api_key_here
```