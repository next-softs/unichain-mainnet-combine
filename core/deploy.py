from concurrent.futures import ThreadPoolExecutor

from utils.logs import logger
from contracts.Owlto import *
from config import *

import random, time


def deploy(acc):
    client = Owlto(acc)
    resp = client.deploy()
    time.sleep(random.randint(*DeploySettings.delay))
    return resp

def start_deploy(accounts):
    random.shuffle(accounts)

    with ThreadPoolExecutor(max_workers=GeneralSettings.threads) as executor:
        futures = [executor.submit(deploy, acc) for acc in accounts]

        for future in futures:
            future.result()
