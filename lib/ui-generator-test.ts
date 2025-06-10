/**
 * Тестовые примеры и демонстрация работы UI Generator
 */

import { UIGenerator } from './ui-generator';
import { MCPUIHelper, mcpUI } from './mcp-ui-helpers';

/**
 * Набор тестовых данных для демонстрации
 */
export const testData = {
  // Данные пользователей для таблицы
  users: [
    {
      id: 1,
      name: 'Иван Петров',
      email: 'ivan@company.com',
      department: 'Разработка',
      position: 'Senior Developer',
      salary: 120000,
      active: true,
      joinDate: '2022-03-15T00:00:00Z'
    },
    {
      id: 2,
      name: 'Мария Сидорова',
      email: 'maria@company.com',
      department: 'Дизайн',
      position: 'UI/UX Designer',
      salary: 95000,
      active: true,
      joinDate: '2023-01-20T00:00:00Z'
    },
    {
      id: 3,
      name: 'Алексей Козлов',
      email: 'alex@company.com',
      department: 'QA',
      position: 'QA Engineer',
      salary: 85000,
      active: false,
      joinDate: '2021-08-10T00:00:00Z'
    }
  ],

  // Профиль одного пользователя для карточки
  userProfile: {
    name: 'Иван Петров',
    email: 'ivan@company.com',
    phone: '+7 (999) 123-45-67',
    department: 'Разработка',
    position: 'Senior Developer',
    employeeId: 'EMP-001',
    startDate: '2022-03-15',
    manager: 'Анна Николаева',
    location: 'Москва, офис №1',
    skills: ['JavaScript', 'React', 'Node.js', 'PostgreSQL'],
    projects: ['Проект Alpha', 'Проект Beta'],
    performance: {
      rating: 4.7,
      tasksCompleted: 145,
      tasksInProgress: 3,
      efficiency: 92
    }
  },

  // Список задач
  tasks: [
    {
      id: 'TASK-001',
      title: 'Реализовать систему аутентификации',
      description: 'Добавить JWT токены и OAuth2',
      status: 'В работе',
      priority: 'Высокий',
      assignee: 'Иван Петров',
      reporter: 'Анна Николаева',
      created: '2024-01-10T09:00:00Z',
      updated: '2024-01-13T14:30:00Z',
      dueDate: '2024-01-20T23:59:59Z',
      progress: 75,
      estimatedHours: 40,
      loggedHours: 30,
      tags: ['backend', 'security', 'critical'],
      comments: 3
    },
    {
      id: 'TASK-002',
      title: 'Создать мобильную версию дашборда',
      description: 'Адаптивный дизайн для планшетов и телефонов',
      status: 'Новая',
      priority: 'Средний',
      assignee: 'Мария Сидорова',
      reporter: 'Иван Петров',
      created: '2024-01-12T11:15:00Z',
      updated: '2024-01-12T11:15:00Z',
      dueDate: '2024-01-25T23:59:59Z',
      progress: 0,
      estimatedHours: 32,
      loggedHours: 0,
      tags: ['frontend', 'mobile', 'ui'],
      comments: 1
    }
  ],

  // Статистика для графиков
  statistics: {
    monthly: [12, 19, 23, 17, 25, 21, 18, 29, 15, 22, 26, 20],
    weekly: [45, 52, 38, 67, 41, 58, 49],
    daily: [8, 12, 6, 15, 9, 11, 7, 14, 10, 8],
    categories: {
      'Разработка': 45,
      'Тестирование': 23,
      'Дизайн': 18,
      'Документация': 9,
      'Встречи': 15
    }
  },

  // Комплексные данные проекта
  project: {
    info: {
      name: 'Проект Alpha',
      description: 'Система управления задачами нового поколения',
      status: 'В разработке',
      startDate: '2024-01-01',
      endDate: '2024-06-30',
      budget: 2500000,
      spent: 1250000,
      currency: 'RUB'
    },
    team: [
      { name: 'Иван Петров', role: 'Tech Lead', load: 100 },
      { name: 'Мария Сидорова', role: 'Designer', load: 80 },
      { name: 'Алексей Козлов', role: 'QA Engineer', load: 60 }
    ],
    metrics: {
      totalTasks: 156,
      completedTasks: 89,
      inProgressTasks: 23,
      blockedTasks: 5,
      efficiency: 87,
      velocity: 15.3,
      burndown: [100, 95, 88, 82, 75, 68, 60, 52, 45, 38, 30, 22, 15, 8, 3]
    },
    milestones: [
      { name: 'Прототип', date: '2024-02-15', status: 'Завершён' },
      { name: 'MVP', date: '2024-04-01', status: 'В работе' },
      { name: 'Бета-версия', date: '2024-05-15', status: 'Запланирован' },
      { name: 'Релиз', date: '2024-06-30', status: 'Запланирован' }
    ]
  }
};

