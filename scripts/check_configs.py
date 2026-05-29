#!/usr/bin/env python3
"""
VLESS Config Aggregator
Собирает из GitHub-зеркал Telegram-каналов и крупных агрегаторов.
Приоритет: REALITY > Россия > IPv6 > остальные.
Каждый выходной файл ограничен TARGET_KB килобайт.
"""
import os, time, json, base64, random, re
import requests

SOURCES = [
    {   "name": "soroushmirzaei-vless",
        "urls": ["https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless"],
        "priority": 10 },
    {   "name": "soroushmirzaei-reality",
        "urls": ["https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/splitted/reality"],
        "priority": 10, "tags": ["reality"] },
    {   "name": "soroushmirzaei-ipv6",
        "urls": ["https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/splitted/ipv6"],
        "priority": 9, "tags": ["ipv6"] },
    {   "name": "soroushmirzaei-russia",
        "urls": [
            "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ru/vless",
            "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ru/mixed",
        ],
        "priority": 10, "tags": ["russia"] },
    {   "name": "MrMohebi-vless",
        "urls": ["https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/vless.txt"],
        "priority": 9 },
    {   "name": "MrMohebi-all",
        "urls": ["https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/all.txt"],
        "priority": 9 },
    {   "name": "Surfboardv2ray-tgparse",
        "urls": ["https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/vless.txt"],
        "priority": 9 },
    {   "name": "Surfboardv2ray-russia",
        "urls": [
            "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/Russia/Vless.txt",
            "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/Russia/Reality.txt",
        ],
        "priority": 9, "tags": ["russia"] },
    {   "name": "Surfboardv2ray-reality",
        "urls": ["https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/Reality/Vless.txt"],
        "priority": 9, "tags": ["reality"] },
    {   "name": "Surfboardv2ray-ipv6",
        "urls": ["https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/IPv6/Vless.txt"],
        "priority": 8, "tags": ["ipv6"] },
    {   "name": "yebekhe-vless",
        "urls": ["https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vless"],
        "priority": 9 },
    {   "name": "yebekhe-reality",
        "urls": ["https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/reality"],
        "priority": 9, "tags": ["reality"] },
    {   "name": "yebekhe-russia",
        "urls": ["https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/countries/ru/mix"],
        "priority": 9, "tags": ["russia"] },
    {   "name": "yebekhe-ipv6",
        "urls": ["https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/splitted/ipv6"],
        "priority": 8, "tags": ["ipv6"] },
    {   "name": "Epodonios-vless",
        "urls": ["https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Configs/vless.txt"],
        "priority": 8 },
    {   "name": "Epodonios-all",
        "urls": ["https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Configs/All_Configs_Sub.txt"],
        "priority": 8 },
    {   "name": "barry-far-all",
        "urls": ["https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt"],
        "priority": 8 },
    {   "name": "barry-far-sub6",
        "urls": ["https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub6.txt"],
        "priority": 8 },
    {   "name": "barry-far-sub7",
        "urls": ["https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub7.txt"],
        "priority": 8 },
    {   "name": "mahdibland-vless",
        "urls": ["https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge_vless.txt"],
        "priority": 8 },
    {   "name": "mahdibland-reality",
        "urls": ["https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/splitted/reality.txt"],
        "priority": 8, "tags": ["reality"] },
    {   "name": "mahdibland-ipv6",
        "urls": ["https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/splitted/ipv6.txt"],
        "priority": 7, "tags": ["ipv6"] },
    {   "name": "lagzian-reality",
        "urls": ["https://raw.githubusercontent.com/lagzian/SS-Collector/main/VLESS/reality.txt"],
        "priority": 9, "tags": ["reality"] },
    {   "name": "lagzian-vless",
        "urls": ["https://raw.githubusercontent.com/lagzian/SS-Collector/main/VLESS/vless.txt"],
        "priority": 8 },
    {   "name": "lagzian-ipv6",
        "urls": ["https://raw.githubusercontent.com/lagzian/SS-Collector/main/VLESS/ipv6.txt"],
        "priority": 8, "tags": ["ipv6"] },
    {   "name": "coldwater-reality",
        "urls": ["https://raw.githubusercontent.com/coldwater-10/V2rayCollector/main/vless_reality.txt"],
        "priority": 9, "tags": ["reality"] },
    {   "name": "coldwater-vless",
        "urls": ["https://raw.githubusercontent.com/coldwater-10/V2rayCollector/main/vless.txt"],
        "priority": 8 },
    {   "name": "coldwater-russia",
        "urls": [
            "https://raw.githubusercontent.com/coldwater-10/V2Hub/main/Russia",
            "https://raw.githubusercontent.com/coldwater-10/V2rayCollector/main/vless_russia.txt",
        ],
        "priority": 9, "tags": ["russia"] },
    {   "name": "SoliSpirit-reality",
        "urls": ["https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/reality.txt"],
        "priority": 8, "tags": ["reality"] },
    {   "name": "SoliSpirit-vless",
        "urls": ["https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/vless.txt"],
        "priority": 7 },
    {   "name": "MatinKh98-reality",
        "urls": ["https://raw.githubusercontent.com/MatinKh98/v2ray-subscribe/main/subscribe/reality.txt"],
        "priority": 8, "tags": ["reality"] },
    {   "name": "MatinKh98-vless",
        "urls": ["https://raw.githubusercontent.com/MatinKh98/v2ray-subscribe/main/subscribe/vless.txt"],
        "priority": 7 },
    {   "name": "ALIILAPRO-sub",
        "urls": ["https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/sub.txt"],
        "priority": 8 },
    {   "name": "v2rayse-russia",
        "urls": ["https://raw.githubusercontent.com/v2rayse/node-list/main/data/ru.txt"],
        "priority": 8, "tags": ["russia"] },
    {   "name": "Proxifly-russia",
        "urls": [
            "https://raw.githubusercontent.com/Proxifly/free-proxy-list/main/proxies/countries/RU/data.txt",
            "https://raw.githubusercontent.com/Proxifly/free-proxy-list/main/proxies/protocols/vless/data.txt",
        ],
        "priority": 8, "tags": ["russia"] },
    {   "name": "vakhov-ru",
        "urls": ["https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/vless.txt"],
        "priority": 7, "tags": ["russia"] },
    {   "name": "mheidari98-vless",
        "urls": ["https://raw.githubusercontent.com/mheidari98/.proxy/main/vless"],
        "priority": 7 },
    {   "name": "saeeddev94-vless",
        "urls": ["https://raw.githubusercontent.com/saeeddev94/xray-boot/master/vless.txt"],
        "priority": 7 },
    {   "name": "mfuu-vless",
        "urls": ["https://raw.githubusercontent.com/mfuu/v2ray/master/vless.txt"],
        "priority": 7 },
    {   "name": "ermaozi-vless",
        "urls": ["https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/vless.txt"],
        "priority": 7 },
    {   "name": "Leon406-vless",
        "urls": ["https://raw.githubusercontent.com/Leon406/SubCrawler/main/sub/share/vless"],
        "priority": 7 },
    {   "name": "arshiacomplus-vless",
        "urls": ["https://raw.githubusercontent.com/arshiacomplus/v2rayExtractor/main/vless.txt"],
        "priority": 7 },
    {   "name": "resasanian-vless",
        "urls": ["https://raw.githubusercontent.com/resasanian/Mirza/main/vless.txt"],
        "priority": 7 },
    {   "name": "IranianCypherpunks",
        "urls": ["https://raw.githubusercontent.com/IranianCypherpunks/sub/main/vlessconfig"],
        "priority": 7 },
    {   "name": "awesome-vpn",
        "urls": ["https://raw.githubusercontent.com/awesome-vpn/awesome-vpn/master/all"],
        "priority": 6 },
    {   "name": "freefq",
        "urls": ["https://raw.githubusercontent.com/freefq/free/master/v2"],
        "priority": 6 },
    {   "name": "peasoft",
        "urls": ["https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt"],
        "priority": 6 },
    {   "name": "vpei",
        "urls": ["https://raw.githubusercontent.com/vpei/Free-Node-Merge/main/o/node.txt"],
        "priority": 6 },
    {   "name": "aiboboxx",
        "urls": ["https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2"],
        "priority": 6 },
    {   "name": "roosterkid-vless",
        "urls": ["https://raw.githubusercontent.com/roosterkid/openproxylist/main/VLESS_RAW.txt"],
        "priority": 6 },
    {   "name": "WilliamStar-vless",
        "urls": ["https://raw.githubusercontent.com/WilliamStar007/ClashX-V2Ray-TopFreeProxy/main/combine/vlesssub.txt"],
        "priority": 6 },
    {   "name": "liketolivefree-vless",
        "urls": ["https://raw.githubusercontent.com/liketolivefree/kobabi/main/vless.txt"],
        "priority": 6 },
    {   "name": "a2470982985-nodes",
        "urls": ["https://raw.githubusercontent.com/a2470982985/getNode/main/v2ray.txt"],
        "priority": 5 },
    {   "name": "Barabama-v2rayse",
        "urls": ["https://raw.githubusercontent.com/Barabama/FreeNodes/master/nodes/v2rayse.txt"],
        "priority": 5 },
    {   "name": "tbbatbb",
        "urls": ["https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config.txt"],
        "priority": 5 },
    {   "name": "Pawdroid",
        "urls": ["https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub"],
        "priority": 5 },
    {   "name": "HW7X-vless",
        "urls": ["https://raw.githubusercontent.com/HW7X/vless-config/main/vless.txt"],
        "priority": 5 },
    {   "name": "w1770938096",
        "urls": [
            "https://raw.githubusercontent.com/w1770938096/proxy/main/vless.txt",
            "https://raw.githubusercontent.com/w1770938096/proxy/main/sub6.txt",
        ],
        "priority": 5 },
    {   "name": "rxn957",
        "urls": ["https://raw.githubusercontent.com/rxn957/rxn957/main/vless.txt"],
        "priority": 5 },
    # ── Публичные Telegram-каналы ──
    {   "name": "tg-v2ray_configs_pool",
        "urls": ["https://t.me/s/v2ray_configs_pool"],
        "priority": 9, "tg": True },
    {   "name": "tg-VlessConfig",
        "urls": ["https://t.me/s/VlessConfig"],
        "priority": 9, "tg": True },
    {   "name": "tg-proxy_mtn",
        "urls": ["https://t.me/s/proxy_mtn"],
        "priority": 8, "tg": True },
    {   "name": "tg-DirectVPN",
        "urls": ["https://t.me/s/DirectVPN"],
        "priority": 8, "tg": True },
    {   "name": "tg-freev2rayssr",
        "urls": ["https://t.me/s/freev2rayssr"],
        "priority": 8, "tg": True },
    {   "name": "tg-FreeV2rays",
        "urls": ["https://t.me/s/FreeV2rays"],
        "priority": 8, "tg": True },
    {   "name": "tg-V2rayFarsi",
        "urls": ["https://t.me/s/V2rayFarsi"],
        "priority": 8, "tg": True },
    {   "name": "tg-iP_CF",
        "urls": ["https://t.me/s/iP_CF"],
        "priority": 8, "tg": True },
    {   "name": "tg-ConfigsHUB",
        "urls": ["https://t.me/s/ConfigsHUB"],
        "priority": 8, "tg": True },
    {   "name": "tg-PrivateVPNs",
        "urls": ["https://t.me/s/PrivateVPNs"],
        "priority": 8, "tg": True },
    {   "name": "tg-ShadowsocksM",
        "urls": ["https://t.me/s/ShadowsocksM"],
        "priority": 7, "tg": True },
    {   "name": "tg-vless_vmess_v2rayng",
        "urls": ["https://t.me/s/vless_vmess_v2rayng"],
        "priority": 8, "tg": True },
    {   "name": "tg-v2ray_outlinekey",
        "urls": ["https://t.me/s/v2ray_outlinekey"],
        "priority": 7, "tg": True },
    {   "name": "tg-vmessiran",
        "urls": ["https://t.me/s/vmessiran"],
        "priority": 7, "tg": True },
    {   "name": "tg-proxystore11",
        "urls": ["https://t.me/s/proxystore11"],
        "priority": 7, "tg": True },
]

