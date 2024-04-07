FROM python:3.8-slim
WORKDIR /app
RUN pip install Flask
COPY tarea_remota.py .
EXPOSE 5001
CMD ["python", "tarea_remota.py"]