import Levenshtein

# En yaygın kullanılan paketlerden oluşan referans liste.
# Not: Bu liste elle seçilmiştir; gerçek bir üretim sisteminde
# PyPI'nin "top downloads" istatistiklerinden otomatik çekilebilir.
POPULAR_PACKAGES = [
    "requests", "flask", "django", "numpy", "pandas", "scipy",
    "matplotlib", "pytest", "boto3", "click", "pyyaml", "jinja2",
    "sqlalchemy", "urllib3", "certifi", "setuptools", "pip",
    "wheel", "six", "python-dateutil", "cryptography", "pillow",
    "beautifulsoup4", "lxml", "scikit-learn", "tensorflow",
    "torch", "fastapi", "uvicorn", "pydantic", "aiohttp",
    "redis", "celery", "gunicorn", "psycopg2", "pymongo",
    "docker", "kubernetes", "paramiko", "selenium", "scrapy",
    "nltk", "spacy", "openpyxl", "xlrd", "colorama", "tqdm",
    "attrs", "packaging", "typing-extensions",
    # npm ecosystem examples (demonstrates ecosystem-agnostic design)
    "express", "react", "lodash", "axios", "webpack", "vue",
]


def calculate_similarity(name, reference):
    """
    İki paket adı arasındaki Levenshtein mesafesini hesaplar.
    Mesafe ne kadar küçükse, isimler o kadar benzer demektir.
    """
    return Levenshtein.distance(name.lower(), reference.lower())


def check_typosquat(package_name, threshold=2):
    """
    Verilen paket adını popüler paket listesine karşı kontrol eder.
    threshold: kaç karakter farkına kadar 'şüpheli' sayılacağı.
    """
    package_name_lower = package_name.lower()

    # Eğer paket zaten popüler listedeyse, typosquat değildir
    if package_name_lower in POPULAR_PACKAGES:
        return {
            "is_suspicious": False,
            "reason": "Package is itself a well-known popular package.",
            "closest_match": None,
            "distance": None,
        }

    closest_match = None
    smallest_distance = float("inf")

    for popular in POPULAR_PACKAGES:
        distance = calculate_similarity(package_name_lower, popular)
        if distance < smallest_distance:
            smallest_distance = distance
            closest_match = popular

    if smallest_distance <= threshold and smallest_distance > 0:
        return {
            "is_suspicious": True,
            "reason": (
                f"I think this package is suspicious because its name "
                f"is very close to the popular package '{closest_match}' "
                f"(edit distance: {smallest_distance})."
            ),
            "closest_match": closest_match,
            "distance": smallest_distance,
        }

    return {
        "is_suspicious": False,
        "reason": "No close match to a popular package found.",
        "closest_match": closest_match,
        "distance": smallest_distance,
    }