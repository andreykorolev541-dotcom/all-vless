#!/usr/bin/env python3
import os
import time
import json
import base64
import random
import re
import requests

GITHUB_SOURCES = [
    {
        "name": "barry-far",
        "urls": ["https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt"]
    },
    {
        "name": "soroushmirzaei",
        "urls": ["https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless"]
    },
    {
        "name": "mahdibland",
        "urls": ["https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge_vless.txt"]
    },
    {
        "name": "mfuu",
        "urls": ["https://raw.githubusercontent.com/mfuu/v2ray/master/vless.txt"]
    },
    {
        "name": "yebekhe",
        "urls": ["https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vless"]
    },
    {
        "name": "Epodonios",
        "urls": ["https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Configs/vless.txt"]
    },
    {
        "name": "peasoft",
        "urls": ["https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt"]
    },
    {
        "name": "awesome-vpn",
        "urls": ["https://raw.githubusercontent.com/awesome-vpn/awesome-vpn/master/all"]
    },
    # Эти репо специально агрегируют из Telegram каналов
    {
        "name": "vless-reality-ezpz",
        "urls": ["https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/sub.txt"]
    },
    {
        "name": "rxn957",
        "urls": ["https://raw.githubusercontent.com/rxn957/rxn957/main/vless.txt"]
    },
    {
        "name": "HW7X-vless",
        "urls": ["https://raw.githubusercontent.com/HW7X/vless-config/main/vless.txt"]
    },
    {
        "name": "vpei",
        "urls": ["https://raw.githubusercontent.com/vpei/Free-Node-Merge/main/o/node.txt"]
    },
    {
        "name": "tbbatbb",
        "urls": ["https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config.txt"]
    },
    {
        "name": "lagzian-ss-collector",
        "urls": ["https://raw.githubusercontent.com/lagzian/SS-Collector/main/VLESS/vless.txt"]
    },
    {
        "name": "lagzian-reality",
        "urls": ["https://raw.githubusercontent.com/lagzian/SS-Collector/main/VLESS/reality.txt"]
    },
]

OUTPUT_DIR = "configs"
MAX_CONFIGS = 200


def fetch(urls: list) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200 and len(r.text.strip()) > 20:
                print(f"    OK: {url}")
                return r.text.strip()
            else:
                print(f"    FAIL {r.status_code}: {url}")
        except Exception as e:
            print(f"    ERROR: {url} — {e}")
    return ""


def decode_base64(data: str) -> str:
    clean = "".join(data.split())
    clean += '=' * (-len(clean) % 4)
    try:
        return base64.b64decode(clean).decode('utf-8', errors='ignore')
    except Exception:
        return ""


def extract_vless(text: str) -> list:
    result = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("vless://") and "@" in line:
            result.append(line)
    # Также ищем через regex на случай если слитно
    found = re.findall(r'vless://[A-Za-z0-9\-]+@[^\s\'"<>&\n]+', text)
    for cfg in found:
        cfg = cfg.replace("&amp;", "&")
        if cfg not in result:
            result.append(cfg)
    return result


def main():
    print("=== СТАРТ ===")
    start = time.time()
    unique = set()

    print("\n── GitHub источники ──")
    for source in GITHUB_SOURCES:
        name = source["name"]
        print(f"\n[{name}]")
        raw = fetch(source["urls"])

        if not raw:
            print(f"  Пропущен — не загрузился")
            continue

        extracted = extract_vless(raw)

        if not extracted:
            decoded = decode_base64(raw)
            if decoded:
                extracted = extract_vless(decoded)

        if extracted:
            print(f"  Найдено: {len(extracted)} конфигов")
            unique.update(extracted)
        else:
            print(f"  VLESS строк не найдено")

    configs = list(unique)
    print(f"\nВсего уникальных: {len(configs)}")

    if len(configs) > MAX_CONFIGS:
        random.shuffle(configs)
        configs = configs[:MAX_CONFIGS]
        print(f"Обрезано до {MAX_CONFIGS}")

    if not configs:
        configs = ["vless://00000000-0000-0000-0000-000000000000@127.0.0.1:443?encryption=none&security=tls#No_Configs_Found"]

    plain = "\n".join(sorted(configs)) + "\n"
    b64 = base64.b64encode(plain.encode()).decode()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(f"{OUTPUT_DIR}/vless_plain.txt", "w") as f:
        f.write(plain)
    with open(f"{OUTPUT_DIR}/vless_base64.txt", "w") as f:
        f.write(b64)

    stats = {
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_configs": len(configs),
        "elapsed_seconds": round(time.time() - start, 2)
    }
    with open(f"{OUTPUT_DIR}/stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    print(f"\nГотово! Сохранено: {len(configs)} конфигов")


if __name__ == "__main__":
    main()
