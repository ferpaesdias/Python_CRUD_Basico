FROM python:3.12-slim

# Evitar .pyc e melhorar logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Usuário não-root
RUN useradd -m appuser

WORKDIR /app

# Dependências de sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Permissões
RUN chown -R appuser:appuser /app
USER appuser

# Variáveis padrão
ENV PORT=8000
ENV DATABASE_URL=sqlite:///data.db

EXPOSE 8000

CMD ["python", "app.py"]

