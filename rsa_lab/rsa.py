"""Small, educational RSA arithmetic. Not suitable for production use."""

from dataclasses import dataclass
from math import gcd
from secrets import randbits, randbelow


@dataclass(frozen=True)
class ToyRSAKey:
    n: int
    e: int
    d: int
    p: int
    q: int
    phi: int


def is_probable_prime(n: int, rounds: int = 24) -> bool:
    """Miller-Rabin probable-prime test suitable for toy experiments."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small:
        if n == prime:
            return True
        if n % prime == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = 2 + randbelow(n - 3)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int) -> int:
    if bits < 8:
        raise ValueError("Use at least 8 bits for a toy prime.")
    while True:
        candidate = randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(candidate):
            return candidate


def generate_toy_key(bits: int = 32, e: int = 65537) -> ToyRSAKey:
    """Generate a small textbook RSA key for controlled experiments."""
    if bits < 16:
        raise ValueError("Use at least 16 bits for the modulus.")
    half = bits // 2
    while True:
        p = generate_prime(half)
        q = generate_prime(bits - half)
        if p == q:
            continue
        phi = (p - 1) * (q - 1)
        if gcd(e, phi) == 1:
            d = pow(e, -1, phi)
            return ToyRSAKey(p * q, e, d, p, q, phi)


def encrypt(message: int, n: int, e: int) -> int:
    if not 0 <= message < n:
        raise ValueError("Message must satisfy 0 <= message < n.")
    return pow(message, e, n)


def decrypt(ciphertext: int, key: ToyRSAKey) -> int:
    if not 0 <= ciphertext < key.n:
        raise ValueError("Ciphertext must satisfy 0 <= ciphertext < n.")
    return pow(ciphertext, key.d, key.n)


def validate_key(key: ToyRSAKey) -> bool:
    return (
        key.p * key.q == key.n
        and key.phi == (key.p - 1) * (key.q - 1)
        and (key.e * key.d) % key.phi == 1
    )
