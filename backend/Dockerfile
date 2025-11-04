# ==========================
# Stage 1: Build
# ==========================
FROM python:3.12-alpine AS builder

# Zainstaluj zależności do kompilacji pakietów
RUN apk add --no-cache build-base gfortran musl-dev lapack-dev

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj plik z zależnościami i zainstaluj paczki
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj kod aplikacji
COPY . .

# Jeśli jakieś pakiety są potrzebne tylko w build stage, można je odinstalować
# np. pandas, numpy (przykład)
# RUN pip uninstall -y pandas && apk del build-base gfortran musl-dev lapack-dev

# ==========================
# Stage 2: Runtime
# ==========================
FROM python:3.12-alpine

# Katalog roboczy
WORKDIR /app

# Skopiuj tylko zainstalowane paczki i kod aplikacji
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/main.py ./main.py
COPY --from=builder /app/src ./src

# Eksponuj port z ustawień Pydantic Settings
EXPOSE 8000

# Uruchom FastAPI
CMD ["python", "main.py"]
