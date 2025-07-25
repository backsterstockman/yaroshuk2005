# Инструкция по развертыванию проекта

## Описание

Веб-приложение для загрузки и валидации JSON-файлов с последующим сохранением данных в PostgreSQL и просмотром записей через DataTables.  
**Внимание:** название репозитория должно соответствовать требованиям задания (4 латинские буквы + 1-5 цифр, без упоминаний тестового задания).

---

## 1. Клонирование репозитория

```bash
git clone https://github.com/backsterstockman/yaroshuk2005
cd yaroshuk2005
```

---

## 2. Настройка переменных окружения

Создайте `.env` со следующим содержимым:

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=digital_sp
DB_USER=postgres
DB_PASSWORD=postgres
```

---

## 3. Запуск через Docker Compose

```bash
docker-compose up --build
```

- Приложение будет доступно на [http://localhost/](http://localhost/)
- PostgreSQL будет доступен на порту 5432 (для подключения с вашей машины).

---

## 4. Использование приложения

- **Загрузка JSON:**  
  Перейдите на страницу [http://localhost/upload](http://localhost/upload), выберите и загрузите JSON-файл в формате:
    ```json
    [
      {
        "name": "random string less than 50 characters",
        "date": "2024-07-25_12:30"
      }
    ]
    ```
  - Если формат некорректный, появится сообщение об ошибке.
  - Если всё корректно — данные сохраняются в базу.

- **Просмотр записей:**  
  Перейдите на страницу [http://localhost/records](http://localhost/records), чтобы увидеть все записи в виде таблицы с поддержкой поиска и сортировки (DataTables).

---

## 5. Развёртывание на сервере (nginx + gunicorn)

### Пример docker-compose.yml уже включает сервис nginx.

### Пример конфига nginx.conf

```
events {}

http {
    server {
        listen 80;
        server_name _;

        location / {
            proxy_pass         http://app:8000;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Proto $scheme;
        }
    }
}
```

### Пример запуска gunicorn (если потребуется):

```bash
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
