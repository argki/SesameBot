# Copyright (c) 2026 CircleTenThanks
"""Sesame スマートロックを操作する."""

import base64
import datetime
import json
import logging
import os

import requests
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.cmac import CMAC

# 参考: https://doc.candyhouse.co/ja/SesameAPI

LOGGER = logging.getLogger(__name__)
_REQUEST_TIMEOUT_SECONDS = 30
_CMD_PRESS_AND_RELEASE = 89
_CMAC_MESSAGE_SLICE = slice(2, 8)
_JST = datetime.timezone(datetime.timedelta(hours=9))


def main() -> None:
    """Sesame API で鍵を操作する."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    uuid = os.environ["UUID_SB"]
    secret_key = os.environ["SECRET_KEY_SB"]
    api_key = os.environ["API_KEY_SB"]

    history = "SesameBot"
    base64_history = base64.b64encode(bytes(history, "utf-8")).decode()

    LOGGER.info(base64_history)
    headers = {"x-api-key": api_key}

    ts = int(datetime.datetime.now(tz=_JST).timestamp())
    message = ts.to_bytes(4, byteorder="little")
    message_hex = message.hex()[_CMAC_MESSAGE_SLICE]

    cmac = CMAC(algorithms.AES(bytes.fromhex(secret_key)))
    cmac.update(bytes.fromhex(message_hex))
    sign = cmac.finalize().hex()

    url = f"https://app.candyhouse.co/api/sesame2/{uuid}/cmd"
    body = {
        "cmd": _CMD_PRESS_AND_RELEASE,
        "history": base64_history,
        "sign": sign,
    }
    res = requests.post(
        url,
        json.dumps(body),
        headers=headers,
        timeout=_REQUEST_TIMEOUT_SECONDS,
    )
    LOGGER.info("%s %s", res.status_code, res.text)


if __name__ == "__main__":
    main()
