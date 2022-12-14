# Задача Интерактиваня платформа для реализации инновационных идей
## inProject Backend
Backend

Репозиторий содержит код и данные для решения задачи в рамках конкурса "ЛИДЕРЫ ЦИФРОВОЙ ТРАНСФОРМАЦИИ 2022"

### Инструкция сборки
1. Запустить docker-compose
   ```docker-compose up --build -d```
2. Накатить миграции
   ```docker exec inproject_backend-backend-1 alembic upgrade head```

### Cтруктура проекта
1. ```app``` - папка api веб приложения
   - ```api```
     - ```dependencies``` - зависимости маршрутов
     - ```error``` - http ошибки
     - ```routes``` - маршруты апи
   - ```core```
     - ```celery_app.py``` - настройки celery и фоновые задачи
     - ```config.py``` - конфигурация приложения
   - ```db``` - настройки подключения к БД
   - ```models``` - модели таблиц для БД
   - ```repositories``` - репозитории с запросами к БД
   - ```schemas``` - схемы для получения и выдачи информации
   - ```services``` - объединяет работу со схемами и репозиториями
<!--  -->
2. ```ml``` - папка с фоновыми задачами искусственного интеллекта
<!--  -->
3. ```alembic``` - папка с миграциями


### Фоновые задачи
В проекте существует 4 фоновые задачи:
1. ```audit``` - отслеживает все запросы в которых присутствует заголовок "Authorization": "Bearer <token>"
2. ```relation_project``` - просчитывает схожесть проектов с помощью трансформера
   - Активируется на следующих api маршрутах
     - ```POST /api/project```
3. ```calculate_recommendation_users_and_projects``` - подбирает рекомендуемые проекты для участников и рекомендуемых участников для проектов
   - Активируется на следующих api маршрутах
     - ```POST /api/project```
     - ```PUT /api/user```
4. ```recomended_category``` - классификация категорий на основе анализа семантики проекта
   - Активируется на следующих api маршрутах
     - ```POST /api/project```
