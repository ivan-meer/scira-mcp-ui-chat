# 🔧 Отладка MCP серверов

Пошаговое руководство по диагностике и решению проблем с MCP серверами.

## 🚨 Основные проблемы и решения

### Проблема: ИИ не видит инструменты MCP сервера

**ИСПРАВЛЕНО в коде:**
- Добавлен `useMemo` для реактивности `mcpServersForApi`
- Исправлена передача серверов в Chat API

**Симптомы:**
- Сервер показывает статус "connected" ✅
- В логах видно: `MCP tools from https://server-url: ['tool1', 'tool2']`
- Но ИИ отвечает: "У меня нет доступных инструментов"

**Диагностика:**

1. **Проверьте активацию сервера:**
```javascript
// В консоли браузера (F12)
console.log('Selected servers:', JSON.parse(localStorage.getItem('selected-mcp-servers') || '[]'));
console.log('All servers:', JSON.parse(localStorage.getItem('mcp-servers') || '[]'));
```

2. **Проверьте передачу в API:**
```javascript
// Network tab -> POST /api/chat -> Request Payload
// Должно содержать:
{
  "mcpServers": [
    {
      "type": "sse",
      "url": "https://server-url/sse"
    }
  ]
}
```

3. **Проверьте логи инициализации:**
```bash
# В терминале разработки должно быть:
"MCP tools from https://server-url/sse: ['get_tasks_status', 'show_task_status']"
```

**Решение:**
1. Убедитесь что сервер активирован (галочка "Use")
2. Перезагрузите страницу после активации
3. Если проблема остается - очистите localStorage:
```javascript
localStorage.removeItem('mcp-servers');
localStorage.removeItem('selected-mcp-servers');
// Добавьте серверы заново
```

### Проблема: Чаты не сохраняются

**ИСПРАВЛЕНО в коде:**
- Добавлено сохранение в `onFinish` callback
- Включена загрузка истории чатов
- Исправлен драйвер базы данных

**Симптомы:**
- Сообщения отправляются и отвечают
- При перезагрузке чаты исчезают
- Ошибки в API `/api/chats`

**Диагностика:**

1. **Проверьте статус PostgreSQL:**
```bash
docker ps | grep postgres
# Должно показать: Up X minutes
```

2. **Проверьте API чатов:**
```bash
curl -H "x-user-id: test-user" http://localhost:3001/api/chats
# Должно вернуть: [] или список чатов
```

3. **Проверьте логи сохранения:**
```bash
# В терминале разработки ищите:
"Chat saved with ID: chat-id-here"
```

**Решение:**
1. Перезапустите PostgreSQL: `docker restart postgres`
2. Проверьте переменные окружения в `.env.local`
3. Примените схему БД: `pnpm db:push`

## 🔍 Пошаговая диагностика

### Шаг 1: Проверка базовой настройки

```bash
# 1. Статус приложения
curl -I http://localhost:3001
# Ожидаем: 200 OK

# 2. Статус базы данных
docker ps | grep postgres
# Ожидаем: Up X minutes

# 3. Подключение к базе
docker exec postgres psql -U postgres -c "SELECT 1;"
# Ожидаем: (1 row)

# 4. Проверка схемы
docker exec postgres psql -U postgres -c "\d chats;"
# Ожидаем: таблица с колонками id, user_id, title, created_at, updated_at
```

### Шаг 2: Проверка MCP серверов

```javascript
// В консоли браузера (F12)

// 1. Все серверы
const allServers = JSON.parse(localStorage.getItem('mcp-servers') || '[]');
console.log('All servers:', allServers);

// 2. Активные серверы
const selectedServers = JSON.parse(localStorage.getItem('selected-mcp-servers') || '[]');
console.log('Selected servers:', selectedServers);

// 3. Статус серверов
allServers.forEach(server => {
  console.log(`${server.name}: ${server.status}`);
});
```

### Шаг 3: Проверка API запросов

**В DevTools Network tab:**

1. **POST /api/chat:**
```json
// Request должен содержать:
{
  "messages": [...],
  "mcpServers": [
    {
      "type": "sse",
      "url": "https://server-url/sse",
      "headers": []
    }
  ],
  "selectedModel": "claude-3-5-sonnet-20241022",
  "chatId": "chat-id",
  "userId": "user-id"
}
```

2. **GET /api/chats:**
```javascript
// Headers должны содержать:
{
  "x-user-id": "user-id-here"
}
```

### Шаг 4: Проверка логов

**В терминале разработки ищите:**

```bash
# Успешная инициализация MCP
"MCP tools from https://server-url/sse: ['tool1', 'tool2']"

# Сохранение чата
"Chat saved with ID: chat-id"

# Ошибки подключения
"Failed to initialize MCP client: Error details"
"Error saving chat: Error details"
```

**В консоли браузера ищите:**

```javascript
// Ошибки загрузки
"Error loading chat history: Error details"

// Ошибки MCP
"Error fetching chats: Error details"
```