OUTPUT_DIR   = "configs"
TARGET_KB    = 52        # plain ~52KB → base64 ~70KB
TARGET_BYTES = TARGET_KB * 1024

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
}
TG_HEADERS = {
    **HEADERS,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
}


def fetch(urls: list, is_tg: bool = False) -> str:
    hdrs = TG_HEADERS if is_tg else HEADERS
    for url in urls:
        for attempt in range(2):
            try:
                r = requests.get(url, headers=hdrs, timeout=25)
                if r.status_code == 200 and len(r.text.strip()) > 20:
                    print(f"    OK  [{r.status_code}]: {url}")
                    return r.text.strip()
                else:
                    print(f"    FAIL [{r.status_code}]: {url}")
                    break
            except requests.exceptions.Timeout:
                print(f"    TIMEOUT (попытка {attempt + 1}): {url}")
            except Exception as e:
                print(f"    ERR: {url} — {e}")
                break
    return ""


def decode_b64(data: str) -> str:
    clean = "".join(data.split())
    clean += "=" * (-len(clean) % 4)
    try:
        return base64.b64decode(clean).decode("utf-8", errors="ignore")
    except Exception:
        return ""


def is_ipv6(cfg: str) -> bool:
    return bool(re.search(r"@\[([0-9a-fA-F:]+)\]", cfg))


