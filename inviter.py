from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.sync import TelegramClient
from telethon.tl import functions
from time import sleep
import random

#############################################
# --- НЕОБХОДИМО ЗАПОЛНИТЬ!!! ---

api_id = 0
api_hash = 0
# -Название файла, в котором хранятся userId (должен находится в одной директории со скриптом)
users_file = 'chat_users.txt'
# -Название чата, куда приглашать юзеров (без @)
chat_name = 'asd'
device_model = "Pixel 3 XL"
system_version = "Android 10.0"

##########################################

if api_id == 0 or api_hash == 0:
    print("Пожалуйста, перед запуском скрипта отредактируйте необходимые данные в нём! Вы не заполнили такие важные поля, как 'api_id' или 'api_hash'")
    exit()


with TelegramClient('SESSION_FOR_TELEGRAM_INVITER', api_id, api_hash, device_model=device_model, system_version=system_version) as client:
    try:
        with open(users_file, 'r') as file:
            user_ids = file.readlines()

        user_ids = [user_id.strip() for user_id in user_ids if user_id.strip()]

        chat = client.get_entity(chat_name)
        chat_id = chat.id

        for user_id in user_ids:
            try:
                user_id = int(user_id)
                user = client.get_entity(user_id)
                if user:
                    client(functions.channels.InviteToChannelRequest(chat_id, [user]))
                    print(f"Пользователь с ID {user_id} приглашен в чат. Отдыхаю...")
                    sleep(random.randrange(10, 30)) ###### -Здесь можно установить другое значение секунд (от и до), например: sleep(random.randrange(1, 3)) будет означать, что скрипт будет приглашать юзеров не раньше, чем через секунду и не позже, чем три секунды.
                else:
                    print(f"Пользователь с ID {user_id} не найден.")
            except PeerFloodError as e:
                print(f"бан за флуд со стороны telegram: {e}")
                exit()
            except UserPrivacyRestrictedError:
                print(f"Юзер {user_id} установил настройки 'не приглашать меня в группы'")
            except Exception as e:
                print(f"Ошибка при приглашении пользователя с ID {user_id}: {str(e)}")

    except Exception as e:
        print(f"Ошибка при чтении файла: {str(e)}")