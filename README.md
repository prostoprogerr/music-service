## Music Similarity Service

Сервис помогает находить музыкальные треки, похожие на заданный, используя базу Deezer. Просто введите исполнителя и название трека – система покажет список рекомендуемых композиций с возможностью прослушивания фрагментов и сохранения в личные плейлисты.

Ссылка на рабочий проект: https://prostoproger.pythonanywhere.com

## Технологии
  - Backend: Python 3.10, Django 5.1.15
  - База данных: SQLite
  - Внешние интеграции: Deezer API
  - Аналитика: Собственная логика (на основе данных от Deezer сервис вычисляет коэффициент схожести "match_score"),  хранение истории (связи между треками сохраняются в модели "Similarity")
  - Frontend: Bootstrap 5.3, Кастомные CSS-стили, HTML5 Audio API

## Скриншоты

https://raw.githubusercontent.com/prostoprogerr/music-service/refs/heads/main/music_project/%D0%93%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0.jpg
*Главная страница с приветствием и навигацией.*

https://github.com/prostoprogerr/music-service/blob/main/music_project/%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%20%D1%82%D1%80%D0%B5%D0%BA%D0%BE%D0%B2.jpg
*Список похожих треков с плеерами и возможностью выбора для плейлиста.*

https://raw.githubusercontent.com/prostoprogerr/music-service/refs/heads/main/music_project/%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BB%D0%B5%D0%B9%D0%BB%D0%B8%D1%81%D1%82.jpg
*Просмотр сохранённого плейлиста с треками и плеерами.*

## Как запустить проект локально
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/prostoprogerr/music-service.git
   cd music-service
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   venv\Scripts\activate     # для Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Выполните миграции:
   ```bash
   python manage.py migrate
   ```
5. Запустите сервер:
   ```bash
   python manage.py runserver
   ```
6. Откройте проект в браузере:
   Перейдите по ссылке: http://127.0.0.1:8000/
