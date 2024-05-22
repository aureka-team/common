import codecs


def base64_encoder(text: str) -> str:
    return codecs.encode(text.encode(), "base64").decode().strip()


def base64_decoder(base64_str: str) -> str:
    return codecs.decode(
        base64_str.encode(),
        "base64",
    ).decode()
