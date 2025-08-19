"""
Скрипт для экспорта OpenAPI схемы в JSON файл
"""

import json
from main import app

def export_openapi_schema():
    """Экспортировать OpenAPI схему в JSON файл"""
    
    # Получаем OpenAPI схему
    openapi_schema = app.openapi()
    
    # Сохраняем в файл
    with open("openapi_schema.json", "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    
    print("✅ OpenAPI схема экспортирована в файл: openapi_schema.json")
    print(f"📊 Схема содержит {len(openapi_schema['paths'])} endpoints")
    
    # Показываем список endpoints
    print("\n📋 Доступные endpoints:")
    for path, methods in openapi_schema['paths'].items():
        for method in methods.keys():
            print(f"  {method.upper():6} {path}")
    
    # Показываем модели данных
    print(f"\n📝 Модели данных ({len(openapi_schema['components']['schemas'])}):")
    for model_name in openapi_schema['components']['schemas'].keys():
        print(f"  - {model_name}")

if __name__ == "__main__":
    export_openapi_schema()

