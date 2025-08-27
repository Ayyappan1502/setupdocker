FROM python:3.12.4-alpine3.20



RUN apk add --no-cache curl

WORKDIR /app

# first copy the dependencies only


# Upgrade pip & setuptools
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip install  -r requirements.txt

# Install the dependencies 


# now copy the app code
# build time by using the cache if no new dependencies are added
# 
COPY app.py .

CMD ["python","0.0.0.0:8080","app:app"]