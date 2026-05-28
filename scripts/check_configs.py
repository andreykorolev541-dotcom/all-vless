#!/usr/bin/env python3
import urllib.request, os, time, json, random, re

# ── CIDR источники ─────────────────────────────────────────────────────────

# Платформенные IP (VK Cloud, Яндекс, Mail.ru и др.) — Ground-Zerro/DomainMapper
PLATFORM_CIDR = [
    ("VK / ВКонтакте [IP]",
     "https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/main/platforms/ip-vkontakte.txt"),
    ("Яндекс [IP]",
     "https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/main/platforms/ip-yandex.txt"),
    ("Mail.ru / MAX [IP]",
     "https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/main/platforms/ip-mailru.txt"),
    ("Сбер [IP]",
     "https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/main/platforms/ip-sber.txt"),
    ("Тинькофф [IP]",
     "https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/main/platforms/ip-tinkoff.txt"),
    ("Госуслуги [IP]",
     "https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/main/platforms/ip-gosuslugi.txt"),
    ("Одноклассники [IP]",
     "https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/main/platforms/ip-odnoklassniki.txt"),
]

# Сводные российские CIDR списки
AGGREGATE_CIDR = [
    ("igareck [CIDR RU all]",
     "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-all.txt"),
    ("igareck [CIDR RU checked — VK/YA/CDN/Beeline]",
     "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-checked.txt"),
    ("antifilter.download [IP list]",
     "https://community.antifilter.download/list/ip.lst"),
    ("antifilter.download [summarized]",
     "https://community.antifilter.download/list/summarized.lst"),
    ("1andrevich Re-filter-lists [ipsets all]",
     "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ipsets_all.lst"),
    ("zhongfly runet-ip [CIDR RU]",
     "https://raw.githubusercontent.com/zhongfly/runet-ip/main/russia-cidr.txt"),
    ("ipverse [RU IPv4 aggregated]",
     "https://raw.githubusercontent.com/ipverse/rir-ip/master/country/ru/ipv4-aggregated.txt"),
    ("nicklvsa russia-blocked [CIDR]",
     "https://raw.githubusercontent.com/nicklvsa/russia-blocked/main/russia.cidr"),
    ("Ground-Zerro DomainMapper [all RU IP]",
     "https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/main/russia-ip.txt"),
]

CIDR_SOURCES = PLATFORM_CIDR + AGGREGATE_CIDR

# ── SNI источники ──────────────────────────────────────────────────────────
SNI_SOURCES = [
    ("igareck [SNI RU all]",
     "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-SNI-RU-all.txt"),
    ("antifilter.download [domains]",
     "https://community.antifilter.download/list/domains.lst"),
    ("1andrevich Re-filter-lists [domains all]",
     "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/domains_all.lst"),
    ("1andrevich Re-filter-lists [domains lite]",
     "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/lists/domains_lite.lst"),
    ("Ground-Zerro DomainMapper [VK domains]",
     "https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/main/platforms/dns-vkontakte.txt"),
    ("Ground-Zerro DomainMapper [Яндекс domains]",
     "https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/main/platforms/dns-yandex.txt"),
    ("Ground-Zerro DomainMapper [Mail.ru domains]",
     "https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/main/platforms/dns-mailru.txt"),
    ("dartraiden no-Russia-hosts",
     "https://raw.githubusercontent.com/dartraiden/no-Russia-hosts/master/hosts.txt"),
    ("nicklvsa russia-blocked [domains]",
     "https://raw.githubusercontent.com/nicklvsa/russia-blocked/main/russia-domains.txt"),
]

OUTPUT_DIR = "configs"
PER_SOURCE = 500   # для CIDR/SNI можно больше — это не серверы


def fetch(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  [WARN] {url.split('/')[-1][:50]}: {e}")
        return ""


def is_cidr(line: str) -> bool:
    return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}(/\d{1,2})?$", line.strip()))


def is_domain(line: str) -> bool:
    line = line.strip().lstrip(".")
    return bool(re.match(r"^(?!\-)([a-zA-Z0-9\-]{1,63}\.)+[a-zA-Z]{2,}$", line)) \
           and not line.startswith("#")


def collect_cidr(sources: list) -> set:
    result = set()
    for name, url in sources:
        raw = fetch(url)
        if not raw:
            continue
        items = [l.strip() for l in raw.splitlines() if is_cidr(l)]
        if not items:
            print(f"  +    0  {name}")
            continue
        if len(items) > PER_SOURCE:
            items = random.sample(items, PER_SOURCE)
        print(f"  +{len(items):5d}  {name}")
        result.update(items)
    return result


def collect_sni(sources: list) -> set:
    result = set()
    for name, url in sources:
        raw = fetch(url)
        if not raw:
            continue
        items = []
        for l in raw.splitlines():
            l = l.strip().lstrip("*.").lower()
            if not l or l.startswith("#"):
                continue
            parts = l.split()
            candidate = parts[-1] if len(parts) > 1 else l
            if is_domain(candidate):
                items.append(candidate)
        if not items:
            print(f"  +    0  {name}")
            continue
        if len(items) > PER_SOURCE:
            items = random.sample(items, PER_SOURCE)
        print(f"  +{len(items):5d}  {name}")
        result.update(items)
    return result


def save(filename: str, items: set) -> int:
    lines = sorted(items)
    with open(f"{OUTPUT_DIR}/{filename}", "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Сохранено: {filename} — {len(lines)} записей")
    return len(lines)


def main():
    print(f"=== CIDR + SNI Collector ===\n")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    start = time.time()

    print(f"[1/2] Сбор CIDR ({len(CIDR_SOURCES)} источников)...")
    cidr = collect_cidr(CIDR_SOURCES)
    print(f"\n  Итого уникальных CIDR: {len(cidr)}\n")

    print(f"[2/2] Сбор SNI/доменов ({len(SNI_SOURCES)} источников)...")
    sni = collect_sni(SNI_SOURCES)
    print(f"\n  Итого уникальных доменов: {len(sni)}\n")

    print("Сохранение...")
    n_cidr = save("CIDR-RU-all.txt", cidr)
    n_sni  = save("SNI-RU-all.txt",  sni)

    stats = {
        "last_updated":    time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cidr_sources":    len(CIDR_SOURCES),
        "sni_sources":     len(SNI_SOURCES),
        "per_source":      PER_SOURCE,
        "cidr_total":      n_cidr,
        "sni_total":       n_sni,
        "elapsed_seconds": round(time.time() - start, 1),
    }
    with open(f"{OUTPUT_DIR}/stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    print(f"\nГотово. CIDR: {n_cidr}, SNI: {n_sni}")


if __name__ == "__main__":
    main()
