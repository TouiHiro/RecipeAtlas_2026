
import json
import ijson

from pathlib import Path
from collections import defaultdict
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

BASE_DIR = Path(__file__).resolve().parent

SOURCE = BASE_DIR / "geo_data" / "N03-20260101.geojson"

OUTPUT = BASE_DIR / "map" / "static" / "map" / "geojson"

OUTPUT.mkdir(parents=True, exist_ok=True)

if not SOURCE.exists():
    raise FileNotFoundError(SOURCE)

regions = {}
geometries = defaultdict(list)

print("全国行政区域データの読み込み開始")

with SOURCE.open("rb") as f:

    features = ijson.items(
        f, "features.item", use_float=True
    )

    for i, feature in enumerate(features, 1):

        p = feature["properties"]

        code = str(p.get("N03_007") or "").strip()
        prefecture = p.get("N03_001") or ""
        city = p.get("N03_004") or ""
        ward = p.get("N03_005") or ""
        county = p.get("N03_003") or ""

        if not code or not city:
            continue

        name = city + ward

        if not feature.get("geometry"):
            continue

        geometry = shape(feature["geometry"])

        if geometry.is_empty:
            continue

        if not geometry.is_valid:
            geometry = geometry.buffer(0)

        if geometry.is_empty:
            continue

        # 境界座標を軽量化
        geometry = geometry.simplify(
            0.001,
            preserve_topology=True
        )

        regions[code] = {
            "code": code,
            "prefecture": prefecture,
            "name": name,
            "city": city,
            "ward": ward,
            "county": county,
            "prefecture_code": code[:2]
        }

        geometries[code].append(geometry)

        if i % 5000 == 0:
            print(f"{i:,}件読み込み完了")

print("地域別データを生成しています")

search_data = []
prefecture_data = defaultdict(list)

for code, region in regions.items():

    geometry = unary_union(geometries[code])

    if geometry.is_empty:
        continue

    center = geometry.representative_point()

    region["lat"] = round(center.y, 6)
    region["lng"] = round(center.x, 6)

    search_data.append(region)

    feature = {
        "type": "Feature",
        "properties": region,
        "geometry": mapping(geometry)
    }

    prefecture_data[code[:2]].append(feature)

# 全国検索用JSON
with (OUTPUT / "regions.json").open(
    "w", encoding="utf-8"
) as f:

    json.dump(
        search_data,
        f,
        ensure_ascii=False,
        separators=(",", ":")
    )

# 都道府県別GeoJSON
for code, features in prefecture_data.items():

    data = {
        "type": "FeatureCollection",
        "features": features
    }

    with (OUTPUT / f"{code}.geojson").open(
        "w", encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            separators=(",", ":")
        )

    print(f"{code}.geojson 作成完了")

print("==============================")
print("全国データの変換完了")
print(f"地域数: {len(search_data)}")
print(f"都道府県数: {len(prefecture_data)}")
print(f"保存先: {OUTPUT}")
print("==============================")
