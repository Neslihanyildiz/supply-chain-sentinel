import requests
import time


def get_package_metadata(package_name):
    """
    PyPI'nin resmi JSON API'sinden paket bilgisi çeker.
    Key gerektirmez, ücretsizdir.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        return {"name": package_name, "found": False, "error": str(e)}

    if response.status_code == 404:
        # Paket PyPI'de bulunamadı — bu önemli bir sinyal olabilir
        return {"name": package_name, "found": False, "error": "not found on PyPI"}

    if response.status_code != 200:
        return {"name": package_name, "found": False, "error": f"HTTP {response.status_code}"}

    data = response.json()
    info = data.get("info", {})
    releases = data.get("releases", {})

    # en eski ve en yeni yayın tarihini bul
    all_upload_times = []
    for version, files in releases.items():
        for file_info in files:
            if "upload_time" in file_info:
                all_upload_times.append(file_info["upload_time"])

    first_release = min(all_upload_times) if all_upload_times else None
    last_release = max(all_upload_times) if all_upload_times else None

    return {
        "name": package_name,
        "found": True,
        "latest_version": info.get("version"),
        "author": info.get("author"),
        "maintainer": info.get("maintainer"),
        "home_page": info.get("home_page"),
        "project_urls": info.get("project_urls"),
        "first_release": first_release,
        "last_release": last_release,
        "total_releases": len(releases),
    }


def collect_all_metadata(packages):
    """
    parser.py'den gelen paket listesini alır,
    her biri için PyPI'den metadata çeker.
    """
    results = []
    for pkg in packages:
        metadata = get_package_metadata(pkg["name"])
        results.append(metadata)
        time.sleep(0.3)  # PyPI'ye nazik davranmak için küçük bekleme
    return results