from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.output.json import JsonV1Dot5
import uuid


def generate_sbom(packages, metadata_list, output_path="sbom.json"):
    """
    Taranan paket listesinden CycloneDX formatında bir SBOM üretir.

    packages: parser.py'den gelen [{"name": ..., "version": ...}, ...]
    metadata_list: metadata_collector.py'den gelen paket bilgileri (PyPI'den
                    çekilen gerçek/latest versiyon bilgisi için kullanılır)
    """
    bom = Bom()

    # metadata_list'i isimle erişilebilir hale getir (hızlı arama için)
    metadata_by_name = {m["name"]: m for m in metadata_list}

    for pkg in packages:
        name = pkg["name"]
        # requirements.txt'te belirtilen versiyon varsa onu kullan,
        # yoksa PyPI'den çektiğimiz en güncel versiyonu kullan
        version = pkg.get("version")
        if not version and name in metadata_by_name:
            version = metadata_by_name[name].get("latest_version")

        component = Component(
            name=name,
            version=version or "unknown",
            type=ComponentType.LIBRARY,
        )
        bom.components.add(component)

    # JSON formatında (CycloneDX v1.5) serialize et
    json_output = JsonV1Dot5(bom)
    serialized = json_output.output_as_string()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(serialized)

    return output_path