def is_reality(cfg: str) -> bool:
    return "security=reality" in cfg.lower() or "reality" in cfg.lower()


def config_fingerprint(cfg: str) -> str:
    m = re.match(r"vless://([^@]+)@([^?#\s]+)", cfg)
    if m:
        return f"{m.group(1)}@{m.group(2)}"
    return cfg


def extract_vless(text: str) -> list:
    seen_fp: set = set()
    result:  list = []
    candidates: list = []

    for line in text.splitlines():
        line = line.strip()
        if line.startswith("vless://") and "@" in line:
            candidates.append(line.replace("&amp;", "&"))

    for m in re.finditer(r"vless://[A-Za-z0-9\-]{8,}@[^\s'\",<>&\n]{10,}", text):
        c = m.group(0).replace("&amp;", "&")
        c = re.sub(r"[)\]}'\"\\]+$", "", c)
        candidates.append(c)

    for cfg in candidates:
        if "@" not in cfg:
            continue
        fp = config_fingerprint(cfg)
        if fp not in seen_fp:
            seen_fp.add(fp)
            result.append(cfg)

    return result


def sanitize_tag(label: str) -> str:
    """Только безопасные символы в #фрагменте URL."""
    label = re.sub(r"^tg-", "TG_", label)
    label = re.sub(r"[^A-Za-z0-9._\-]", "_", label)
    return label[:50]


