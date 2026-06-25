
import math
import secrets
import string
import random

AMBIGUOUS_CHARS = set("l1I0O")


def generate_password(
    length=12,
    use_upper=True,
    use_digits=True,
    use_symbols=True,
    use_ambiguous=True,
    require_each_category=True,
):
    """Generuję losowe hasło.
    Parametry:
    - length: długość hasła
    - use_upper/use_digits/use_symbols: informacja o tym czy włączam lub wyłączam kategorię
    - use_ambiguous: czy pozwalam na znaki łatwe do pomylenia
    - require_each_category: staram się zapewnić co najmniej 1 znak z każdej włączonej kategorii
    """

    if length < 1:
        raise ValueError("Długość hasła musi być większa niż 0")

    pools = []

    lower = set(string.ascii_lowercase)
    if not use_ambiguous:
        lower -= AMBIGUOUS_CHARS
    pools.append("".join(sorted(lower)))

    if use_upper:
        upper = set(string.ascii_uppercase)
        if not use_ambiguous:
            upper -= AMBIGUOUS_CHARS
        pools.append("".join(sorted(upper)))

    if use_digits:
        digits = set(string.digits)
        if not use_ambiguous:
            digits -= AMBIGUOUS_CHARS
        pools.append("".join(sorted(digits)))

    if use_symbols:
        symbols = set("!@#$%^&*()-_=+[]{};:,.<>/?")
        if not use_ambiguous:
            symbols -= AMBIGUOUS_CHARS
        pools.append("".join(sorted(symbols)))

    # Usuwam puste pule (np. gdy wszystkie znaki z danej puli były oznaczone jako mylące)
    pools = [p for p in pools if p]

    if not pools:
        raise ValueError("Brak dostępnych znaków do generowania hasła")

    combined = "".join(pools)

    password_chars = []
    if require_each_category and length >= len(pools):
        for pool in pools:
            password_chars.append(secrets.choice(pool))

    # Uzupełniam pozostałe znaki
    remaining = length - len(password_chars)
    for _ in range(remaining):
        password_chars.append(secrets.choice(combined))

    # Bezpieczne przemieszanie znaków, aby nie było przewidywalnego wzorca
    rng = random.SystemRandom()
    rng.shuffle(password_chars)

    return "".join(password_chars)


def estimate_entropy_bits(length, pool_size):
    # Oszacowuję entropię (w bitach) dla danego zbioru znaków i długości.
    if pool_size <= 1 or length <= 0:
        return 0.0
    return length * math.log2(pool_size)


def classify_entropy(bits):
    # Zwracam prostą etykietę siły hasła na podstawie entropii.
    if bits < 28:
        return "słabe"
    if bits < 36:
        return "średnie"
    if bits < 60:
        return "silne"
    return "bardzo silne"


def pool_size(use_upper=True, use_digits=True, use_symbols=True, use_ambiguous=True):
    # Zwracam przybliżony rozmiar puli znaków, której używam do generowania hasła.
    s = set(string.ascii_lowercase)
    if not use_ambiguous:
        s -= AMBIGUOUS_CHARS
    if use_upper:
        u = set(string.ascii_uppercase)
        if not use_ambiguous:
            u -= AMBIGUOUS_CHARS
        s |= u
    if use_digits:
        d = set(string.digits)
        if not use_ambiguous:
            d -= AMBIGUOUS_CHARS
        s |= d
    if use_symbols:
        sy = set("!@#$%^&*()-_=+[]{};:,.<>/?")
        if not use_ambiguous:
            sy -= AMBIGUOUS_CHARS
        s |= sy
    return len(s)
