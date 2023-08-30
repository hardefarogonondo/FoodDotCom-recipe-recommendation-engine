FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./src/back_end /app
COPY ./models /app/models
COPY ./data/processed/train.pkl /app/data/processed/train.pkl
COPY ./data/processed/test.pkl /app/data/processed/test.pkl
COPY ./data/processed/train_sparse_matrix.pkl /app/data/processed/train_sparse_matrix.pkl
COPY ./data/processed/user_mapping.pkl /app/data/processed/user_mapping.pkl
COPY ./data/processed/recipe_mapping.pkl /app/data/processed/recipe_mapping.pkl

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]