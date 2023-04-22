#Config for get tokens from created local file
try:
    import config_local
    #https://t.me/BotFather
    TELEGRAM_TOKEN = config_local.TELEGRAM_TOKEN
    #https://apilayer.com/marketplace/exchangerates_data-api?utm_source=apilayermarketplace&utm_medium=featured
    CONVERSION_API = config_local.CONVERSION_API
    #https://www.pexels.com/ru-ru/api/documentation/
    PEXELS_API_KEY = config_local.PEXELS_API_KEY

    
except:
    print("ERROR Не найден config_local")