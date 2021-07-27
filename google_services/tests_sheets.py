import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name('Users/admin/Documents/Telegram Bots/'
                                                               'ah_telegram_bot_2/google_services/'
                                                               'tests_credentials.json', scope)

client = gspread.authorize(credentials)

test_sheet = client.open('Тестирование знаний_Astana_Hub').sheet1
