#!/usr/bin/env python3
import os
import time
import json
import base64
import random
import requests

# ── Каждая база имеет основной линк и CDN-зеркало на случай блокировок ──
SOURCES_POOL = [
    {
        "name": "Igareck-Vless",
        "urls": [
            "https://raw.githubusercontent.com/igareck/vless/main/vless.txt",
            "https://cdn.jsdelivr.net/gh/igareck/vless@main/vless.txt"
        ]
    },
    {
        "name": "Mahdibland-Merge",
        "urls": [
            "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
            "https://cdn.jsdelivr.net/gh/mahdibland/V2RayAggregator@master/sub/sub_merge.txt"
        ]
    },
    {
        "name": "Yebekhe-TVC",
        "urls": [
            "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vless",
            "https://cdn.jsdelivr.net/gh/yebekhe/TVC@main/subscriptions/protocols/vless"
        ]
    }
]

OUTPUT_DIR = "configs"
MAX_CONFIGS = 200


def fetch_with_fallback(urls: list) -> str:
    """Пробует скачать файл по очереди из списка зеркал"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code == 200 and len(response.text.strip()) > 20:
                return response.text.strip()
        except Exception:
            continue
    return ""


def decode_base64(data: str) -> str:
    """Безопасное декодирование Base64 потока"""
    clean_data = "".join(data.split())
    missing_padding = len(clean_data) % 4
    if missing_padding:
        clean_data += '=' * (4 - missing_padding)
    try:
        return base64.b64decode(clean_data).decode('utf-8', errors='ignore')
    except Exception:
        return ""


def is_vless(line: str) -> bool:
    """Проверка на валидный синтаксик протокола VLESS"""
    line = line.strip()
    return line.startswith("vless://") and "@" in line


def extract_vless(text: str) -> list:
    """Построчный парсинг текстового блока"""
    found = []
    for line in text.splitlines():
        line = line.strip()
        if is_vless(line):
            found.append(line)
    return found


def main():
    print("=== СТАРТ УЛЬТИМАТИВНОГО ПАРСЕРА БАЗ ДАННЫХ ===")
    start_time = time.time()
    unique_configs = set()
    
    for source in SOURCES_POOL:
        name = source["name"]
        raw_data = fetch_with_fallback(source["urls"])
        
        if not raw_data:
            print(f"  [-] {name}: Не удалось загрузить ни с одного зеркала.")
            continue
            
        # Попытка 1: Читаем как обычный текст
        extracted = extract_vless(raw_data)
        
        # Попытка 2: Если пусто, пробуем декодировать из Base64
        if not extracted:
            decoded = decode_base64(raw_data)
            if decoded:
                extracted = extract_vless(decoded)
                
        if extracted:
            print(f"  [+] {name}: Успешно извлечено {len(extracted)} конфигураций.")
            unique_configs.update(extracted)
        else:
            print(f"  [-] {name}: Не найдено подходящих VLESS строк.")

    configs_list = list(unique_configs)
    print(f"\nВсего уникальных серверов найдено: {len(configs_list)}")

    # Ограничиваем выборку до 200 случайных серверов
    if len(configs_list) > MAX_CONFIGS:
        random.shuffle(configs_list)
        configs_list = configs_list[:MAX_CONFIGS]
        print(f"  [*] Применен лимит. Отобрано ровно {MAX_CONFIGS} серверов.")

    if not configs_list:
        configs_list = ["vless://00000000-0000-0000-0000-000000000000@127.0.0.1:443?encryption=none&security=tls#No_Configs_Found_Try_Again"]

    plain_content = "\n".join(sorted(configs_list)) + "\n"
    base64_content = base64.b64encode(plain_content.encode('utf-8')).decode('utf-8')

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(f"{OUTPUT_DIR}/vless_plain.txt", "w", encoding="utf-8") as f:
        f.write(plain_content)
        
    with open(f"{OUTPUT_DIR}/vless_base64.txt", "w", encoding="utf-8") as f:
        f.write(base64_content)

    stats = {
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_configs": len(configs_list),
        "elapsed_seconds": round(time.time() - start_time, 2)
    }
    
    with open(f"{OUTPUT_DIR}/stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print(f"Сохранение завершено! Итоговое количество: {len(configs_list)}")


if __name__ == "__main__":
    main()
    
