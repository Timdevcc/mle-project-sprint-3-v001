# Инструкции по запуску микросервиса

Каждая инструкция выполняется из директории репозитория mle-sprint3-completed
Если необходимо перейти в поддиректорию, напишите соотвесвтующую команду

## 1. FastAPI микросервис в виртуальном окружение
```bash
# команды создания виртуального окружения
python -m venv .venv
source .venv/bin/activate
# команда перехода в директорию
cd services
#установки необходимых библиотек 
pip install -r requirements.txt
# команда запуска сервиса с помощью uvicorn
uvicorn ml_service.service:app --reload --host 0.0.0.0 --port 8000
```
### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:8000/api/apartments/predict-price?user_id=123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "floor": 7,
  "kitchen_area": 10.5,
  "living_area": 32.0,
  "rooms": 2,
  "is_apartment": false,
  "total_area": 54.2,
  "build_year": 2005,
  "building_type_int": 4,
  "latitude": 55.751244,
  "longitude": 37.618423,
  "ceiling_height": 2.7,
  "flats_count": 180,
  "floors_total": 14,
  "has_elevator": true
}'
```
Ответ модели в формате: {"used_id": user_id, "prediction": model_prediction}

## 2. FastAPI микросервис в Docker-контейнере

```bash
# команда перехода в нужную директорию
cd services
#создание образа
docker image build -f Dockerfile_ml_service -t ml_service:v1 .
#запуск
docker container run -d --name ml_service -p 8000:8000 --env-file .env -v ./models:/service/models ml_service:v1
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:8000/api/apartments/predict-price?user_id=123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "floor": 7,
  "kitchen_area": 10.5,
  "living_area": 32.0,
  "rooms": 2,
  "is_apartment": false,
  "total_area": 54.2,
  "build_year": 2005,
  "building_type_int": 4,
  "latitude": 55.751244,
  "longitude": 37.618423,
  "ceiling_height": 2.7,
  "flats_count": 180,
  "floors_total": 14,
  "has_elevator": true
}'
```

## 3. Docker compose для микросервиса и системы моониторинга

```bash
# команда перехода в нужную директорию
cd services
# команда для запуска микросервиса в режиме docker compose
docker compose up --build
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:8000/api/apartments/predict-price?user_id=123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "floor": 7,
  "kitchen_area": 10.5,
  "living_area": 32.0,
  "rooms": 2,
  "is_apartment": false,
  "total_area": 54.2,
  "build_year": 2005,
  "building_type_int": 4,
  "latitude": 55.751244,
  "longitude": 37.618423,
  "ceiling_height": 2.7,
  "flats_count": 180,
  "floors_total": 14,
  "has_elevator": true
}'
```

## 4. Скрипт симуляции нагрузки
Скрипт генерирует 100 запросов c интервалом 0.5 секунд со случайными параметрами.

```bash
# команды необходимые для запуска скрипта
cd services
python3 simulate_load.py
```

Адреса сервисов:
- микросервис: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000