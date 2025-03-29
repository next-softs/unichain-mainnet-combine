# === UNICHAIN MAINNET COMBINE 1.1 ===

**UNICHAIN MAINNET COMBINE** — это бот для автоматизации взаимодействия с блокчейном unichain.  

## Функционал бота:  
- Запуск сразу нескольких модулей
- [Бридж](https://superbridge.app/) ETH из OP/Base в Unichain
- [Врап](https://app.uniswap.org/swap) ETH
- [Свап](https://app.uniswap.org/swap) ETH на USDC и обратно  
- Деплой контрактов на [Owlto](https://owlto.finance/deploy/?chain=Unichain)  
- Минт рандомных nft [nfts2,](https://nfts2.me/unichain/free/all-time) [morkie](https://morkie.xyz/)
- Проверка баланса на кошельках ETH и вывод кол-ва транзакций

## Параметры:  
- Случайные задержки между действиями
- Случайные объёмы ETH
- Случайные транзакции
- Кол-во одновременно запущенных потоков
- Фильтрация nft для минта

## Установка:  
- [Устанавливаете](https://www.python.org/downloads/) `python 3.13`  
- Запускаете файл `setup.bat`

## Запуск:  
- В файле `data>private_keys.txt` указываете приватные ключи.  
- В файле `data>proxies.txt` указываете прокси. Первый ключ соответствует первому прокси в списке, второй к второму и тд. Если ключей больше чем прокси, то прокси пойдут по кругу.  
- Запускать бота файлом `start.bat`  

[![Telegram](https://img.shields.io/badge/-Telegram-090909?style=for-the-badge&logo=telegram&logoColor=27A0D9&color=02223b)](https://t.me/next_softs)
