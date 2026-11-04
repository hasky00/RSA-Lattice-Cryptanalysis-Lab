from rsa_lab.rsa import generate_toy_key, encrypt, decrypt, validate_key


def test_toy_rsa_round_trip():
    key = generate_toy_key(bits=32)
    message = 1234
    assert validate_key(key)
    assert decrypt(encrypt(message, key.n, key.e), key) == message
