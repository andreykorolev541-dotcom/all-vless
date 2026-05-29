#!/usr/bin/env python3
import os
import time
import json
import base64
import random
import re
import requests

# ══════════════════════════════════════════════════════════════════
#  ИСТОЧНИКИ
#  Приоритет: Россия → REALITY/TLS → крупные агрегаторы → IPv6
# ══════════════════════════════════════════════════════════════════
SOURCES = [

    # ── 🇷🇺 Россия и СНГ (специфичные источники) ──
    {
        "name": "soroushmirzaei-russia-vless",
        "urls": ["https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ru/vless"]
    },
    {
        "name": "soroushmirzaei-russia-mixed",
        "urls": ["https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ru/mixed"]
    },
    {
        "name": "yebekhe-russia",
        "urls": ["https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/countries/ru/mix"]
    },
    {
        "name": "mahdibland-russia",
        "urls": ["https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/splitted/vless.txt"]
    },
    {
        "name": "coldwater-russia",
        "urls": [
            "https://raw.githubusercontent.com/coldwater-10/V2Hub/main/Russia",
            "https://raw.githubusercontent.com/coldwater-10/V2rayCollector/main/vless_russia.txt"
        ]
    },
    {
        "name": "Surfboardv2ray-russia",
        "urls": ["https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/Russia/Vless.txt"]
    },
    {
        "name": "Surfboardv2ray-russia-reality",
        "urls": ["https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/Russia/Reality.txt"]
    },
    {
        "name": "v2rayse-russia",
        "urls": ["https://raw.githubusercontent.com/v2rayse/node-list/main/data/ru.txt"]
    },
    {
        "name": "vakhov-russia",
        "urls": [
            "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/vless.txt",
            "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/proxylist.txt"
        ]
    },

    # ── ✨ REALITY конфиги (лучший обход DPI) ──
    {
        "name": "soroushmirzaei-reality",
        "urls": ["https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/splitted/reality"]
    },
    {
        "name": "lagzian-reality",
        "urls": ["https://raw.githubusercontent.com/lagzian/SS-Collector/main/VLESS/reality.txt"]
    },
    {
        "name": "coldwater-reality",
        "urls": ["https://raw.githubusercontent.com/coldwater-10/V2rayCollector/main/vless_reality.txt"]
    },
    {
        "name": "Surfboardv2ray-reality",
        "urls": ["https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/Reality/Vless.txt"]
    },
    {
        "name": "mahdibland-reality",
        "urls": ["https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/splitted/reality.txt"]
    },
    {
        "name": "yebekhe-reality",
        "urls": ["https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/reality"]
    },
    {
        "name": "SoliSpirit-reality",
        "urls": ["https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/reality.txt"]
    },
    {
        "name": "MatinKh98-reality",
        "urls": ["https://raw.githubusercontent.com/MatinKh98/v2ray-subscribe/main/subscribe/reality.txt"]
    },

    # ── 🌐 IPv6 источники ──
    {
        "name": "soroushmirzaei-ipv6",
        "urls": ["https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/splitted/ipv6"]
    },
    {
        "name": "lagzian-ipv6",
        "urls": ["https://raw.githubusercontent.com/lagzian/SS-Collector/main/VLESS/ipv6.txt"]
    },
    {
        "name": "Surfboardv2ray-ipv6",
        "urls": ["https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/IPv6/Vless.txt"]
    },
    {
        "name": "mahdibland-ipv6",
        "urls": ["https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/splitted/ipv6.txt"]
    },
    {
        "name": "yebekhe-ipv6",
        "urls": ["https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/splitted/ipv6"]
    },

    # ── 📦 Крупные агрегаторы ──
    {
        "name": "barry-far-all",
        "urls": ["https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt"]
    },
    {
        "name": "barry-far-sub6",
        "urls": ["https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub6.txt"]
    },
    {
        "name": "barry-far-sub7",
        "urls": ["https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub7.txt"]
    },
    {
        "name": "soroushmirzaei-vless",
        "urls": ["https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless"]
    },
    {
        "name": "mahdibland-vless",
        "urls": ["https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge_vless.txt"]
    },
    {
        "name": "mahdibland-all",
        "urls": ["https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt"]
    },
    {
        "name": "yebekhe-vless",
        "urls": ["https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vless"]
    },
    {
        "name": "Surfboardv2ray-vless",
        "urls": ["https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/vless.txt"]
    },
    {
        "name": "SoliSpirit-vless",
        "urls": ["https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/vless.txt"]
    },
    {
        "name": "MrMohebi-vless",
        "urls": ["https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/vless.txt"]
    },
    {
        "name": "Epodonios-vless",
        "urls": ["https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Configs/vless.txt"]
    },
    {
        "name": "lagzian-vless",
        "urls": ["https://raw.githubusercontent.com/lagzian/SS-Collector/main/VLESS/vless.txt"]
    },
    {
        "name": "coldwater-vless",
        "urls": ["https://raw.githubusercontent.com/coldwater-10/V2rayCollector/main/vless.txt"]
    },
    {
        "name": "ALIILAPRO",
        "urls": ["https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/sub.txt"]
    },
    {
        "name": "mfuu-vless",
        "urls": ["https://raw.githubusercontent.com/mfuu/v2ray/master/vless.txt"]
    },
    {
        "name": "arshiacomplus",
        "urls": ["https://raw.githubusercontent.com/arshiacomplus/v2rayExtractor/main/vless.txt"]
    },
    {
        "name": "awesome-vpn",
        "urls": ["https://raw.githubusercontent.com/awesome-vpn/awesome-vpn/master/all"]
    },
    {
        "name": "IranianCypherpunks",
        "urls": ["https://raw.githubusercontent.com/IranianCypherpunks/sub/main/vlessconfig"]
    },
    {
        "name": "MatinKh98-vless",
        "urls": ["https://raw.githubusercontent.com/MatinKh98/v2ray-subscribe/main/subscribe/vless.txt"]
    },
    {
        "name": "mheidari98-vless",
        "urls": ["https://raw.githubusercontent.com/mheidari98/.proxy/main/vless"]
    },
    {
        "name": "saeeddev94-vless",
        "urls": ["https://raw.githubusercontent.com/saeeddev94/xray-boot/master/vless.txt"]
    },
    {
        "name": "roosterkid-vless",
        "urls": ["https://raw.githubusercontent.com/roosterkid/openproxylist/main/VLESS_RAW.txt"]
    },
    {
        "name": "ermaozi-vless",
        "urls": ["https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/vless.txt"]
    },
    {
        "name": "Leon406-vless",
        "urls": ["https://raw.githubusercontent.com/Leon406/SubCrawler/main/sub/share/vless"]
    },
    {
        "name": "resasanian-vless",
        "urls": ["https://raw.githubusercontent.com/resasanian/Mirza/main/vless.txt"]
    },
    {
        "name": "peasoft",
        "urls": ["https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt"]
    },
    {
        "name": "freefq",
        "urls": ["https://raw.githubusercontent.com/freefq/free/master/v2"]
    },
    {
        "name": "vpei",
        "urls": ["https://raw.githubusercontent.com/vpei/Free-Node-Merge/main/o/node.txt"]
    },
    {
        "name": "aiboboxx-vless",
        "urls": ["https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2"]
    },
    {
        "name": "HW7X-vless",
        "urls": ["https://raw.githubusercontent.com/HW7X/vless-config/main/vless.txt"]
    },
    {
        "name": "rxn957",
        "urls": ["https://raw.githubusercontent.com/rxn957/rxn957/main/vless.txt"]
    },
    {
        "name": "w1770938096",
        "urls": ["https://raw.githubusercontent.com/w1770938096/proxy/main/vless.txt"]
    },
    {
        "name": "Pawdroid-vless",
        "urls": ["https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub"]
    },
    {
        "name": "tbbatbb",
        "urls": ["https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config.txt"]
    },
    {
        "name": "zhangkaiitugithub",
        "urls": ["https://raw.githubusercontent.com/zhangkaiitugithub/passcro/main/speednodes.yaml"]
    },
    {
        "name": "w1770938096-b",
        "urls": ["https://raw.githubusercontent.com/w1770938096/proxy/main/sub6.txt"]
    },
    {
        "name": "Proxifly-russia",
        "urls": [
            "https://raw.githubusercontent.com/Proxifly/free-proxy-list/main/proxies/protocols/vless/data.txt",
            "https://raw.githubusercontent.com/Proxifly/free-proxy-list/main/proxies/countries/RU/data.txt"
        ]
    },
    {
        "name": "hookzof-russia",
        "urls": ["https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"]
    },
    {
        "name": "abshare-vless",
        "urls": [
            "https://raw.githubusercontent.com/abshare/abshare.github.io/main/README.md",
            "https://raw.githubusercontent.com/abshare/abshare.github.io/main/sub.txt"
        ]
    },
    {
        "name": "WilliamStar-vless",
        "urls": ["https://raw.githubusercontent.com/WilliamStar007/ClashX-V2Ray-TopFreeProxy/main/combine/vlesssub.txt"]
    },
    {
        "name": "liketolivefree-vless",
        "urls": ["https://raw.githubusercontent.com/liketolivefree/kobabi/main/vless.txt"]
    },
    {
        "name": "proxypool-vless",
        "urls": [
            "https://raw.githubusercontent.com/a2470982985/getNode/main/v2ray.txt",
            "https://raw.githubusercontent.com/Barabama/FreeNodes/master/nodes/v2rayse.txt"
        ]
    },
]

