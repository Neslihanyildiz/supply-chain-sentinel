import re


def parse_requirements(file_path):
    """
    requirements.txt dosyasını okur, her paketi
    {"name": ..., "operator": ..., "version": ...} formatında listeler.
    """
    packages = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Desteklenen versiyon operatörleri, uzundan kısaya sıralı
    # (>= önce gelmeli ki '=' onu yanlış yakalamasın)
    operator_pattern = r"(==|>=|<=|~=|!=|>|<)"

    for line in lines:
        line = line.strip()

        # boş satır veya yorum satırıysa atla
        if not line or line.startswith("#"):
            continue

        match = re.split(operator_pattern, line, maxsplit=1)

        if len(match) == 1:
            # versiyon belirtilmemiş, ör: "numpy"
            packages.append({
                "name": match[0].strip(),
                "operator": None,
                "version": None
            })
        else:
            # match = [paket_adi, operator, versiyon]
            name, operator, version = match
            packages.append({
                "name": name.strip(),
                "operator": operator,
                "version": version.strip()
            })

    return packages