#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных с начальными данными
"""

import asyncio
from prisma import Prisma

# Начальные вопросы для JavaScript интервью
INITIAL_QUESTIONS = [
    {
        "text": "Что такое замыкание (closure) в JavaScript?",
        "category": "javascript",
        "difficulty": "medium",
        "correctAnswer": "Замыкание - это функция, которая имеет доступ к переменным из внешней области видимости даже после того, как внешняя функция завершила выполнение.",
        "explanation": "Замыкания позволяют функциям 'запоминать' переменные из внешней области видимости. Это мощный механизм для создания приватных переменных и сохранения состояния.",
        "tags": ["closures", "functions", "scope"]
    },
    {
        "text": "В чем разница между var, let и const?",
        "category": "javascript",
        "difficulty": "easy",
        "correctAnswer": "var - функциональная область видимости, можно переопределять; let - блочная область видимости, можно изменять значение; const - блочная область видимости, нельзя изменять значение.",
        "explanation": "var имеет функциональную область видимости и поднимается (hoisting). let и const имеют блочную область видимости, но const нельзя переназначать.",
        "tags": ["variables", "scope", "es6"]
    },
    {
        "text": "Что такое промисы (Promises) в JavaScript?",
        "category": "javascript",
        "difficulty": "medium",
        "correctAnswer": "Промисы - это объекты, представляющие результат асинхронной операции. Они могут находиться в состоянии pending, fulfilled или rejected.",
        "explanation": "Промисы помогают избежать callback hell и лучше обрабатывать асинхронные операции. Они поддерживают цепочки .then() и .catch().",
        "tags": ["promises", "async", "es6"]
    },
    {
        "text": "Объясните концепцию прототипного наследования в JavaScript",
        "category": "javascript",
        "difficulty": "hard",
        "correctAnswer": "В JavaScript наследование основано на прототипах. Каждый объект имеет внутреннюю ссылку на другой объект, называемый его прототипом.",
        "explanation": "Когда мы обращаемся к свойству объекта, JavaScript сначала ищет его в самом объекте, затем в его прототипе, затем в прототипе прототипа и так далее по цепочке прототипов.",
        "tags": ["prototypes", "inheritance", "objects"]
    },
    {
        "text": "Что такое event loop в JavaScript?",
        "category": "javascript",
        "difficulty": "hard",
        "correctAnswer": "Event loop - это механизм, который позволяет JavaScript выполнять неблокирующие операции, несмотря на то, что JavaScript однопоточный.",
        "explanation": "Event loop постоянно проверяет call stack и callback queue. Когда call stack пуст, он берет первую задачу из callback queue и помещает ее в call stack для выполнения.",
        "tags": ["event-loop", "async", "performance"]
    }
]

async def init_database():
    """Инициализация базы данных"""
    prisma = Prisma()
    
    try:
        await prisma.connect()
        
        print("🔗 Подключение к базе данных установлено")
        
        # Проверяем, есть ли уже вопросы в базе
        existing_questions = await prisma.question.find_many()
        
        if existing_questions:
            print(f"📊 В базе уже есть {len(existing_questions)} вопросов")
            return
        
        print("📝 Создание начальных вопросов...")
        
        # Создаем начальные вопросы
        for question_data in INITIAL_QUESTIONS:
            await prisma.question.create({
                'data': question_data
            })
            print(f"✅ Создан вопрос: {question_data['text'][:50]}...")
        
        print(f"🎉 Успешно создано {len(INITIAL_QUESTIONS)} вопросов")
        
    except Exception as e:
        print(f"❌ Ошибка при инициализации базы данных: {e}")
        raise
    finally:
        await prisma.disconnect()

if __name__ == "__main__":
    asyncio.run(init_database())
