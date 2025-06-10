# Автоматическая генерация интерфейсов MCP-UI

## Обзор

Этот документ описывает архитектуру и реализацию автоматической генерации UI интерфейсов для MCP (Model Context Protocol) серверов. Система автоматически создаёт интерактивные интерфейсы на основе типов данных, схем и метаданных из ответов MCP инструментов.

## Текущая архитектура MCP-UI

### 1. **Поток обнаружения интерфейсов**

```
AI Модель → MCP Сервер → UI Парсер → UI Генератор → React Компонент → Пользователь
```

### 2. **Текущая структура UI ресурсов**

MCP серверы возвращают UI ресурсы в таком формате:

```json
{
  "content": [
    {
      "type": "resource",
      "resource": {
        "uri": "ui://component-name",
        "mimeType": "text/html",
        "text": "<div>HTML контент</div>"
      }
    }
  ]
}
```

### 3. **Анализ существующих компонентов**

На основе демо сервера, текущие инструменты возвращают:

- **get_tasks_status**: Текстовый список задач
- **show_task_status**: Интерактивная панель задач  
- **show_user_status**: Профиль пользователя с обзором задач
- **nudge_team_member**: Интерфейс уведомлений

## Архитектура автоматического UI генератора

### 1. **Определение типов данных**

```typescript
interface DataTypeSchema {
  type: 'object' | 'array' | 'string' | 'number' | 'boolean' | 'date';
  properties?: Record<string, DataTypeSchema>;
  items?: DataTypeSchema;
  format?: string;
  metadata?: UIMetadata;
}

interface UIMetadata {
  displayName?: string;        // Отображаемое имя
  description?: string;        // Описание
  component?: 'table' | 'card' | 'list' | 'form' | 'chart';
  validation?: ValidationRules; // Правила валидации
  styling?: StyleConfig;       // Конфигурация стилей
  interactions?: InteractionConfig; // Конфигурация взаимодействий
}
```

### 2. **Пайплайн генерации компонентов**

```typescript
interface GenerationPipeline {
  // Шаг 1: Парсинг и анализ данных
  analyze(data: any): DataTypeSchema;
  
  // Шаг 2: Генерация структуры компонента
  generateComponent(schema: DataTypeSchema): ComponentDefinition;
  
  // Шаг 3: Применение стилей и взаимодействий
  applyEnhancements(component: ComponentDefinition): EnhancedComponent;
  
  // Шаг 4: Рендеринг в HTML/React
  render(component: EnhancedComponent): string;
}
```

### 3. **Шаблоны компонентов**

#### Шаблон таблицы
```html
<div class="ui-table-container">
  <table class="ui-table">
    <thead>
      <tr>{{заголовки}}</tr>
    </thead>
    <tbody>
      {{#each строки}}
      <tr>{{#each this}}<td>{{this}}</td>{{/each}}</tr>
      {{/each}}
    </tbody>
  </table>
</div>
```

#### Шаблон карточки
```html
<div class="ui-card">
  <div class="ui-card-header">
    <h3>{{заголовок}}</h3>
  </div>
  <div class="ui-card-content">
    {{#each поля}}
    <div class="ui-field">
      <label>{{метка}}</label>
      <span>{{значение}}</span>
    </div>
    {{/each}}
  </div>
  {{#if действия}}
  <div class="ui-card-actions">
    {{#each действия}}
    <button onclick="{{действие}}">{{метка}}</button>
    {{/each}}
  </div>
  {{/if}}
</div>
```

## Примеры использования

### Базовое использование
```typescript
const generator = new UIGenerator();
const data = { users: [...], stats: {...} };
const html = generator.generate(data, {
  component: 'auto',
  theme: 'modern',
  interactive: true
});
```

### Продвинутая конфигурация
```typescript
const config = {
  components: {
    users: { type: 'table', sortable: true },
    stats: { type: 'chart', chartType: 'bar' }
  },
  styling: {
    theme: 'dark',
    colors: { primary: '#007bff' }
  },
  interactions: {
    onUserClick: { action: 'select_user', params: ['userId'] }
  }
};
```

## Преимущества

1. **Единообразие** - Унифицированный UI для всех MCP инструментов
2. **Эффективность** - Сокращение времени разработки MCP серверов  
3. **Доступность** - Встроенные функции a11y
4. **Сопровождаемость** - Централизованная логика UI
5. **Расширяемость** - Лёгкое добавление новых типов компонентов