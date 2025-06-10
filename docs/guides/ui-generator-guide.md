# Руководство по использованию UI Generator

## Введение

UI Generator - это автоматическая система генерации интерактивных интерфейсов для MCP серверов. Система анализирует данные и автоматически создаёт подходящие UI компоненты без необходимости написания HTML/CSS вручную.

## Быстрый старт

### 1. Базовое использование

```typescript
import { UIGenerator } from '@/lib/ui-generator';

const generator = new UIGenerator();

// Автоматическая генерация для любых данных
const data = [
  { name: 'Иван', role: 'Developer', active: true },
  { name: 'Мария', role: 'Designer', active: true }
];

const html = generator.generate(data, { 
  component: 'auto',  // Автоматический выбор компонента
  theme: 'modern'     // Современная тема
});

// Для MCP сервера
return {
  content: [{
    type: 'resource',
    resource: {
      uri: 'ui://generated',
      mimeType: 'text/html',
      text: html
    }
  }]
};
```

### 2. Использование готовых хелперов

```typescript
import { mcpUI, createTable, createCard } from '@/lib/mcp-ui-helpers';

// Создание таблицы одной строкой
const tableResponse = createTable(users, { title: 'Список пользователей' });

// Создание карточки профиля
const cardResponse = createCard(userProfile, { title: 'Профиль' });

// Автоматический выбор компонента
const autoResponse = mcpUI.createUIResponse(anyData, {
  component: 'auto',
  title: 'Результаты',
  theme: 'modern'
});
```

## Типы компонентов

### 1. **Таблица** (`table`)
Лучше всего подходит для:
- Массивов объектов с множественными полями (>5 полей)
- Табличных данных
- Списков с сортировкой и фильтрацией

```typescript
const users = [
  { id: 1, name: 'Иван', email: 'ivan@test.com', role: 'Dev' },
  { id: 2, name: 'Мария', email: 'maria@test.com', role: 'Design' }
];

const html = generator.generate(users, { component: 'table' });
```

### 2. **Карточка** (`card`)
Подходит для:
- Одиночных объектов
- Профилей пользователей
- Детальной информации

```typescript
const profile = {
  name: 'Иван Петров',
  email: 'ivan@company.com',
  department: 'Разработка',
  position: 'Senior Developer'
};

const html = generator.generate(profile, { component: 'card' });
```

### 3. **Список** (`list`)
Используется для:
- Массивов с небольшим количеством полей
- Простых списков
- Карточного отображения

```typescript
const tasks = [
  { title: 'Задача 1', status: 'В работе' },
  { title: 'Задача 2', status: 'Завершена' }
];

const html = generator.generate(tasks, { component: 'list' });
```

### 4. **График** (`chart`)
Для числовых данных:
- Массивы чисел
- Статистика
- Метрики

```typescript
const stats = [12, 19, 23, 17, 25, 21, 18, 29];

const html = generator.generate(stats, { component: 'chart' });
```

### 5. **Автоматический выбор** (`auto`)
Система сама выберет наиболее подходящий компонент:

```typescript
// Массив объектов → таблица или список
const data1 = [{ name: 'Test', value: 123 }];

// Одиночный объект → карточка
const data2 = { name: 'Test', value: 123 };

// Числовой массив → график
const data3 = [1, 2, 3, 4, 5];

// Для всех используем auto
const html = generator.generate(data, { component: 'auto' });
```

## Дополнительные компоненты

### Дашборд с метриками

```typescript
import { MCPUIHelper } from '@/lib/mcp-ui-helpers';

const ui = new MCPUIHelper();

const metrics = [
  { title: 'Всего пользователей', value: 156, change: 12, changeType: 'increase' },
  { title: 'Активных сегодня', value: 89, change: -5, changeType: 'decrease' },
  { title: 'Конверсия', value: 87, format: 'percentage' }
];

const dashboard = ui.createDashboard(metrics, {
  title: 'Аналитика'
});
```

### Интерактивные формы

```typescript
const fields = [
  { name: 'name', label: 'Имя', type: 'text', required: true },
  { name: 'email', label: 'Email', type: 'email', required: true },
  { name: 'role', label: 'Роль', type: 'select', options: ['User', 'Admin'] },
  { name: 'bio', label: 'О себе', type: 'textarea' }
];

const form = ui.createForm(fields, {
  title: 'Регистрация пользователя',
  submitLabel: 'Зарегистрироваться'
});
```

### Уведомления

```typescript
// Уведомление об успехе
const success = ui.createNotification(
  'Операция выполнена успешно!',
  { type: 'success', title: 'Готово', dismissible: true }
);

// Предупреждение
const warning = ui.createNotification(
  'Проверьте введённые данные',
  { type: 'warning', title: 'Внимание' }
);

// Ошибка
const error = ui.createNotification(
  'Произошла ошибка при сохранении',
  { type: 'error', title: 'Ошибка' }
);
```

## Конфигурация и темы

### Настройка темы

```typescript
const config = {
  component: 'auto',
  theme: 'modern',        // 'modern' | 'dark'
  interactive: true,      // Интерактивность
  responsive: true,       // Адаптивность
  accessibility: true     // Поддержка a11y
};

const html = generator.generate(data, config);
```

### Кастомизация стилей

