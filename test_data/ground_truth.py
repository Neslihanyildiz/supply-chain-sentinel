# Ground truth test set: manually labeled package names.
# is_typosquat: True = bilerek bozulmuş/şüpheli isim, False = meşru paket

GROUND_TRUTH = [
    # Gerçek, meşru paketler (negatif örnekler)
    {"name": "requests", "is_typosquat": False},
    {"name": "flask", "is_typosquat": False},
    {"name": "django", "is_typosquat": False},
    {"name": "numpy", "is_typosquat": False},
    {"name": "pandas", "is_typosquat": False},
    {"name": "scipy", "is_typosquat": False},
    {"name": "pytest", "is_typosquat": False},
    {"name": "boto3", "is_typosquat": False},
    {"name": "sqlalchemy", "is_typosquat": False},
    {"name": "pillow", "is_typosquat": False},
    {"name": "cryptography", "is_typosquat": False},
    {"name": "banana", "is_typosquat": False},          # ilgisiz isim
    {"name": "my-internal-tool", "is_typosquat": False}, # şirket-içi paket simülasyonu

    # Bilinen typosquat teknikleri (pozitif örnekler)
    {"name": "reqeusts", "is_typosquat": True},   # harf yer değiştirme
    {"name": "reqeust", "is_typosquat": True},    # eksik harf
    {"name": "requestss", "is_typosquat": True},  # fazladan harf
    {"name": "flaskk", "is_typosquat": True},
    {"name": "djanga", "is_typosquat": True},
    {"name": "numpyy", "is_typosquat": True},
    {"name": "pandaas", "is_typosquat": True},
    {"name": "scipyy", "is_typosquat": True},
    {"name": "pytestt", "is_typosquat": True},
    {"name": "boto33", "is_typosquat": True},
    {"name": "expresss", "is_typosquat": True},   # gerçekten test ettiğimiz
    {"name": "pillowe", "is_typosquat": True},
    {"name": "crytography", "is_typosquat": True}, # harf sırası karışık
]