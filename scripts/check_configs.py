#!/usr/bin/env python3
"""
Собирает VLESS конфиги из множества публичных источников,
проверяет каждый на доступность и сохраняет только рабочие.
"""
import base64, socket, ssl, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import json, os, time, re

# ── Источники ──────────────────────────────────────────────────────────────
# Публичные репозитории и подписки, из которых агрегаторы типа igareck
# собирают конфиги. Добавляй/убирай по желанию.
SOURCES = [
    # barry-far/V2ray-Configs
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Splitted-By-Protocol/vless.txt",
    # mahdibland/V2RayAggregator
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity.txt",
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity.txt",
    # yebekhe/TelegramV2rayCollector
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mix",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/vless",
    # mfuu/v2ray
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    # aiboboxx/v2rayfree
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    # freefq/free
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    # Pawdroid/Free-servers
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    # tbbatbb/Proxy
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config.txt",
    # peasoft/NoMoreVPN
    "https://raw.githubusercontent.com/peasoft/NoMoreVPN/master/subscriptions/raw.txt",
    # vveg26/chromego_merge
    "https://raw.githubusercontent.com/vveg26/chromego_merge/main/sub/merged_proxies_new.txt",
    # ALIILAPRO/v2ray
    "https://raw.githubusercontent.com/ALIILAPRO/v2ray/main/sub.txt",
    # w1770946460/v2ray_free_node
    "https://raw.githubusercontent.com/w1770946460/v2ray_free_node/main/sub",
    # ermaozi/get_subscribe
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    # ts-sf/v2ray
    "https://raw.githubusercontent.com/ts-sf/v2ray/main/v",
    # Leon406/SubCrawler
    "https://raw.githubusercontent.com/Leon406/SubCrawler/main/sub/share/vless",
    # ssrsub/ssr
    "https://raw.githubusercontent.com/ssrsub/ssr/master/V2Ray",
    # 1904240202/v2rayShare
    "https://raw.githubusercontent.com/1904240202/v2rayShare/main/v2ray",
]

OUTPUT_DIR = "configs"
TIMEOUT = 5
MAX_WORKERS = 100


def fetch_url(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  [WARN] {url.split('/')[-1]}: {e}")
        return ""


def decode_lines(text: str) -> list:
    text = text.strip()
    if not text:
        return []
    # Попробовать base64
    try:
        decoded = base64.b64decode(text + "==").decode("utf-8", errors="ignore")
        lines = [l.strip() for l in decoded.splitlines() if l.strip()]
        if any(l.startswith(("vless://", "vmess://", "trojan://", "ss://")) for l in lines):
            return lines
    except Exception:
        pass
    return [l.strip() for l in text.splitlines() if l.strip()]


def parse_vless(uri: str):
    try:
        without_scheme = uri[len("vless://"):]
        at_idx = without_scheme.rfind("@")
        if at_idx == -1:
            return None
        host_part = without_scheme[at_idx + 1:]
        for sep in ("?", "#", "/"):
            idx = host_part.find(sep)
            if idx != -1:
                host_part = host_part[:idx]
        if host_part.startswith("["):
            bracket = host_part.find("]")
            host = host_part[1:bracket]
            port_str = host_part[bracket + 2:]
        elif ":" in host_part:
            host, port_str = host_part.rsplit(":", 1)
        else:
            return None
        return host, int(port_str)
    except Exception:
        return None


def check_tcp(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=TIMEOUT):
            return True
    except Exception:
        return False


def check_tls(host: str, port: int) -> bool:
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((host, port), timeout=TIMEOUT) as sock:
            with ctx.wrap_socket(sock, server_hostname=host):
                return True
    except Exception:
        return False


def check_config(uri: str):
    parsed = parse_vless(uri)
    if not parsed:
        return uri, False, "parse_error"
    host, port = parsed
    if check_tcp(host, port):
        return uri, True, "tcp_ok"
    if check_tls(host, port):
        return uri, True, "tls_ok"
    return uri, False, "unreachable"


def is_reality(uri: str) -> bool:
    return "security=reality" in uri or "reality" in uri.lower()


def main():
    print(f"=== VLESS Config Checker | {len(SOURCES)} sources ===\n")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── 1. Сбор конфигов ──────────────────────────────────────────────────
    print(f"[1/3] Collecting configs from {len(SOURCES)} sources...")
    all_vless: set = set()

    for url in SOURCES:
        raw = fetch_url(url)
        if not raw:
            continue
        lines = decode_lines(raw)
        vless = [l for l in lines if l.startswith("vless://")]
        if vless:
            print(f"  +{len(vless):4d}  {url.split('github.com/')[-1][:60]}")
        all_vless.update(vless)

    configs = list(all_vless)
    reality_configs = [c for c in configs if is_reality(c)]
    regular_configs = [c for c in configs if not is_reality(c)]

    print(f"\n  Total unique VLESS : {len(configs)}")
    print(f"  Reality            : {len(reality_configs)}")
    print(f"  Regular            : {len(regular_configs)}\n")

    if not configs:
        print("No configs found. Exiting.")
        sys.exit(0)

    # ── 2. Проверка работоспособности ─────────────────────────────────────
    print(f"[2/3] Checking {len(configs)} configs (timeout={TIMEOUT}s, workers={MAX_WORKERS})...")
    working_reality, working_regular = [], []
    failed = errors = 0
    start = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_config, uri): uri for uri in configs}
        done = 0
        for future in as_completed(futures):
            done += 1
            uri, ok, reason = future.result()
            if ok:
                if is_reality(uri):
                    working_reality.append(uri)
                else:
                    working_regular.append(uri)
            elif reason == "parse_error":
                errors += 1
            else:
                failed += 1
            if done % 100 == 0 or done == len(configs):
                wr = len(working_reality)
                wg = len(working_regular)
                print(f"  {done}/{len(configs)} | Working: {wr + wg} (reality={wr}, regular={wg})")

    elapsed = round(time.time() - start, 1)
    all_working = working_reality + working_regular

    print(f"\n  Done in {elapsed}s | Working: {len(all_working)} / {len(configs)}")

    # ── 3. Сохранение ─────────────────────────────────────────────────────
    print(f"\n[3/3] Saving...")

    def save(filename: str, lines: list):
        path = f"{OUTPUT_DIR}/{filename}"
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n" if lines else "")
        print(f"  {filename}: {len(lines)} configs")

    def save_sub(filename: str, lines: list):
        if not lines:
            return
        encoded = base64.b64encode("\n".join(lines).encode()).decode()
        with open(f"{OUTPUT_DIR}/{filename}", "w") as f:
            f.write(encoded)
        print(f"  {filename}: base64 подписка ({len(lines)} configs)")

    # Все рабочие
    save("working.txt", all_working)
    save_sub("working_sub.txt", all_working)

    # Только Reality
    save("working_reality.txt", working_reality)
    save_sub("working_reality_sub.txt", working_reality)

    # Только обычные VLESS
    save("working_regular.txt", working_regular)
    save_sub("working_regular_sub.txt", working_regular)

    stats = {
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sources": len(SOURCES),
        "total_checked": len(configs),
        "working_total": len(all_working),
        "working_reality": len(working_reality),
        "working_regular": len(working_regular),
        "failed": failed,
        "parse_errors": errors,
        "elapsed_seconds": elapsed,
    }
    with open(f"{OUTPUT_DIR}/stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    print(f"\nDone. Stats saved to configs/stats.json")


if __name__ == "__main__":
    main()
