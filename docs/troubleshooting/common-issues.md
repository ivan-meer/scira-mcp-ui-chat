# 🐛 Частые проблемы и их решения

Это руководство поможет решить наиболее распространенные проблемы при работе с MCP UI Playground Chat.

## 🚨 Критические проблемы

### ИИ не видит добавленные MCP серверы

**Симптомы:**
- Сервер показывает статус "connected"
- В логах видно "MCP tools from server-url: [...]"
- Но ИИ отвечает "у меня нет инструментов" или не использует MCP инструменты

**Причины и решения:**

#### 1. Сервер не активирован для чата

**Проверка:**
```bash
# В логах должно быть:
servers [
  {
    id: 'your-server-id',
    name: 'Your Server',
    status: 'connected'
  }
]
```

**Решение:**
1. Откройте настройки MCP (⚙️)
2. Найдите ваш сервер в списке
3. Убедитесь что галочка "Use" активна
4. Перезагрузите страницу

#### 2. Сервер подключен но инструменты не передаются

**Проверка в коде:**
```typescript
// lib/context/mcp-context.tsx:135
const getActiveServersForApi = (): MCPServerApi[] => {
  return selectedMcpServers  // <- проверьте что сервер в этом списке
    .map(id => getServerById(id))
    .filter((server): server is MCPServer => !!server && server.status === 'connected')
    .map(server => ({
      type: 'sse',
      url: server.type === 'stdio' && server.sandboxUrl ? server.sandboxUrl : server.url,
      headers: server.headers
    }));
};
```

**Решение:**
1. Откройте консоль разработчика (F12)
2. Проверьте что в `selectedMcpServers` есть ID вашего сервера
3. Если нет - активируйте сервер через интерфейс

#### 3. Проблема с localStorage

**Симптомы:**
- Сервер исчезает после перезагрузки
- Настройки не сохраняются

**Решение:**
```javascript
// Очистка localStorage в консоли браузера
localStorage.removeItem('mcp-servers');
localStorage.removeItem('selected-mcp-servers');

// Перезагрузите страницу и добавьте серверы заново
```

### Чаты не сохраняются

**Симптомы:**
- Сообщения отправляются и получаются
- Но при перезагрузке чаты исчезают
- Ошибки в API `/api/chats`

**Причины и решения:**

#### 1. Проблема с базой данных

**Проверка:**
```bash
# Проверьте статус PostgreSQL
docker ps | grep postgres

# Должно показать:
# CONTAINER_ID   postgres   ...   Up X minutes   0.0.0.0:5432->5432/tcp
```

**Решение:**
```bash
# Перезапустите PostgreSQL
docker restart postgres

# Проверьте подключение
docker exec postgres psql -U postgres -c "SELECT 1;"
```

#### 2. Неправильный драйвер базы данных

**Проверка файла `lib/db/index.ts`:**
```typescript
// Должно быть:
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";

// НЕ должно быть:
import { drizzle } from "drizzle-orm/neon-serverless";
import { Pool } from "@neondatabase/serverless";
```

**Решение:**
```bash
# Исправьте импорты в lib/db/index.ts
# Перезапустите сервер разработки
pnpm dev
```

#### 3. Отсутствует user-id в заголовках

**Проверка в консоли браузера:**
```javascript
// Network tab -> XHR -> /api/chats
// Headers должны содержать:
// x-user-id: some-user-id
```

**Проверка кода:**
```typescript
// lib/user-id.ts - должен генерировать ID пользователя
export function getUserId(): string {
  if (typeof window === 'undefined') return 'server-user';
  
  let userId = localStorage.getItem('user-id');
  if (!userId) {
    userId = nanoid();
    localStorage.setItem('user-id', userId);
  }
  return userId;
}
```

## ⚠️ Предупреждения и ошибки

### "Failed to initialize MCP client: 502 Bad Gateway"

**Причина:** Sandbox создался, но сервис внутри недоступен

