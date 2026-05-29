# VLESS Subscription Aggregator

Автоматический сборщик VLESS-конфигураций из популярных Telegram-каналов и GitHub-агрегаторов. Упор на Россию и обход РКН. Обновляется каждые 6 часов. Каждый файл ~70KB — оптимально для Hiddify, v2rayNG, Nekobox.

---

## 🔗 Подписки

### Все конфиги (рекомендуется)

https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_base64.txt

### Только REALITY — лучший обход РКН/DPI

https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_reality_base64.txt

### Только российские серверы

https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_russia_base64.txt

### Только IPv6

https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_ipv6_base64.txt

> Plain-text версии: замените `_base64.txt` на `_plain.txt`

---

## 📱 Как добавить

**Hiddify:** + → Добавить подписку по URL → вставить ссылку → Сохранить → обновить.

**v2rayNG:** ☰ → Subscription group → + → вставить ссылку → OK → ☰ → Update subscription.

**Nekobox:** Profiles → New group → Subscription → вставить ссылку → Update.

---

## 📦 Источники

### Популярные Telegram-каналы

| Канал | Описание |
|-------|----------|
| @igareck | Игорь Ецкало — один из самых известных в РФ |
| @vpnKeys | Крупнейший русский канал с ключами |
| @freevpnkeys | Популярный русский канал |
| @vpn_fail | Новости и ключи для обхода блокировок |
| @antiblock_soft | Обход блокировок РФ |
| @vlessfree | VLESS конфиги |
| @v2rayng_configs | Большой пул конфигов |
| @v2ray_configs_pool | Один из крупнейших пулов |
| @outline_keysss | Outline/VLESS ключи |
| @iP_CF | Cloudflare IP — стабильно работает в РФ |
| @DirectVPN | Прямые конфиги |
| @ConfigsHUB | Агрегатор каналов |
| @proxy_mtn | Активный канал |

### GitHub

| Репозиторий | Описание |
|-------------|----------|
| soroushmirzaei/telegram-configs-collector | Парсит 100+ TG-каналов, есть срез по России |
| Surfboardv2ray/Proxy-sorter | Сортировка по странам, Россия отдельно |
| barry-far/V2ray-Configs | ~15k звёзд, один из старейших |
| MrMohebi/xray-proxy-grabber-telegram | Прямой парсинг Telegram |
| mahdibland/V2RayAggregator | Крупный merger |
| yebekhe/TVC | Telegram Configs, активен годами |
| coldwater-10/V2rayCollector | REALITY + Россия |
| lagzian/SS-Collector | REALITY и IPv6 |

---

## 🔄 Автоматизация

По расписанию — каждые 6 часов. Вручную — Actions → *Update Working Configs* → **Run workflow**.

---

## 📊 Статистика

https://raw.githubusercontent.com/Rageru01/white-list/main/configs/stats.json
