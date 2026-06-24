FROM python:3.12-slim

# Usuario sin privilegios (no ejecutar como root = más seguro)
RUN useradd --create-home --uid 1000 appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER appuser

EXPOSE 8080

# 1) inicializa la BD (con reintentos)  2) arranca gunicorn (servidor de producción)
CMD ["sh", "-c", "python -c 'import app; app.init_db()' && gunicorn --bind 0.0.0.0:8080 --workers 2 app:app"]