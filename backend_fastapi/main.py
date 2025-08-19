from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

# Создание FastAPI приложения
app = FastAPI(
    title="AI Interviewer API",
    description="Простой API для проведения технических интервью по JavaScript",
    version="1.0.0"
)

# Модели данных (Pydantic)
class InterviewStartRequest(BaseModel):
    topic: str
    difficulty: str = "middle"
    question_count: int = 10

class InterviewSession(BaseModel):
    id: str
    topic: str
    difficulty: str
    current_question: int
    total_questions: int
    score: int = 0
    start_time: datetime
    is_active: bool = True

class Question(BaseModel):
    id: str
    text: str
    topic: str
    difficulty: str
    question_number: int

class AnswerRequest(BaseModel):
    interview_id: str
    question_id: str
    answer: str
    time_spent: int

class Feedback(BaseModel):
    score: int
    comment: str
    suggestions: List[str]
    correct_answer: str

# Хранилище данных (в памяти для простоты)
interviews = {}
questions_db = {
    "javascript-basics": [
        {
            "id": "q1",
            "text": "Объясните разницу между var, let и const в JavaScript",
            "topic": "javascript-basics",
            "difficulty": "middle",
            "correct_answer": "var имеет функциональную область видимости и поднимается (hoisting), let и const имеют блочную область видимости, const нельзя переназначить"
        },
        {
            "id": "q2", 
            "text": "Что такое closure в JavaScript?",
            "topic": "javascript-basics",
            "difficulty": "middle",
            "correct_answer": "Closure - это функция, которая имеет доступ к переменным из внешней области видимости даже после завершения выполнения внешней функции"
        },
        {
            "id": "q3",
            "text": "Объясните, что такое Event Loop в JavaScript",
            "topic": "javascript-basics", 
            "difficulty": "senior",
            "correct_answer": "Event Loop - это механизм, который позволяет JavaScript выполнять неблокирующие операции, несмотря на то, что JavaScript однопоточный"
        }
    ]
}

# API Endpoints

@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "AI Interviewer API",
        "version": "1.0.0",
        "endpoints": {
            "start_interview": "POST /api/interview/start",
            "get_question": "GET /api/interview/question",
            "submit_answer": "POST /api/interview/answer", 
            "end_interview": "POST /api/interview/end"
        }
    }

@app.post("/api/interview/start", response_model=InterviewSession)
async def start_interview(request: InterviewStartRequest):
    """
    Начать новое интервью
    
    - **topic**: Тема интервью (например, "javascript-basics")
    - **difficulty**: Уровень сложности ("junior", "middle", "senior")
    - **question_count**: Количество вопросов
    """
    interview_id = str(uuid.uuid4())
    
    # Проверяем, есть ли вопросы для данной темы
    if request.topic not in questions_db:
        raise HTTPException(status_code=404, detail=f"Вопросы для темы '{request.topic}' не найдены")
    
    # Создаем новую сессию интервью
    session = InterviewSession(
        id=interview_id,
        topic=request.topic,
        difficulty=request.difficulty,
        current_question=1,
        total_questions=min(request.question_count, len(questions_db[request.topic])),
        start_time=datetime.now()
    )
    
    # Сохраняем сессию
    interviews[interview_id] = session
    
    return session

@app.get("/api/interview/question")
async def get_question(interview_id: str):
    """
    Получить текущий вопрос для интервью
    
    - **interview_id**: ID сессии интервью
    """
    # Проверяем существование сессии
    if interview_id not in interviews:
        raise HTTPException(status_code=404, detail="Сессия интервью не найдена")
    
    session = interviews[interview_id]
    
    # Проверяем, не завершено ли интервью
    if not session.is_active:
        raise HTTPException(status_code=400, detail="Интервью уже завершено")
    
    # Проверяем, не закончились ли вопросы
    if session.current_question > session.total_questions:
        raise HTTPException(status_code=400, detail="Все вопросы пройдены")
    
    # Получаем вопрос
    topic_questions = questions_db[session.topic]
    question_index = session.current_question - 1
    
    if question_index >= len(topic_questions):
        raise HTTPException(status_code=400, detail="Вопросы закончились")
    
    question_data = topic_questions[question_index]
    
    question = Question(
        id=question_data["id"],
        text=question_data["text"],
        topic=question_data["topic"],
        difficulty=question_data["difficulty"],
        question_number=session.current_question
    )
    
    return {
        "question": question,
        "progress": {
            "current": session.current_question,
            "total": session.total_questions,
            "score": session.score
        }
    }

