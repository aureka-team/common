import codecs


def base64_encoder(binary_data: bytes) -> str:
    return codecs.encode(binary_data, "base64").strip().decode()


def base64_decoder(base64_str: str) -> bytes:
    return codecs.decode(
        base64_str.encode(),
        "base64",
    )
