FROM python:3.10-slim

WORKDIR /app

# Copiar código
COPY . .

# Instalar dependencias del sistema (opcional pero útil para PyMySQL y cryptography)
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libssl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Exponer puerto Flask
EXPOSE 5000

# Comando para esperar DB y lanzar app
CMD ["sh", "-c", "python wait_for_db.py && python init_db.py && python app.py"]