OUTPUT_DIR = "configs"
MAX_CONFIGS = 1000  # увеличено для лучшего покрытия


def fetch(urls: list) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=25)
            if r.status_code == 200 and len(r.text.strip()) > 20:
                print(f"    OK  [{r.status_code}]: {url}")
                return r.text.strip()
            else:
                print(f"    FAIL [{r.status_code}]: {url}")
        except Exception as e:
            print(f"    ERR: {url} — {e}")
    return ""


def decode_base64(data: str) -> str:
    clean = "".join(data.split())
    clean += "=" * (-len(clean) % 4)
    try:
        return base64.b64decode(clean).decode("utf-8", errors="ignore")
    except Exception:
        return ""


def is_ipv6(cfg: str) -> bool:
    return bool(re.search(r"@\[([0-9a-fA-F:]+)\]", cfg))


def extract_vless(text: str) -> list:
    seen: set = set()
    result: list = []

    # 1) строки vless://
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("vless://") and "@" in line:
            line = line.replace("&amp;", "&")
            if line not in seen:
                seen.add(line)
                result.append(line)

    # 2) вложенные в текст (yaml, json, html)
    for cfg in re.findall(r"vless://[A-Za-z0-9\-]+@[^\s'\",<>&\n]+", text):
        cfg = cfg.replace("&amp;", "&")
        # убираем мусорные символы в хвосте
        cfg = re.sub(r"[)\]}'\"]+$", "", cfg)
        if cfg not in seen and "@" in cfg:
            seen.add(cfg)
            result.append(cfg)

    return result