def tag(cfg: str, source_name: str) -> str:
    if "#" not in cfg:
        return f"{cfg}#{sanitize_tag(source_name)}"
    base, frag = cfg.rsplit("#", 1)
    frag_clean = re.sub(r"[^A-Za-z0-9._\-\u0400-\u04FF ]", "", frag).strip()
    return f"{base}#{frag_clean}" if frag_clean else base


def trim_to_size(configs: list, max_bytes: int) -> list:
    result = []
    total  = 0
    for cfg in configs:
        line_bytes = len((cfg + "\n").encode("utf-8"))
        if total + line_bytes > max_bytes:
            break
        result.append(cfg)
        total += line_bytes
    return result


def save(filename: str, configs_list: list) -> int:
    configs_list = trim_to_size(configs_list, TARGET_BYTES)
    # Финальная проверка: только валидные vless:// строки без пробелов
    clean = [c.strip() for c in configs_list
             if c.strip().startswith("vless://") and "@" in c and " " not in c.split("#")[0]]
    if not clean:
        open(f"{OUTPUT_DIR}/{filename}_plain.txt",  "w").close()
        open(f"{OUTPUT_DIR}/{filename}_base64.txt", "w").close()
        return 0
    plain = "\n".join(clean) + "\n"
    b64   = base64.b64encode(plain.encode("utf-8")).decode("utf-8")
    with open(f"{OUTPUT_DIR}/{filename}_plain.txt",  "w", encoding="utf-8") as f:
        f.write(plain)
    with open(f"{OUTPUT_DIR}/{filename}_base64.txt", "w", encoding="utf-8") as f:
        f.write(b64)
    plain_kb = len(plain.encode()) / 1024
    b64_kb   = len(b64.encode())   / 1024
    print(f"  {filename}: {len(clean)} конфигов  "
          f"(plain={plain_kb:.1f}KB, base64={b64_kb:.1f}KB)")
    return len(clean)


