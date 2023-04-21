try:
    import config_local
    TELEGRAM_TOKEN = config_local.TELEGRAM_TOKEN
    WEATHER_TOKEN = config_local.WEATHER_TOKEN
    WEBHOOK_URL = config_local.WEBHOOK_URL
    
except:
    print("ERROR Не найден config_local")