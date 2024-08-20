# Telegram Inviter

Этот проект представляет собой скрипт для автоматического добавления 
пользователей в Telegram каналы и группы с использованием библиотеки Pyrogram.

## Получение API-ключей

Перед установкой необходимо получить api-ключи:

1. Зайдите на сайт [my.telegram.org](https://my.telegram.org/).
2. Войдите в свою учетную запись Telegram с помощью вашего номера телефона. 
3. Перейдите в раздел "API Development Tools". 
4. Создайте новое приложение, если у вас его еще нет. 
5. После создания вы получите `API_ID` и `API_HASH` вашего приложения.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/stepkacorporation/TeleInviter.git
   cd TeleInviter
   ```
   
2. Создайте виртуальное окружение и активируйте его:

   ```bash
   # Для Linux/Mac
   python3 -m venv venv  
   source venv/bin/activate 
   ```
   
   ```bash
   # Для Windows
   python -m venv venv  # или py -m venv venv
   venv/Scripts/activate 
   ```

3. Установите необходимые зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл **\`.env\`** в корневой директории проекта и добавьте в него свои API ключи:

   ```text
   API_ID=your_api_id_here
   API_HASH=your_api_hash_here
   SESSION_NAME=your_session_name_here
   ```
   
   Замените `your_api_id_here`, `your_api_hash_here`, и `your_session_name_here` на ваши реальные значения.


## Использование

1. Подготовьте файл **\`users.txt\`**, содержащий список пользователей, которых нужно будет добавить в канал или группу. 
Пример содержания:

   ```text
   username1
   username2
   ```
   
2. Запустите скрипт:

   ```bash
   python main.py
   ```
   
3. Введите ссылку на канал или группу, куда хотите добавить пользователей.
4. Скрипт автоматически добавит пользователей в указанный канал или группу.