def main():
    print("=" * 60)
    print("  VLESS CONFIG AGGREGATOR")
    print(f"  Лимит: ~{TARGET_KB}KB plain / ~{int(TARGET_KB * 4 / 3)}KB base64 на файл")
    print("=" * 60)
    start = time.time()

    all_fps:      set  = set()
    all_configs:  list = []
    russia_set:   set  = set()
    reality_set:  set  = set()
    ipv6_set:     set  = set()
    source_stats: dict = {}

    sorted_sources = sorted(SOURCES, key=lambda s: s.get("priority", 5), reverse=True)
    print(f"\nИсточников: {len(sorted_sources)}\n")

    for src in sorted_sources:
        name  = src["name"]
        is_tg = src.get("tg", False)
        tags  = src.get("tags", [])
        print(f"\n[{name}]")

        raw = fetch(src["urls"], is_tg=is_tg)
        if not raw:
            source_stats[name] = 0
            print("  — пропущен")
            continue

        extracted = extract_vless(raw)
        if not extracted:
            decoded = decode_b64(raw)
            if decoded:
                extracted = extract_vless(decoded)

        if not extracted:
            source_stats[name] = 0
            print("  — vless не найдено")
            continue

        added = 0
        for cfg in extracted:
            fp = config_fingerprint(cfg)
            if fp in all_fps:
                continue
            all_fps.add(fp)
            cfg = tag(cfg, name)
            all_configs.append(cfg)
            added += 1

            if is_ipv6(cfg)    or "ipv6"    in tags: ipv6_set.add(cfg)
            if is_reality(cfg) or "reality" in tags: reality_set.add(cfg)
            if "russia" in tags or "russia" in name.lower():
                russia_set.add(cfg)

        source_stats[name] = added
        print(f"  Добавлено: {added}  "
              f"(IPv6={sum(1 for c in extracted if is_ipv6(c))}, "
              f"REALITY={sum(1 for c in extracted if is_reality(c))})")

    print(f"\n{'─' * 40}")
    print(f"Уникальных итого : {len(all_configs)}")
    print(f"  REALITY        : {len(reality_set)}")
    print(f"  Россия         : {len(russia_set)}")
    print(f"  IPv6           : {len(ipv6_set)}")
    print(f"{'─' * 40}")

    reality_list = list(reality_set)
    russia_list  = list(russia_set - reality_set)
    ipv6_list    = list(ipv6_set - reality_set - russia_set)
    others       = [c for c in all_configs
                    if c not in reality_set and c not in russia_set and c not in ipv6_set]

    for lst in [reality_list, russia_list, ipv6_list, others]:
        random.shuffle(lst)

    ordered_all = reality_list + russia_list + ipv6_list + others

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\nЗапись файлов в {OUTPUT_DIR}/")

    n_all     = save("vless",         ordered_all)
    n_reality = save("vless_reality", reality_list)
    n_russia  = save("vless_russia",  russia_list)
    n_ipv6    = save("vless_ipv6",    ipv6_list)

    stats = {
        "last_updated":    time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_configs":   n_all,
        "reality_configs": n_reality,
        "russia_configs":  n_russia,
        "ipv6_configs":    n_ipv6,
        "ipv4_configs":    len([c for c in ordered_all[:n_all] if not is_ipv6(c)]),
        "target_kb":       TARGET_KB,
        "elapsed_seconds": round(time.time() - start, 2),
        "sources":         source_stats,
    }
    with open(f"{OUTPUT_DIR}/stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"\nГотово за {stats['elapsed_seconds']}с")
    print(f"\nПодписки:")
    print(f"  Все      → configs/vless_base64.txt          ({n_all} конфигов)")
    print(f"  REALITY  → configs/vless_reality_base64.txt  ({n_reality} конфигов)")
    print(f"  Россия   → configs/vless_russia_base64.txt   ({n_russia} конфигов)")
    print(f"  IPv6     → configs/vless_ipv6_base64.txt     ({n_ipv6} конфигов)")


if __name__ == "__main__":
    main()
