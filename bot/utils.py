def validate_symbol(symbol: str) -> str:
    if not symbol or not isinstance(symbol, str):
        raise ValueError("symbol must be a non-empty string, e.g. BTCUSDT")
    return symbol.strip().upper()


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in ("BUY", "SELL"):
        raise ValueError("side must be BUY or SELL")
    return s


def validate_type(tp: str) -> str:
    t = tp.strip().upper()
    if t not in ("MARKET", "LIMIT", "STOP"):
        raise ValueError("type must be MARKET, LIMIT, or STOP")
    return t


def validate_positive_number(name: str, value_str: str):
    try:
        v = float(value_str)
    except Exception:
        raise ValueError(f"{name} must be a number")
    if v <= 0:
        raise ValueError(f"{name} must be > 0")
    return v