**Решение:**
1. Проверьте что сервис на указанном порту работает
2. Для stdio серверов убедитесь что команда корректна
3. Проверьте логи sandbox в консоли

**Пример исправления:**
```bash
# Вместо:
docker run alpine/socat STDIO TCP:host.docker.internal:8811

# Используйте:
docker run -i --rm alpine/socat STDIO TCP:host.docker.internal:8811
```

### "Error: connect ECONNREFUSED 127.0.0.1:5432"

**Причина:** PostgreSQL не запущен

**Решение:**
```bash
# Запустите PostgreSQL
docker start postgres

# Или создайте новый контейнер
docker run --name postgres-mcp \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=postgres \
  -p 5432:5432 \
  -d postgres:15
```

### "API key or JWT token is required"

**Причина:** Отсутствует Daytona API ключ

**Решение:**
1. Добавьте в `.env.local`:
```env
DAYTONA_API_KEY=your_daytona_key
DAYTONA_API_URL="https://app.daytona.io/api"
```

2. Перезапустите сервер:
```bash
pnpm dev
```

## 🔍 Отладка пошагово

### Проверка MCP сервера

1. **Статус подключения**
```javascript
// В консоли браузера
console.log(localStorage.getItem('mcp-servers'));
console.log(localStorage.getItem('selected-mcp-servers'));
```

2. **Логи инициализации**
```bash
# В терминале разработки ищите:
"MCP tools from https://server-url/sse: ['tool1', 'tool2']"
"Failed to initialize MCP client: Error details"
```

3. **Проверка API запроса**
```javascript
// Network tab в DevTools
// POST /api/chat
// Request payload должен содержать:
{
  "messages": [...],
  "mcpServers": [
    {
      "type": "sse",
      "url": "https://server-url/sse"
    }
  ]
}
```

### Проверка сохранения чатов

1. **API запрос чатов**
```bash
curl -H "x-user-id: test-user" http://localhost:3001/api/chats
```

2. **Проверка базы данных**
```bash
docker exec postgres psql -U postgres -c "SELECT * FROM chats LIMIT 5;"
docker exec postgres psql -U postgres -c "SELECT * FROM messages LIMIT 5;"
```

3. **Логи сохранения**
```bash
# В терминале ищите:
"Saving chat with ID: chat-id"
"Chat saved successfully"
```

## 📋 Диагностический чеклист

### Перед обращением за помощью

- [ ] PostgreSQL запущен и доступен
- [ ] Файл `.env.local` содержит правильный `DATABASE_URL`
- [ ] Схема базы данных применена (`pnpm db:push`)
- [ ] MCP сервер добавлен и активирован
- [ ] В логах видны инструменты от MCP сервера
- [ ] API `/api/chats` возвращает данные (пустой массив ОК)
- [ ] User ID генерируется в localStorage
- [ ] Нет ошибок в консоли браузера

### Команды для сбора информации

```bash
# Статус всех контейнеров
docker ps -a

# Логи PostgreSQL
docker logs postgres

# Тест подключения к базе
docker exec postgres psql -U postgres -c "\l"

# Проверка схемы
docker exec postgres psql -U postgres -c "\d"

# Статус приложения
curl -I http://localhost:3001
```

## 🆘 Экстренное восстановление

### Полная переустановка

```bash
# 1. Остановите все
docker stop postgres
pnpm dev # Ctrl+C

# 2. Очистите данные
docker rm postgres
rm -rf node_modules
rm .env.local

# 3. Переустановите
pnpm install

# 4. Настройте заново
cp .env.example .env.local
# Отредактируйте .env.local

# 5. Запустите базу
docker run --name postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -d postgres:15

# 6. Примените схему
pnpm db:push

# 7. Запустите приложение
pnpm dev
```

### Очистка браузера

```javascript
// В консоли браузера
localStorage.clear();
sessionStorage.clear();
// Перезагрузите страницу (Ctrl+F5)
```