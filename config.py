
class GeneralSettings:
    # использовать прокси | True - вкл / False - откл
    useProxies = True

    # кол-во потоков
    threads = 1

    # макс. кол-во символов в дробной части объёмов precision = [4, 6]
    precision = [4, 6]

    # задержки между стартом аккаунтов
    delay_start = [600, 3600]

    # запуск сразу нескольких модулей ["bridge", "swap", "mint_nft", "deploy"]
    start_modules = ["swap", "deploy"]


class BridgeSettings:
    # объём для бриджа в unichain [от, до] рекомендуемый минимум 0.0002
    amounts = [0.003, 0.0035]

    # из каких сетей бриджим, выбирается рандомная сеть из списка ["base", "op"], если ETH нет в выбранной сети, то берем другую сеть
    chains = ["base", "op"]

    # если объём ETH + WETH > заданного, то не бриджем
    min_amount = 0.003

    # задержки между бриджем на кошельках
    delay = [60, 600]

class SwapSettings:
    # на какие монеты свапаем ["WETH", "USDC"]
    coins = ["WETH", "USDC"]

    # объём для wrap/uwrap ETH [от, до]
    amounts = [0.0002, 0.001]

    # минимальный объём ETH при котором всегда продаем
    min_amount_for_sell = 0.0003

    # кол-во свапов за сессию
    count_swap = [1, 4]

    # зедержка между свапами
    delay_swap = [5, 30]

    # задержки между сессиями wrap/unwrap
    delay = [600, 3600]


class NftSettings:
    # где покупаем NFT ["morkie", "nfts2"]
    market_nft = ["morkie"]

    # макс. стоимость nft
    max_price = 0.00005

    # общее кол-во nft на кошельке [от, до]
    amounts = [7, 9]

    # задержки между минтом
    delay = [5, 15]

    # всегда минтить разные nft | True - вкл / False - откл
    mint_different = True

    # минтим nft если их заминтили > указанного
    min_nfts_minted = 110

class DeploySettings:
    # задержки между деплоем контракта на кошельках
    delay = [600, 3600]

