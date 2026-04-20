import os
from dotenv import load_dotenv
load_dotenv()

def get_env(name: str, default=None, required: bool = False):
    value = os.getenv(name, default)
    if required and (value is None or value == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

def get_int(name: str, default: int) -> int:
    return int(get_env(name, str(default)))

def get_float(name: str, default: float) -> float:
    return float(get_env(name, str(default)))
