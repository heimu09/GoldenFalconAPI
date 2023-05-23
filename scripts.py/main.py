import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# Загрузка данных из файла Excel
df = pd.read_excel('scripts.py\\output_formatted.xlsx')

df = df.rename(columns={'ФИО (полное)': 'name', 'Должность (полное)': 'position', 'Телефон сотовый': 'phone', 'Пароль': 'password'})

# Преобразование данных в список словарей
candidates = df.to_dict('records')
# URL эндпоинта API
url = 'http://127.0.0.1:8000/api/v1/candidates/'
username = "heimu"
password = 'leopoldfitz'

# Отправка POST-запроса на API для создания кандидатов
for candidate in candidates:
    response = requests.post(url, data=candidate, auth=HTTPBasicAuth(username, password))
    if response.status_code == 201:
        print(f'Кандидат {candidate["name"]} успешно создан')
    else:
        print(f'Ошибка при создании кандидата {candidate["name"]}: {response.text}')
        break


# import pandas as pd
# from .models import Vote

# # Извлечение данных из базы данных
# votes = Vote.objects.all()

# # Список словарей для хранения данных голосов
# data = []

# # Итерация по всем голосам и их связанным данным
# for vote in votes:
#     vote_data = {
#         'ID голоса': vote.id,
#         'ФИО избирателя': vote.voter.full_name,
#         'Фотография для голосования': vote.voter.photo.url,
#         'Номер телефона': vote.voter.phone,
#         'Электронная почта': vote.voter.email,
#         'Краткая биографическая информация': vote.voter.biography,
#         'Перечень информационных материалов': vote.voter.materials,
#         'Номинация': vote.nomination,
#     }
#     data.append(vote_data)

# # Создание DataFrame из данных голосов
# df = pd.DataFrame(data)

# # Запись DataFrame в файл Excel
# df.to_excel('votes.xlsx', index=False)
