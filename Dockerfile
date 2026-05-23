# ETAP 1: Budowanie (Builder)
FROM python:3.11-slim AS builder

WORKDIR /app

# Instalacja bibliotek 
RUN pip install --no-cache-dir flask requests

# ETAP 2: Obraz końcowy (Runtime)
FROM python:3.11-slim

# Instalacja curl dla Healthchecka i usunięcie zbędnych list pakietów
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Tworzenie użytkownika
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin pogodynka

WORKDIR /app

# Kopiujemy zainstalowane biblioteki z buildera (standardowa ścieżka w systemie) i zamieniamy właściciela
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Kopiujemy kod aplikacji i folder templates
COPY . .

#Z mieniamy właściciela plików w /app na użytkownika 'pogodynka'
RUN chown -R pogodynka:appgroup /app

# Przełączenie użytkownika
USER pogodynka

# Nasłuchiwany port
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

CMD ["python", "app.py"]