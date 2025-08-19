import requests
import json

# Базовый URL API
BASE_URL = "http://localhost:8000"

def test_root():
    """Тест корневого endpoint"""
    print("=== Тест корневого endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_start_interview():
    """Тест начала интервью"""
    print("=== Тест начала интервью ===")
    data = {
        "topic": "javascript-basics",
        "difficulty": "middle",
        "question_count": 3
    }
    response = requests.post(f"{BASE_URL}/api/interview/start", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        return result["id"]  # Возвращаем ID интервью для дальнейших тестов
    return None

def test_get_question(interview_id):
    """Тест получения вопроса"""
    print("=== Тест получения вопроса ===")
    response = requests.get(f"{BASE_URL}/api/interview/question?interview_id={interview_id}")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        return result["question"]["id"]  # Возвращаем ID вопроса
    return None

def test_submit_answer(interview_id, question_id):
    """Тест отправки ответа"""
    print("=== Тест отправки ответа ===")
    data = {
        "interview_id": interview_id,
        "question_id": question_id,
        "answer": "var имеет функциональную область видимости, let и const имеют блочную область видимости, const нельзя переназначить",
        "time_spent": 60
    }
    response = requests.post(f"{BASE_URL}/api/interview/answer", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
    print()

def test_end_interview(interview_id):
    """Тест завершения интервью"""
    print("=== Тест завершения интервью ===")
    response = requests.post(f"{BASE_URL}/api/interview/end?interview_id={interview_id}")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
    print()

def main():
    """Основная функция тестирования"""
    print("🚀 Начинаем тестирование AI Interviewer API")
    print("=" * 50)
    
    # Тест 1: Корневой endpoint
    test_root()
    
    # Тест 2: Начало интервью
    interview_id = test_start_interview()
    
    if interview_id:
        # Тест 3: Получение вопроса
        question_id = test_get_question(interview_id)
        
        if question_id:
            # Тест 4: Отправка ответа
            test_submit_answer(interview_id, question_id)
            
            # Тест 5: Получение следующего вопроса
            test_get_question(interview_id)
            
            # Тест 6: Отправка второго ответа
            test_submit_answer(interview_id, "q2")
            
            # Тест 7: Завершение интервью
            test_end_interview(interview_id)
    
    print("✅ Тестирование завершено!")

if __name__ == "__main__":
    main()

