import argparse
import sys
from generator import (
    generate_password,
    estimate_entropy_bits,
    pool_size,
    classify_entropy,
)


def parse_args():
    p = argparse.ArgumentParser(description="Generator haseł")
    p.add_argument(
        "-l", "--length", type=int, default=12, help="Długość hasła (domyślnie 12)"
    )
    p.add_argument(
        "--no-upper", action="store_true", help="Wyłącz użycie wielkich liter"
    )
    p.add_argument("--no-digits", action="store_true", help="Wyłącz użycie cyfr")
    p.add_argument("--no-symbols", action="store_true", help="Wyłącz użycie symboli")
    p.add_argument(
        "--no-ambiguous",
        action="store_true",
        help="Wyklucz znaki mylące (l, 1, I, 0, O)",
    )
    p.add_argument(
        "--no-require",
        action="store_true",
        help="Nie wymusza obecności znaku z każdej włączonej kategorii",
    )
    p.add_argument(
        "--copy",
        action="store_true",
        help="Skopiuje wygenerowane hasło do schowka, jeśli pyperclip jest zainstalowany",
    )
    return p.parse_args()


def try_copy_to_clipboard(text):
    try:
        import pyperclip

        pyperclip.copy(text)
        return True
    except Exception:
        return False


def main():
    args = parse_args()
    try:
        password = generate_password(
            length=args.length,
            use_upper=not args.no_upper,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            use_ambiguous=not args.no_ambiguous,
            require_each_category=not args.no_require,
        )
    except ValueError as e:
        print(f"Błąd: {e}")
        sys.exit(1)

    # Wyliczam entropię i oceniam siłę
    psize = pool_size(
        use_upper=not args.no_upper,
        use_digits=not args.no_digits,
        use_symbols=not args.no_symbols,
        use_ambiguous=not args.no_ambiguous,
    )
    bits = estimate_entropy_bits(len(password), psize)
    strength = classify_entropy(bits)

    print(password)
    print(f"Entropia: {bits:.1f} bitów ({strength})")
    # większa entropia oznacza trudniejsze łamanie metodą brute‑force (każdy dodatkowy bit podwaja przestrzeń poszukiwań)")

    if args.copy:
        ok = try_copy_to_clipboard(password)
        if ok:
            print("Hasło skopiowane do schowka.")
        else:
            print(
                "Nie udało się skopiować do schowka (pyperclip może nie być zainstalowany)."
            )


if __name__ == "__main__":
    main()
