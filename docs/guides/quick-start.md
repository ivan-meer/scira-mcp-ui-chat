# 🚀 Быстрый старт

Это руководство поможет вам запустить MCP UI Playground Chat за 5 минут.

## Предварительные требования

- Node.js 18+ и pnpm
- Docker (для PostgreSQL и MCP серверов)
- API ключи от AI провайдеров

## Шаг 1: Клонирование и установка

```bash
git clone <repository-url>
cd scira-mcp-ui-chat
pnpm install
```

## Шаг 2: Настройка окружения

Создайте файл `.env.local`:

```env
# База данных
DATABASE_URL="postgresql://postgres:password@localhost:5432/postgres"

# AI провайдеры (добавьте свои ключи)
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
XAI_API_KEY=your_xai_key
GROQ_API_KEY=your_groq_key

# Daytona (для stdio MCP серверов)
DAYTONA_API_KEY=your_daytona_key
DAYTONA_API_URL="https://app.daytona.io/api"
```

## Шаг 3: Запуск базы данных

```bash
# Запуск PostgreSQL в Docker
docker run --name postgres-mcp \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=postgres \
  -p 5432:5432 \
  -d postgres:15

# Применение схемы базы данных
pnpm db:push
```

## Шаг 4: Запуск приложения

```bash
pnpm dev
```

Приложение будет доступно по адресу: http://localhost:3001

## Шаг 5: Добавление первого MCP сервера

1. Откройте http://localhost:3001
2. Нажмите на иконку настроек (⚙️) рядом с выбором модели
3. Добавьте демо сервер:
   - **Имя**: MCP Demo
   - **Тип**: SSE (Server-Sent Events)
   - **URL**: `https://remote-mcp-server-authless.idosalomon.workers.dev/sse`
4. Нажмите "Add Server"
5. Нажмите "Use" для активации

## Шаг 6: Тестирование

Напишите в чате:
```
Какие инструменты тебе доступны?
```

ИИ должен показать список доступных инструментов от MCP сервера.

## Что дальше?

- [Подключение собственных MCP серверов](mcp-servers.md)
- [Настройка stdio серверов](transport-types.md)
- [Устранение неполадок](../troubleshooting/common-issues.md)

## Частые проблемы при запуске

### База данных не подключается
```bash
# Проверьте статус контейнера
docker ps | grep postgres

# Перезапустите если нужно
docker restart postgres-mcp
```

### Порт 3000 занят
Приложение автоматически переключится на порт 3001.

### MCP сервер не отвечает
Проверьте логи в консоли браузера и терминале разработки.