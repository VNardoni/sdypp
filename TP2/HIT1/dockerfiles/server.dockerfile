FROM python:3.8-slim
WORKDIR /app
RUN pip install Flask
COPY server.py .
EXPOSE 5000
CMD ["python", "server.py"]