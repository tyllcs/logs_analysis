# Project Dataset's Log Analisys

## Данные
Данные для проекта взяты с Kaggle:

**[Web Server Access Logs](https://www.kaggle.com/datasets/eliasdabbas/web-server-access-logs)**

## Загрузка данных
1. Перейдите по ссылке на Kaggle
2. Скачайте `access.log`
3. Поместите файл в папку `data`

## Архитертура
- **data/** - папка для данных
- **src/main.py** - основной файл с логикой
- **tests/** - модульные тесты (pytest)

## Как запустить через Docker
1. Если нет, установите [Docker](https://www.docker.com/products/docker-desktop/)
2. Найдите и запустите образ tyllcs/weblogs:latest

Запуск тестов:
```bash
docker run --rm tyllcs/weblogs:latest
```
Запуск в интерактивном режиме:
```bash
docker run --rm -it tyllcs/weblogs:latest
```
Образ доступен на Docker Hub: https://hub.docker.com/repository/docker/tyllcs/weblogs

## Загрузка
```bash
pip install -r requirements
```