@app.post("/api/interview/answer", response_model=Feedback)
async def submit_answer(request: AnswerRequest):
    """
    Отправить ответ на вопрос и получить фидбэк
    
    - **interview_id**: ID сессии интервью
    - **question_id**: ID вопроса
    - **answer**: Ответ пользователя
    - **time_spent**: Время, потраченное на ответ (в секундах)
    """
    # Проверяем существование сессии
    if request.interview_id not in interviews:
        raise HTTPException(status_code=404, detail="Сессия интервью не найдена")
    
    session = interviews[request.interview_id]
    
    # Проверяем, не завершено ли интервью
    if not session.is_active:
        raise HTTPException(status_code=400, detail="Интервью уже завершено")
    
    # Находим вопрос в базе
    topic_questions = questions_db[session.topic]
    current_question = None
    
    for q in topic_questions:
        if q["id"] == request.question_id:
            current_question = q
            break
    
    if not current_question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    
    # Простой анализ ответа (в реальном проекте здесь будет AI)
    score = analyze_answer_simple(request.answer, current_question["correct_answer"])
    
    # Обновляем сессию
    session.score += score
    session.current_question += 1
    
    # Генерируем фидбэк
    feedback = generate_feedback(score, request.answer, current_question["correct_answer"])
    
    return feedback

@app.post("/api/interview/end")
async def end_interview(interview_id: str):
    """
    Завершить интервью
    
    - **interview_id**: ID сессии интервью
    """
    # Проверяем существование сессии
    if interview_id not in interviews:
        raise HTTPException(status_code=404, detail="Сессия интервью не найдена")
    
    session = interviews[interview_id]
    
    # Завершаем интервью
    session.is_active = False
    
    # Вычисляем итоговую оценку
    total_score = session.score
    max_possible_score = session.total_questions * 10
    percentage = (total_score / max_possible_score) * 100 if max_possible_score > 0 else 0
    
    return {
        "message": "Интервью завершено",
        "final_score": total_score,
        "max_possible_score": max_possible_score,
        "percentage": round(percentage, 2),
        "questions_answered": session.current_question - 1,
        "total_questions": session.total_questions
    }

# Вспомогательные функции

def analyze_answer_simple(user_answer: str, correct_answer: str) -> int:
    """
    Простой анализ ответа (заглушка для AI)
    В реальном проекте здесь будет интеграция с Ollama или OpenAI
    """
    user_words = set(user_answer.lower().split())
    correct_words = set(correct_answer.lower().split())
    
    # Простое сравнение по ключевым словам
    common_words = user_words.intersection(correct_words)
    
    if len(common_words) >= len(correct_words) * 0.7:
        return 9  # Отличный ответ
    elif len(common_words) >= len(correct_words) * 0.5:
        return 7  # Хороший ответ
    elif len(common_words) >= len(correct_words) * 0.3:
        return 5  # Средний ответ
    else:
        return 3  # Слабый ответ

def generate_feedback(score: int, user_answer: str, correct_answer: str) -> Feedback:
    """Генерация фидбэка на основе оценки"""
    
    if score >= 8:
        comment = "Отличный ответ! Вы хорошо понимаете концепцию."
        suggestions = ["Можете добавить практические примеры", "Рассмотрите edge cases"]
    elif score >= 6:
        comment = "Хороший ответ, но есть возможности для улучшения."
        suggestions = ["Добавьте больше деталей", "Приведите примеры кода"]
    elif score >= 4:
        comment = "Базовое понимание есть, но нужно углубить знания."
        suggestions = ["Изучите документацию", "Попрактикуйтесь с примерами"]
    else:
        comment = "Рекомендуется изучить тему более детально."
        suggestions = ["Прочитайте учебные материалы", "Посмотрите видеоуроки"]
    
    return Feedback(
        score=score,
        comment=comment,
        suggestions=suggestions,
        correct_answer=correct_answer
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

