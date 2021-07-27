import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name('Users/admin/Documents/Telegram Bots/'
                                                         'ah_telegram_bot_2/google_services/creds.json', scope)

client = gspread.authorize(creds)

sheet = client.open('AH_Bot_Applicants').sheet1

