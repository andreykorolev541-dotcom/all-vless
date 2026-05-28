# VLESS Reality Checker

Автоматически собирает VLESS конфиги из 20+ популярных репозиториев и Telegram-агрегаторов, проверяет каждый на доступность и сохраняет только рабочие. Обновляется каждые 6 часов без участия пользователя.

## Что это и зачем

Берёт по 150 конфигов из каждого источника, проверяет TCP/TLS подключение к каждому серверу и оставляет только те, что реально отвечают. Reality конфиги хранятся отдельно — они работают стабильнее в России.

## Файлы

| Файл | Описание |
|------|----------|
| configs/working_sub.txt | Все рабочие конфиги — base64 подписка |
| configs/working_reality_sub.txt | Только Reality — base64 подписка (рекомендуется) |
| configs/working_regular_sub.txt | Только обычные VLESS — base64 подписка |
| configs/working.txt | Все рабочие — plain text |
| configs/working_reality.txt | Только Reality — plain text |
| configs/working_regular.txt | Только обычные VLESS — plain text |
| configs/stats.json | Статистика последнего обновления |

## Ссылки для VPN-клиента

Все рабочие конфиги:
https://raw.githubusercontent.com/andreykorolev541-dotcom/vless/main/configs/working_sub.txt

Только Reality (рекомендуется для России):
https://raw.githubusercontent.com/andreykorolev541-dotcom/vless/main/configs/working_reality_sub.txt

## Как добавить подписку в клиент

### v2rayNG (Android)
Нижнее меню → Подписки → + → вставить ссылку → Обновить

### Hiddify (Android / iOS)
+ → Добавить профиль → вставить ссылку

### v2rayN (Windows)
Подписки → Настройки подписок → Добавить → вставить ссылку → Обновить

### Streisand (iOS)
Настройки → Импорт из URL → вставить ссылку

## Источники

- igareck/vpn-configs-for-russia — Reality белые списки для России
- soroushmirzaei/telegram-configs-collector — агрегатор 100+ Telegram каналов
- yebekhe/TelegramV2rayCollector — агрегатор Telegram каналов
- itsyebekhe/HiN-VPN
- barry-far/V2ray-Configs
- Epodonios/v2ray-configs
- peasoft/NoMoreVPN — Россия фокус
- mahdibland/V2RayAggregator
- и другие популярные агрегаторы

## Как устроено

Из каждого источника берётся случайная выборка до 150 VLESS конфигов. Затем к каждому серверу устанавливается TCP (или TLS) соединение — если сервер отвечает, конфиг считается рабочим. Reality конфиги сортируются по скорости ответа и идут первыми.

## Обновление

Автоматически каждые 6 часов через GitHub Actions.
Ручной запуск: Actions → Update Working Configs → Run workflow.

## Структура репозитория

scripts/
  check_configs.py       сбор, проверка и сохранение конфигов
.github/workflows/
  update-config.yml      автоматический запуск по расписанию
configs/
  working_sub.txt        результат (генерируется автоматически)
  working_reality_sub.txt
  stats.json