def tag_source(configs: list, source_name: str) -> list:
    """Добавляем метку источника в fragment (#...) если её нет."""
    tagged = []
    for cfg in configs:
        if "#" not in cfg:
            cfg = f"{cfg}#{source_name}"
        tagged.append(cfg)
    return tagged


def main():
    print("=== СТАРТ СБОРКИ ===")
    start = time.time()

    all_configs: set = set()
    russia_configs: set = set()
    reality_configs: set = set()
    ipv6_configs: set = set()

    source_stats: dict = {}

    print(f"\nВсего источников: {len(SOURCES)}\n")
    print("── Загрузка ──")

    for source in SOURCES:
        name = source["name"]
        print(f"\n[{name}]")
        raw = fetch(source["urls"])

        if not raw:
            source_stats[name] = 0
            print("  Пропущен")
            continue

        extracted = extract_vless(raw)

        if not extracted:
            decoded = decode_base64(raw)
            if decoded:
                extracted = extract_vless(decoded)

        if not extracted:
            source_stats[name] = 0
            print("  VLESS не найдено")
            continue

        extracted = tag_source(extracted, name)

        ipv6_found  = [c for c in extracted if is_ipv6(c)]
        ipv4_found  = [c for c in extracted if not is_ipv6(c)]
        real_found  = [c for c in extracted if "reality" in c.lower() or "Reality" in c]
        ru_found    = [c for c in extracted if "russia" in name.lower() or "ru" in name.lower()]

        print(f"  Найдено: {len(extracted)}  "
              f"(IPv4={len(ipv4_found)}, IPv6={len(ipv6_found)}, REALITY={len(real_found)})")

        source_stats[name] = len(extracted)
        all_configs.update(extracted)
        ipv6_configs.update(ipv6_found)
        reality_configs.update(real_found)
        russia_configs.update(ru_found)

    configs     = list(all_configs)
    ipv6_list   = list(ipv6_configs)
    reality_list = list(reality_configs)
    russia_list  = list(russia_configs)

    print(f"\n─────────────────────────────")
    print(f"Всего уникальных : {len(configs)}")
    print(f"Из них IPv6      : {len(ipv6_list)}")
    print(f"Из них REALITY   : {len(reality_list)}")
    print(f"Россия/СНГ       : {len(russia_list)}")
    print(f"─────────────────────────────")

    # ── Отбор ──
    # Квоты: Россия+REALITY — приоритет, потом IPv6, потом прочие
    if len(configs) > MAX_CONFIGS:
        ru_quota      = min(len(russia_list),  MAX_CONFIGS // 4)
        reality_quota = min(len(reality_list), MAX_CONFIGS // 4)
        ipv6_quota    = min(len(ipv6_list),    MAX_CONFIGS // 6)
        other_quota   = MAX_CONFIGS - ru_quota - reality_quota - ipv6_quota

        others = [c for c in configs
                  if c not in russia_configs and c not in reality_configs and c not in ipv6_configs]

        random.shuffle(russia_list)
        random.shuffle(reality_list)
        random.shuffle(ipv6_list)
        random.shuffle(others)

        configs = (
            russia_list[:ru_quota] +
            reality_list[:reality_quota] +
            ipv6_list[:ipv6_quota] +
            others[:other_quota]
        )
        random.shuffle(configs)
        print(f"Обрезано до {MAX_CONFIGS} "
              f"(RU={ru_quota}, REALITY={reality_quota}, IPv6={ipv6_quota}, other={other_quota})")

    if not configs:
        configs = [
            "vless://00000000-0000-0000-0000-000000000000@127.0.0.1:443"
            "?encryption=none&security=tls#No_Configs_Found"
        ]

    # ── Запись файлов ──
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Единая подписка (plain + base64) — сюда вставляете в клиент
    plain = "\n".join(configs) + "\n"
    b64   = base64.b64encode(plain.encode()).decode()

    _w(f"{OUTPUT_DIR}/vless_plain.txt",  plain)
    _w(f"{OUTPUT_DIR}/vless_base64.txt", b64)

    # IPv6 отдельно
    if ipv6_list:
        ipv6_plain = "\n".join(ipv6_list) + "\n"
        _w(f"{OUTPUT_DIR}/vless_ipv6_plain.txt",  ipv6_plain)
        _w(f"{OUTPUT_DIR}/vless_ipv6_base64.txt", base64.b64encode(ipv6_plain.encode()).decode())
    else:
        open(f"{OUTPUT_DIR}/vless_ipv6_plain.txt",  "w").close()
        open(f"{OUTPUT_DIR}/vless_ipv6_base64.txt", "w").close()

    # REALITY отдельно
    if reality_list:
        real_plain = "\n".join(reality_list) + "\n"
        _w(f"{OUTPUT_DIR}/vless_reality_plain.txt",  real_plain)
        _w(f"{OUTPUT_DIR}/vless_reality_base64.txt", base64.b64encode(real_plain.encode()).decode())
    else:
        open(f"{OUTPUT_DIR}/vless_reality_plain.txt",  "w").close()
        open(f"{OUTPUT_DIR}/vless_reality_base64.txt", "w").close()

    # Россия отдельно
    if russia_list:
        ru_plain = "\n".join(russia_list) + "\n"
        _w(f"{OUTPUT_DIR}/vless_russia_plain.txt",  ru_plain)
        _w(f"{OUTPUT_DIR}/vless_russia_base64.txt", base64.b64encode(ru_plain.encode()).decode())
    else:
        open(f"{OUTPUT_DIR}/vless_russia_plain.txt",  "w").close()
        open(f"{OUTPUT_DIR}/vless_russia_base64.txt", "w").close()

    # Статистика
    stats = {
        "last_updated":    time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_configs":   len(configs),
        "ipv6_configs":    len(ipv6_list),
        "reality_configs": len(reality_list),
        "russia_configs":  len(russia_list),
        "ipv4_configs":    len([c for c in configs if not is_ipv6(c)]),
        "elapsed_seconds": round(time.time() - start, 2),
        "sources":         source_stats,
    }
    _w(f"{OUTPUT_DIR}/stats.json", json.dumps(stats, indent=2, ensure_ascii=False))

    print(f"\nГотово! Сохранено {len(configs)} конфигов за {stats['elapsed_seconds']}с")
    print(f"\nФайлы в папке {OUTPUT_DIR}/:")
    print("  vless_plain.txt          ← вставить как URL подписки (raw)")
    print("  vless_base64.txt         ← вставить как base64 подписку")
    print("  vless_russia_base64.txt  ← только российские серверы")
    print("  vless_reality_base64.txt ← только REALITY (лучший обход DPI)")
    print("  vless_ipv6_base64.txt    ← только IPv6")


def _w(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Записан: {path}")


if __name__ == "__main__":
    main()