/**
 * Класс для тестирования UI Generator
 */
export class UIGeneratorTester {
  private generator: UIGenerator;
  private helper: MCPUIHelper;

  constructor() {
    this.generator = new UIGenerator();
    this.helper = new MCPUIHelper({
      defaultTheme: 'modern',
      enableInteractivity: true,
      enableResponsive: true,
      enableAccessibility: true
    });
  }

  /**
   * Тест 1: Автоматическое определение типа компонента
   */
  testAutoComponentSelection() {
    console.log('=== Тест автоматического выбора компонентов ===');

    const tests = [
      { name: 'Массив пользователей', data: testData.users, expected: 'table' },
      { name: 'Профиль пользователя', data: testData.userProfile, expected: 'card' },
      { name: 'Числовая статистика', data: testData.statistics.weekly, expected: 'chart' },
      { name: 'Простая строка', data: 'Привет, мир!', expected: 'text' },
      { name: 'Простое число', data: 42, expected: 'text' }
    ];

    tests.forEach(test => {
      const html = this.generator.generate(test.data, { component: 'auto' });
      console.log(`${test.name}: ${html.length > 0 ? 'OK' : 'FAIL'}`);
    });
  }

  /**
   * Тест 2: Различные типы компонентов
   */
  testComponentTypes() {
    console.log('=== Тест различных типов компонентов ===');

    const components = ['table', 'card', 'list', 'chart', 'text'] as const;
    
    components.forEach(component => {
      try {
        const html = this.generator.generate(testData.users, { component });
        console.log(`Компонент ${component}: ${html.length > 0 ? 'OK' : 'FAIL'}`);
      } catch (error) {
        console.log(`Компонент ${component}: FAIL - ${error}`);
      }
    });
  }

  /**
   * Тест 3: Различные темы
   */
  testThemes() {
    console.log('=== Тест различных тем ===');

    const themes = ['modern', 'dark'];
    
    themes.forEach(theme => {
      try {
        const html = this.generator.generate(testData.userProfile, { 
          component: 'card', 
          theme 
        });
        console.log(`Тема ${theme}: ${html.includes('--ui-primary') ? 'OK' : 'FAIL'}`);
      } catch (error) {
        console.log(`Тема ${theme}: FAIL - ${error}`);
      }
    });
  }

  /**
   * Тест 4: MCP UI Helper функции
   */
  testMCPUIHelper() {
    console.log('=== Тест MCP UI Helper ===');

    try {
      // Тест создания таблицы
      const table = this.helper.createUIResponse(testData.users, {
        component: 'table',
        title: 'Сотрудники компании'
      });
      console.log(`Создание таблицы: ${table.content[0].resource.text.length > 0 ? 'OK' : 'FAIL'}`);

      // Тест создания дашборда
      const metrics = [
        { title: 'Всего пользователей', value: 156, change: 12, changeType: 'increase' as const },
        { title: 'Активных', value: 143, change: 5, changeType: 'increase' as const },
        { title: 'Эффективность', value: 87, format: 'percentage' as const }
      ];
      const dashboard = this.helper.createDashboard(metrics, {
        title: 'Статистика пользователей'
      });
      console.log(`Создание дашборда: ${dashboard.content[0].resource.text.includes('mcp-dashboard') ? 'OK' : 'FAIL'}`);

      // Тест создания формы
      const fields = [
        { name: 'name', label: 'Имя', type: 'text' as const, required: true },
        { name: 'email', label: 'Email', type: 'email' as const, required: true }
      ];
      const form = this.helper.createForm(fields, {
        title: 'Регистрация пользователя'
      });
      console.log(`Создание формы: ${form.content[0].resource.text.includes('mcp-form') ? 'OK' : 'FAIL'}`);

      // Тест создания уведомления
      const notification = this.helper.createNotification(
        'Пользователь успешно создан!',
        { type: 'success', title: 'Успех' }
      );
      console.log(`Создание уведомления: ${notification.content[0].resource.text.includes('mcp-notification') ? 'OK' : 'FAIL'}`);

    } catch (error) {
      console.log(`MCP UI Helper: FAIL - ${error}`);
    }
  }

