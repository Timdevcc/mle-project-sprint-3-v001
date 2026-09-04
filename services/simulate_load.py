import random
import time
import requests


URL = "http://localhost:8000/api/apartments/predict-price"
INTERVAL_SECONDS = 0.5  
TOTAL_REQUESTS = 100


def generate_random_apartment() -> dict:
    rooms = random.randint(1, 4)
    total_area = round(random.uniform(25.0 * rooms, 35.0 * rooms), 1)
    living_area = round(total_area * random.uniform(0.5, 0.7), 1)
    kitchen_area = round(max(5.0, total_area - living_area - 10.0), 1)
    floors_total = random.randint(5, 25)
    floor = random.randint(1, floors_total)

    return {
        "floor": floor,
        "kitchen_area": kitchen_area,
        "living_area": living_area,
        "rooms": rooms,
        "is_apartment": random.choice([True, False]),
        "total_area": total_area,
        "build_year": random.randint(1960, 2024),
        "building_type_int": random.randint(1, 6),
        "latitude": round(random.uniform(55.55, 55.90), 6),
        "longitude": round(random.uniform(37.35, 37.85), 6),
        "ceiling_height": round(random.uniform(2.5, 3.2), 1),
        "flats_count": random.randint(50, 400),
        "floors_total": floors_total,
        "has_elevator": random.choice([True, False]),
    }


def run_simulation():
    count = 0

    while count < TOTAL_REQUESTS:
        count += 1
        user_id = random.randint(1, 1000)
        payload = generate_random_apartment()
        params = {"user_id": user_id}

        try:
            response = requests.post(URL, params=params, json=payload, timeout=5)
            if response.status_code == 200:
                pred_price = response.json().get("prediction", 0)
                print(f"[{count}] 200 OK | User: {user_id} | Price: {pred_price:,.0f} RUB")
            else:
                print(f"[{count}] Ошибка {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"[{count}] Сервис недоступен: {e}")

        time.sleep(INTERVAL_SECONDS)

    


if __name__ == "__main__":
    run_simulation()