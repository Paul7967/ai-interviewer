"""
Демонстрация работы AI Interviewer API

Этот скрипт показывает, как работает наш FastAPI сервер
без необходимости его запуска.
"""

from main import app, interviews, questions_db
from fastapi.testclient import TestClient
import json

# Создаем тестовый клиент
client = TestClient(app)

def demo_api():
    """Демонстрация всех API endpoints"""
    
    print("🚀 Демонстрация AI Interviewer API")
    print("=" * 50)
    
    # 1. Тест корневого endpoint
    print("\n1️⃣ Тест корневого endpoint")
    print("-" * 30)
    response = client.get("/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 2. Начало интервью
    print("\n2️⃣ Начало интервью")
    print("-" * 30)
    interview_data = {
        "topic": "javascript-basics",
        "difficulty": "middle",
        "question_count": 3
    }
    response = client.post("/api/interview/start", json=interview_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        interview_id = result["id"]
        
        # 3. Получение первого вопроса
        print("\n3️⃣ Получение первого вопроса")
        print("-" * 30)
        response = client.get(f"/api/interview/question?interview_id={interview_id}")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            question_id = result["question"]["id"]
            
            # 4. Отправка ответа
            print("\n4️⃣ Отправка ответа")
            print("-" * 30)
            answer_data = {
                "interview_id": interview_id,
                "question_id": question_id,
                "answer": "var имеет функциональную область видимости, let и const имеют блочную область видимости, const нельзя переназначить",
                "time_spent": 60
            }
            response = client.post("/api/interview/answer", json=answer_data)
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 5. Получение второго вопроса
            print("\n5️⃣ Получение второго вопроса")
            print("-" * 30)
            response = client.get(f"/api/interview/question?interview_id={interview_id}")
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                question_id = result["question"]["id"]
                
                # 6. Отправка второго ответа
                print("\n6️⃣ Отправка второго ответа")
                print("-" * 30)
                answer_data = {
                    "interview_id": interview_id,
                    "question_id": question_id,
                    "answer": "Closure - это функция, которая имеет доступ к переменным из внешней области видимости",
                    "time_spent": 45
                }
                response = client.post("/api/interview/answer", json=answer_data)
                print(f"Status: {response.status_code}")
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
                
                # 7. Завершение интервью
                print("\n7️⃣ Завершение интервью")
                print("-" * 30)
                response = client.post(f"/api/interview/end?interview_id={interview_id}")
                print(f"Status: {response.status_code}")
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    print("\n✅ Демонстрация завершена!")

def show_available_questions():
    """Показать доступные вопросы"""
    print("\n📚 Доступные вопросы в базе данных:")
    print("=" * 50)
    
    for topic, questions in questions_db.items():
        print(f"\nТема: {topic}")
        print("-" * 30)
        for i, question in enumerate(questions, 1):
            print(f"{i}. {question['text']}")
            print(f"   Сложность: {question['difficulty']}")
            print()

def show_api_structure():
    """Показать структуру API"""
    print("\n🔧 Структура API:")
    print("=" * 30)
    
    endpoints = [
        ("GET", "/", "Корневой endpoint с информацией об API"),
        ("POST", "/api/interview/start", "Начать новое интервью"),
        ("GET", "/api/interview/question", "Получить текущий вопрос"),
        ("POST", "/api/interview/answer", "Отправить ответ на вопрос"),
        ("POST", "/api/interview/end", "Завершить интервью")
    ]
    
    for method, path, description in endpoints:
        print(f"{method:6} {path:<25} - {description}")

if __name__ == "__main__":
    # Показываем структуру API
    show_api_structure()
    
    # Показываем доступные вопросы
    show_available_questions()
    
    # Запускаем демонстрацию
    demo_api()