## 🛠️ Решение конкретных ошибок

### "502 Bad Gateway" от MCP сервера

**Причина:** Sandbox создался, но сервис внутри недоступен

**Проверка:**
```bash
# Для stdio серверов проверьте команду
# Вместо:
docker run alpine/socat STDIO TCP:host.docker.internal:8811

# Должно быть:
docker run -i --rm alpine/socat STDIO TCP:host.docker.internal:8811
```

**Решение:**
1. Проверьте что сервис на указанном порту работает
2. Убедитесь в корректности команды для stdio
3. Для тестирования используйте SSE сервер

### "Error: connect ECONNREFUSED 127.0.0.1:5432"

**Причина:** PostgreSQL не запущен

**Решение:**
```bash
# Проверьте статус
docker ps -a | grep postgres

# Запустите если остановлен
docker start postgres

# Создайте новый если нужно
docker run --name postgres-mcp \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -d postgres:15
```

### "API key or JWT token is required"

**Причина:** Отсутствует Daytona API ключ

**Решение:**
```bash
# Добавьте в .env.local:
echo 'DAYTONA_API_KEY=your_key_here' >> .env.local
echo 'DAYTONA_API_URL="https://app.daytona.io/api"' >> .env.local

# Перезапустите сервер
pnpm dev
```

### "Failed to load chat history"

**Причина:** Проблема с загрузкой истории

**Решение:**
```javascript
// Очистите cache React Query
// В консоли браузера:
window.location.reload();

// Или очистите localStorage:
localStorage.clear();
```

## 📊 Мониторинг и метрики

### Важные логи для отслеживания

**Успешная работа:**
```bash
# MCP серверы
"MCP tools from https://server-url/sse: ['tool1', 'tool2', 'tool3']"
"Sandbox created for server-id, URL: https://sandbox-url/sse"

# Сохранение чатов
"Chat saved with ID: chat-id-123"

# Статус серверов
"servers [ { id: 'server-id', status: 'connected' } ]"
```

**Проблемы:**
```bash
# Ошибки MCP
"Failed to initialize MCP client: 502 Bad Gateway"
"Error starting MCP sandbox: Timeout"

# Ошибки БД
"Error saving chat: connect ECONNREFUSED"
"Error fetching chats: Invalid user ID"

# Ошибки состояния
"Server failed to become ready after 20 attempts"
```

### Команды для диагностики

```bash
# Полный статус системы
echo "=== Application Status ==="
curl -I http://localhost:3001

echo "=== Database Status ==="
docker ps | grep postgres

echo "=== Database Connection ==="
docker exec postgres psql -U postgres -c "SELECT COUNT(*) FROM chats;"

echo "=== API Status ==="
curl -H "x-user-id: test" http://localhost:3001/api/chats

echo "=== Environment ==="
cat .env.local | grep -v "API_KEY"
```

## 🆘 Экстренное восстановление

### Полный перезапуск системы

```bash
#!/bin/bash
echo "Stopping all services..."
docker stop postgres 2>/dev/null || true
pkill -f "next dev" 2>/dev/null || true

echo "Cleaning up..."
docker start postgres || docker run --name postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -d postgres:15

echo "Waiting for database..."
sleep 5

echo "Applying database schema..."
pnpm db:push

echo "Starting application..."
pnpm dev
```

### Сброс MCP серверов

```javascript
// В консоли браузера
localStorage.removeItem('mcp-servers');
localStorage.removeItem('selected-mcp-servers');
console.log('MCP servers cleared. Reload page and add servers again.');
```

### Сброс базы данных

```bash
# ВНИМАНИЕ: Удаляет ВСЕ данные!
docker exec postgres psql -U postgres -c "DROP TABLE IF EXISTS messages, chats CASCADE;"
pnpm db:push
echo "Database reset completed."
```

## 📋 Чеклист диагностики

Перед обращением за помощью проверьте:

**Базовая система:**
- [ ] PostgreSQL запущен (`docker ps | grep postgres`)
- [ ] Приложение отвечает (`curl -I localhost:3001`)
- [ ] База данных доступна (`docker exec postgres psql -U postgres -c "SELECT 1;"`)
- [ ] Схема применена (`pnpm db:push`)

**MCP серверы:**
- [ ] Сервер добавлен в интерфейсе
- [ ] Сервер активирован (галочка "Use")
- [ ] Статус "connected" в списке серверов
- [ ] В логах видны инструменты от сервера

**API и сохранение:**
- [ ] API `/api/chats` возвращает данные
- [ ] User ID присутствует в localStorage
- [ ] Логи показывают "Chat saved with ID"
- [ ] История загружается при открытии чата

**Переменные окружения:**
- [ ] `.env.local` содержит `DATABASE_URL`
- [ ] AI API ключи настроены
- [ ] Для stdio: `DAYTONA_API_KEY` настроен

Если все пункты выполнены, но проблема остается - приложите логи из терминала и консоли браузера к вашему запросу о помощи.