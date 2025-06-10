# 🔗 Подключение MCP серверов

Подробное руководство по добавлению и настройке MCP серверов в приложении.

## Типы MCP серверов

### 1. SSE (Server-Sent Events) серверы
Удаленные HTTP серверы, которые предоставляют SSE endpoint.

**Преимущества:**
- Прямое подключение
- Не требует дополнительных ресурсов
- Быстрая настройка

**Недостатки:**
- Требует публичный URL
- Ограниченные возможности локальной разработки

### 2. stdio серверы
Локальные серверы, запускаемые через командную строку.

**Преимущества:**
- Полная изоляция в sandbox
- Поддержка любых команд
- Безопасность выполнения

**Недостатки:**
- Требует Daytona API ключ
- Дольше запускается (создание sandbox)

## Добавление SSE сервера

### Через интерфейс

1. **Откройте настройки MCP**
   - Нажмите иконку ⚙️ рядом с выбором модели
   - Или используйте кнопку "Add MCP Server" в боковой панели

2. **Заполните форму**
   ```
   Имя сервера: Мой SSE сервер
   Тип транспорта: SSE (Server-Sent Events)
   URL сервера: https://example.com/sse
   ```

3. **Добавьте заголовки (опционально)**
   ```
   Authorization: Bearer your-token
   X-API-Key: your-api-key
   ```

4. **Сохраните и активируйте**
   - Нажмите "Add Server"
   - Нажмите "Use" для активации

### Программно

```typescript
const server: MCPServer = {
  id: 'my-sse-server',
  name: 'Мой SSE сервер',
  type: 'sse',
  url: 'https://example.com/sse',
  headers: [
    { key: 'Authorization', value: 'Bearer token' }
  ],
  status: 'disconnected'
};
```

## Добавление stdio сервера

### Через интерфейс

1. **Откройте настройки MCP**
   
2. **Заполните форму stdio**
   ```
   Имя сервера: Docker MCP
   Тип транспорта: stdio (Standard I/O)
   Команда: docker
   Аргументы: run -i --rm alpine/socat STDIO TCP:host.docker.internal:8811
   ```

3. **Переменные окружения (опционально)**
   ```
   API_KEY: your-api-key
   DEBUG: true
   ```

4. **Сохраните и активируйте**

### Примеры stdio команд

**Python MCP сервер:**
```bash
Команда: python
Аргументы: -m mcp_server.example
```

**Node.js MCP сервер:**
```bash
Команда: npx
Аргументы: -y @modelcontextprotocol/server-filesystem
```

**Docker контейнер:**
```bash
Команда: docker
Аргументы: run -i --rm my-mcp-server
```

## Популярные MCP серверы

### 1. Filesystem Server
```bash
Команда: npx
Аргументы: -y @modelcontextprotocol/server-filesystem /path/to/directory
```

**Возможности:**
- Чтение файлов
- Поиск в файлах
- Создание и редактирование

### 2. GitHub Server
```bash
Команда: npx
Аргументы: -y @modelcontextprotocol/server-github
```

**Переменные окружения:**
```
GITHUB_PERSONAL_ACCESS_TOKEN: your-token
```

### 3. Memory Server
```bash
Команда: docker
Аргументы: run -i --rm mcp/memory
```

**Возможности:**
- Хранение знаний
- Поиск по памяти
- Ассоциации

### 4. Brave Search Server
```bash
Команда: npx
Аргументы: -y @modelcontextprotocol/server-brave-search
```

**Переменные окружения:**
```
BRAVE_API_KEY: your-api-key
```

## Управление серверами

### Проверка статуса

В интерфейсе статус отображается цветом:
- 🟢 **connected** - сервер работает
- 🟡 **connecting** - подключение
- 🔴 **error** - ошибка
- ⚪ **disconnected** - отключен

### Перезапуск сервера

1. Нажмите на сервер в списке
2. Нажмите "Stop" (если запущен)
3. Нажмите "Start" для повторного запуска

### Удаление сервера

1. Найдите сервер в списке
2. Нажмите кнопку удаления (🗑️)
3. Подтвердите действие

## Отладка подключения

### Логи в консоли

Откройте консоль разработчика (F12) и проверьте:

```javascript
// Логи MCP клиентов
"MCP tools from https://server-url/sse: ['tool1', 'tool2']"

// Ошибки подключения
"Failed to initialize MCP client: Error message"
```

### Логи сервера

В терминале разработки:

```bash
# Успешное подключение
"[startSandbox] Sandbox created for server-id, URL: https://sandbox-url/sse"

# Ошибки sandbox
"Error starting MCP sandbox: Error details"
```

### Проверка инструментов

После подключения сервера спросите ИИ:
```
Какие инструменты тебе доступны?
```

ИИ должен перечислить инструменты от подключенных серверов.

## Безопасность

### stdio серверы
- Выполняются в изолированном Daytona sandbox
- Нет доступа к локальной файловой системе
- Автоматическая очистка после использования

### SSE серверы
- Используйте HTTPS для безопасной передачи
- Проверяйте подлинность серверов
- Не передавайте секретные данные в URL

### Переменные окружения
- Никогда не храните API ключи в коде
- Используйте переменные окружения
- Регулярно обновляйте токены

## Примеры конфигураций

### Локальная разработка
```typescript
{
  name: "Local Dev Server",
  type: "stdio",
  command: "python",
  args: ["-m", "my_mcp_server"],
  env: [
    { key: "DEBUG", value: "true" },
    { key: "LOG_LEVEL", value: "debug" }
  ]
}
```

### Продакшн SSE
```typescript
{
  name: "Production API",
  type: "sse",
  url: "https://api.example.com/mcp/sse",
  headers: [
    { key: "Authorization", value: "Bearer prod-token" },
    { key: "User-Agent", value: "MCP-UI-Chat/1.0" }
  ]
}
```

### Docker сервер
```typescript
{
  name: "Docker MCP",
  type: "stdio", 
  command: "docker",
  args: ["run", "-i", "--rm", "my-org/mcp-server"],
  env: [
    { key: "CONTAINER_API_KEY", value: "container-key" }
  ]
}
```