  /**
   * Тест 5: Производительность
   */
  testPerformance() {
    console.log('=== Тест производительности ===');

    const startTime = Date.now();
    const iterations = 100;

    for (let i = 0; i < iterations; i++) {
      this.generator.generate(testData.users, { component: 'auto' });
    }

    const endTime = Date.now();
    const avgTime = (endTime - startTime) / iterations;

    console.log(`Среднее время генерации: ${avgTime.toFixed(2)}ms`);
    console.log(`Производительность: ${avgTime < 10 ? 'OK' : 'WARN'} (цель: < 10ms)`);
  }

  /**
   * Запуск всех тестов
   */
  runAllTests() {
    console.log('Запуск тестов UI Generator...\n');

    this.testAutoComponentSelection();
    console.log('');

    this.testComponentTypes();
    console.log('');

    this.testThemes();
    console.log('');

    this.testMCPUIHelper();
    console.log('');

    this.testPerformance();
    console.log('');

    console.log('Тестирование завершено!');
  }

  /**
   * Генерация примеров для демонстрации
   */
  generateExamples() {
    const examples = {
      // Пример 1: Таблица пользователей
      usersTable: this.helper.createUIResponse(testData.users, {
        component: 'table',
        title: 'Список сотрудников',
        description: 'Информация о сотрудниках компании'
      }),

      // Пример 2: Карточка профиля
      userProfile: this.helper.createUIResponse(testData.userProfile, {
        component: 'card',
        title: 'Профиль сотрудника'
      }),

      // Пример 3: Список задач
      tasksList: this.helper.createUIResponse(testData.tasks, {
        component: 'list',
        title: 'Активные задачи'
      }),

      // Пример 4: График статистики
      statsChart: this.helper.createUIResponse(testData.statistics.monthly, {
        component: 'chart',
        title: 'Статистика по месяцам'
      }),

      // Пример 5: Комплексные данные проекта (автовыбор)
      projectData: this.helper.createUIResponse(testData.project, {
        component: 'auto',
        title: 'Обзор проекта'
      }),

      // Пример 6: Дашборд
      dashboard: this.helper.createDashboard([
        { title: 'Всего задач', value: 156, change: 12, changeType: 'increase' },
        { title: 'Завершено', value: 89, change: -5, changeType: 'decrease' },
        { title: 'В работе', value: 23, change: 8, changeType: 'increase' },
        { title: 'Эффективность', value: 87, format: 'percentage' }
      ], {
        title: 'Панель управления проектом'
      }),

      // Пример 7: Форма создания задачи
      taskForm: this.helper.createForm([
        { name: 'title', label: 'Название задачи', type: 'text', required: true },
        { name: 'description', label: 'Описание', type: 'textarea' },
        { name: 'priority', label: 'Приоритет', type: 'select', options: ['Низкий', 'Средний', 'Высокий'] },
        { name: 'assignee', label: 'Исполнитель', type: 'text' },
        { name: 'dueDate', label: 'Срок выполнения', type: 'text' }
      ], {
        title: 'Создание новой задачи',
        submitLabel: 'Создать задачу'
      }),

      // Пример 8: Уведомления
      successNotification: this.helper.createNotification(
        'Задача успешно создана и назначена исполнителю!',
        { type: 'success', title: 'Успех', dismissible: true }
      ),

      warningNotification: this.helper.createNotification(
        'Некоторые поля формы заполнены некорректно. Проверьте данные.',
        { type: 'warning', title: 'Внимание', dismissible: true }
      )
    };

    return examples;
  }
}

/**
 * Создание экземпляра тестера для экспорта
 */
export const tester = new UIGeneratorTester();

/**
 * Быстрый тест для проверки работоспособности
 */
export function quickTest() {
  console.log('Быстрая проверка UI Generator...');
  
  const generator = new UIGenerator();
  const result = generator.generate(testData.users, { component: 'auto' });
  
  if (result && result.length > 0) {
    console.log('✅ UI Generator работает корректно!');
    return true;
  } else {
    console.log('❌ Проблема с UI Generator!');
    return false;
  }
}

/**
 * Экспорт тестовых данных и функций
 */
const uiGeneratorTestModule = {
  testData,
  tester,
  quickTest,
  UIGeneratorTester
};

export default uiGeneratorTestModule;