import re
import random
import asyncio

from pyrogram import Client, errors
from pyrogram.types.user_and_chats.chat_preview import ChatPreview

from loguru import logger

from config import api_id, api_hash, session_name

logger.add('info.log')

USERS_FILE = 'users.txt'

USERNAME_REGEX = r'https?://t\.me/([a-zA-Z0-9_]+)'
INVITE_REGEX = r'https?://t\.me/\+([a-zA-Z0-9_-]+)'


def extract_entity_from_link(link: str) -> str:
    """
    Извлекает имя пользователя (публичного канала или группы) или инвайт-ссылку
    из переданной ссылки.

    :param link: URL на публичный канал/группу или инвайт-ссылка.
    :return: Имя пользователя (публичного канала или группы) или инвайт-ссылка.
    :raises ValueError: Если ссылка не соответствует ожидаемому формату.
    """

    if re.match(INVITE_REGEX, link):
        return link
    if match := re.match(USERNAME_REGEX, link):
        return match.group(1)
    raise ValueError('Некорректная ссылка')


async def get_users(filepath: str) -> list[str]:
    """
    Читает список пользователей из файла.

    :param filepath: Путь к файлу с именами пользователей.
    :return: Список пользователей.
    """

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logger.error(f'Файл "{filepath}" не найден!')
        return []
    except Exception as error:
        logger.error(f'Ошибка при чтении файла "{filepath}": {error}')
        return []


async def main():
    """
    Основная асинхронная функция программы, которая управляет процессом
    добавления пользователей в группу или канал.
    """

    async with Client(session_name, api_id, api_hash) as app:
        app: Client

        logger.info(f'Получаем имена пользователей из файла "{USERS_FILE}".')
        users = await get_users(filepath=USERS_FILE)
        num_users = len(users)
        logger.info(f'Получено пользователей: {num_users}.')
        if not users:
            logger.warning(f'Нет пользователей для приглашения.')
            return

        while True:
            invitation_link = input(f'\nВставьте ссылку на канал или группу для приглашения: ')
            try:
                target_entity = await app.get_chat(extract_entity_from_link(invitation_link))
                break
            except ValueError as error:
                logger.warning(f'Ошибка ввода: {error}')
            except Exception as error:
                logger.error(f'Не удалось получить чат: {error}')

        if isinstance(target_entity, ChatPreview):
            logger.info(f'Присоединяемся к группе {invitation_link}')
            try:
                target_entity = await app.join_chat(invitation_link)
            except Exception as error:
                logger.error(f'Не удалось присоединиться к группе: {error}')
                return

        logger.info(f'\nНачинаем процесс добавления {num_users} пользователей в канал/группу:\n')

        added = 0

        _max_len = len(str(num_users))
        for i, username in enumerate(users, start=1):
            logger.info(f'{i:>{_max_len}} - ', end='')
            try:
                is_added = await app.add_chat_members(chat_id=target_entity.id, user_ids=[username])
                if is_added:
                    logger.info(f'Пользователь {username} добавлен.')
                    added += 1
                else:
                    raise errors.UserNotParticipant
            except errors.FloodWait as error:
                logger.warning(f'Превышен лимит добавлений. Подождите {error.value} секунд.'
                               f' Добавлено: {added} пользователей.')
                await asyncio.sleep(error.value + 1)
            except errors.UserPrivacyRestricted:
                logger.warning(f'Пользователь {username} ограничил доступ к своим данным.')
            except errors.UserNotParticipant:
                logger.warning(f'Пользователь {username} не был добавлен, возможно, он ограничил доступ.')
            except errors.UserNotMutualContact:
                logger.warning(f'Пользователь {username} не является вашим взаимным контактом, добавление невозможно.')
            except errors.UserAlreadyParticipant:
                logger.info(f'Пользователь {username} уже является участником данного канала/группы.')
            except errors.UsernameInvalid:
                logger.warning(f'Невалидное имя пользователя: {username}')
            except (errors.ChatWriteForbidden, errors.ChatAdminRequired, errors.ChatAdminInviteRequired):
                logger.error(f'У вас недостаточно прав для добавления пользователей в данный канал/группу.')
                return
            except Exception as error:
                logger.error(f'Не удалось добавить пользователя {username}: {str(error)}')

            await asyncio.sleep(random.uniform(0.5, 1))

        logger.info(f'\nВсего добавлено: {added} пользователей.')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Завершение программы.')
    except Exception as critical_error:
        logger.critical(f'Необработанная ошибка: {critical_error}')
