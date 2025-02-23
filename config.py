
class GeneralSettings:
    # использовать прокси | True - вкл / False - откл
    useProxies = True

    # кол-во потоков
    threads = 3

    # макс. кол-во символов в дробной части объёмов precision = [4, 6]
    precision = [3, 4]

    # задержки между стартом аккаунтов
    delay_start = [600, 3600]

    # запуск сразу нескольких модулей ["bridge", "wrap_unwrap", "mint_nft", "deploy"]
    start_modules = ["mint_nft", "wrap_unwrap"]


class BridgeSettings:
    # объём для бриджа в unichain [от, до] рекомендуемый минимум 0.0002
    amounts = [0.001, 0.0015]

    # из каких сетей бриджим, выбирается рандомная сеть из списка ["base", "op"], если ETH нет в выбранной сети, то берем другую сеть
    chains = ["base", "op"]

    # если объём ETH + WETH > заданного, то не бриджем
    min_amount = 0.0005

    # задержки между бриджем на кошельках
    delay = [10, 100]


class WrapUnwrapSettings:
    # объём для wrap/uwrap ETH [от, до]
    amounts = [0.0002, 0.001]

    # кол-во свапов за сессию
    count_swap = [1, 4]

    # зедержка между свапами
    delay_swap = [5, 30]

    # задержки между сессиями wrap/unwrap
    delay = [600, 3600]


class NftSettings:
    # макс. стоимость nft
    max_price = 0.00005

    # общее кол-во nft на кошельке [от, до]
    amounts = [4, 6]

    # задержки между минтом
    delay = [10, 100]

    # всегда минтить разные nft | True - вкл / False - откл
    mint_different = True

    # минтим nft если их заминтили > указанного
    min_nfts_minted = 30

class DeploySettings:
    # задержки между деплоем контракта на кошельках
    delay = [3600, 3600*3]

