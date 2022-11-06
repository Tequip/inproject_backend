# InProject Backend
Backend

Инструкция сборки docker
1. git clone git@github.com:Tequip/CrowdBackend.git
2. Скачать 2 файла с https://disk.yandex.ru/d/UC0yQk6gqFxY4g и поместить их в корень проекта
   (../CrowdBackend/.env) (../CrowdBackend/Crowd.db)
3. Находясь в директории CrowdBackend выполнить `docker build -f Dockerfile.dev -t crowd .`
4. Запустить контейнер `docker run -d -p 8000:80 --name=crowd_backend --rm crowd` 