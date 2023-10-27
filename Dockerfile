FROM python:3.10

LABEL maintainer "Triumph"

COPY ../ /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ARG OPENAI_API_KEY
ARG KAY_API_KEY

ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV KAY_API_KEY=$KAY_API_KEY

CMD ["streamlit", "run", "app.py"]