```typescript
const ui = new MCPUIHelper({
  defaultTheme: 'modern',
  customStyles: `
    .ui-table { border-radius: 12px; }
    .ui-card { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
  `
});
```

## Интеграция с MCP сервером

### Простая интеграция

```typescript
import { mcpUI } from '@/lib/mcp-ui-helpers';

export class MyMCPServer {
  
  async getUserList() {
    const users = await getUsersFromDB();
    
    return mcpUI.createUIResponse(users, {
      title: 'Список пользователей',
      component: 'table',
      uri: 'ui://users-list'
    });
  }
  
  async getUserProfile(userId: string) {
    const profile = await getUserById(userId);
    
    return mcpUI.createUIResponse(profile, {
      title: 'Профиль пользователя',
      component: 'card',
      uri: `ui://user-${userId}`
    });
  }
}
```

### Использование декоратора

```typescript
import { MCPUIHelper } from '@/lib/mcp-ui-helpers';

export class MyMCPServer {
  private ui = new MCPUIHelper();

  @ui.autoUI({ title: 'Статистика задач', component: 'auto' })
  async getTaskStats() {
    // Возвращаем обычные данные
    return {
      total: 156,
      completed: 89,
      inProgress: 23,
      pending: 44
    };
    // UI будет создан автоматически
  }
}
```

## Примеры для разных типов данных

### Данные пользователей

```typescript
const users = [
  {
    id: 1,
    name: 'Иван Петров',
    email: 'ivan@company.com',
    department: 'IT',
    position: 'Developer',
    salary: 120000,
    active: true,
    joinDate: '2022-03-15'
  }
];

// Автоматически создаст таблицу
const html = generator.generate(users, { component: 'auto' });
```

### Профиль пользователя

```typescript
const profile = {
  name: 'Иван Петров',
  email: 'ivan@company.com',
  phone: '+7 999 123-45-67',
  department: 'IT отдел',
  position: 'Senior Developer',
  experience: '5 лет',
  skills: ['JavaScript', 'React', 'Node.js'],
  projects: ['Проект A', 'Проект B'],
  performance: { rating: 4.8, tasks: 145 }
};

// Автоматически создаст карточку
const html = generator.generate(profile, { component: 'auto' });
```

### Статистика и метрики

```typescript
// Простые числа - создаст график
const monthlyStats = [12, 19, 23, 17, 25, 21, 18, 29, 15, 22];

// Комплексная статистика - создаст дашборд
const complexStats = {
  users: { total: 1250, active: 890, new: 45 },
  revenue: { current: 125000, previous: 118000, growth: 5.9 },
  performance: { uptime: 99.8, response: 120, errors: 0.2 }
};

const dashboard = ui.createDashboard([
  { title: 'Всего пользователей', value: 1250, change: 8, changeType: 'increase' },
  { title: 'Активных', value: 890, change: 12, changeType: 'increase' },
  { title: 'Доход', value: 125000, format: 'currency' },
  { title: 'Время отклика', value: 120, change: -15, changeType: 'decrease' }
]);
```

## Лучшие практики

### 1. Выбор правильного компонента

- **Таблица**: >5 полей в объекте, нужна сортировка
- **Список**: 2-5 полей в объекте, акцент на читаемость
- **Карточка**: Одиночный объект, детальная информация
- **График**: Числовые данные, тренды, статистика
- **Авто**: Не уверены - система выберет сама

### 2. Структурирование данных

```typescript
// Хорошо - понятные названия полей
const goodData = {
  userName: 'Иван Петров',
  userEmail: 'ivan@test.com',
  isActive: true
};

// Плохо - непонятные сокращения
const badData = {
  usr_nm: 'Иван Петров',
  eml: 'ivan@test.com',
  act: 1
};
```

### 3. Использование метаданных

```typescript
// Добавление контекста для лучшего отображения
const dataWithContext = {
  title: 'Отчёт по продажам',
  description: 'Статистика за последний месяц',
  data: salesData,
  metadata: {
    generated: new Date(),
    source: 'CRM система',
    period: 'Январь 2024'
  }
};
```

### 4. Обработка ошибок

```typescript
try {
  const html = generator.generate(data, config);
  return mcpUI.createUIResponse(html);
} catch (error) {
  // Fallback для некорректных данных
  return mcpUI.createNotification(
    'Не удалось сгенерировать интерфейс',
    { type: 'error', title: 'Ошибка' }
  );
}
```

## Тестирование

```typescript
import { tester } from '@/lib/ui-generator-test';

// Запуск всех тестов
tester.runAllTests();

// Быстрая проверка
import { quickTest } from '@/lib/ui-generator-test';
quickTest(); // true если всё работает
```

## Заключение

UI Generator значительно упрощает создание интерактивных интерфейсов для MCP серверов:

- **Автоматическая генерация** - не нужно писать HTML/CSS
- **Умный выбор компонентов** - система сама определит лучший формат
- **Готовые решения** - таблицы, карточки, формы, дашборды
- **Простая интеграция** - несколько строк кода
- **Адаптивность** - работает на всех устройствах
- **Доступность** - поддержка a11y из коробки

Начните с автоматического режима (`component: 'auto'`) и при необходимости переходите к точной настройке компонентов.