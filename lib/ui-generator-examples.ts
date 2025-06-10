/**
 * Примеры использования автоматического генератора UI
 */

import { UIGenerator, GenerationConfig } from './ui-generator';

// Создание экземпляра генератора
const generator = new UIGenerator();

/**
 * Пример 1: Автоматическая генерация таблицы пользователей
 */
export function generateUsersTable() {
  const usersData = [
    { id: 1, name: 'Иван Петров', email: 'ivan@example.com', role: 'Admin', active: true },
    { id: 2, name: 'Мария Сидорова', email: 'maria@example.com', role: 'User', active: true },
    { id: 3, name: 'Алексей Козлов', email: 'alex@example.com', role: 'Editor', active: false },
  ];

  const config: GenerationConfig = {
    component: 'auto', // Автоматический выбор (будет таблица)
    theme: 'modern',
    interactive: true,
    responsive: true,
    accessibility: true
  };

  return generator.generate(usersData, config);
}

/**
 * Пример 2: Карточка профиля пользователя
 */
export function generateUserProfile() {
  const profileData = {
    name: 'Иван Петров',
    email: 'ivan@example.com',
    department: 'Разработка',
    position: 'Senior Developer',
    phone: '+7 (999) 123-45-67',
    location: 'Москва',
    joinDate: '2022-03-15T00:00:00Z',
    tasksCompleted: 145,
    projectsActive: 3
  };

  const config: GenerationConfig = {
    component: 'card',
    theme: 'modern',
    interactive: false
  };

  return generator.generate(profileData, config);
}

/**
 * Пример 3: График статистики
 */
export function generateStatsChart() {
  const statsData = [25, 45, 30, 60, 35, 50, 75, 40];

  const config: GenerationConfig = {
    component: 'chart',
    theme: 'dark',
    interactive: true
  };

  return generator.generate(statsData, config);
}

/**
 * Пример 4: Список задач
 */
export function generateTasksList() {
  const tasksData = [
    {
      id: 1,
      title: 'Исправить баг с авторизацией',
      priority: 'Высокий',
      status: 'В работе',
      assignee: 'Иван Петров'
    },
    {
      id: 2,
      title: 'Добавить новую функцию',
      priority: 'Средний',
      status: 'Новая',
      assignee: 'Мария Сидорова'
    },
    {
      id: 3,
      title: 'Обновить документацию',
      priority: 'Низкий',
      status: 'Завершена',
      assignee: 'Алексей Козлов'
    }
  ];

  const config: GenerationConfig = {
    component: 'list',
    theme: 'modern',
    interactive: true,
    responsive: true
  };

  return generator.generate(tasksData, config);
}

/**
 * Пример 5: Сложные данные с автоматическим выбором компонента
 */
export function generateComplexData() {
  const complexData = {
    summary: {
      totalUsers: 150,
      activeProjects: 12,
      completedTasks: 890,
      pendingIssues: 23
    },
    recentActivity: [
      'Пользователь Иван создал новую задачу',
      'Проект "Alpha" обновлён',
      'Задача #456 завершена'
    ],
    topUsers: [
      { name: 'Иван Петров', score: 95 },
      { name: 'Мария Сидорова', score: 87 },
      { name: 'Алексей Козлов', score: 82 }
    ]
  };

  const config: GenerationConfig = {
    component: 'auto',
    theme: 'modern',
    interactive: true,
    responsive: true,
    accessibility: true
  };

  return generator.generate(complexData, config);
}

/**
 * Пример функции для MCP сервера
 */
export function createMCPUIResponse(data: any, componentType?: string): any {
  const config: GenerationConfig = {
    component: (componentType as any) || 'auto',
    theme: 'modern',
    interactive: true,
    responsive: true,
    accessibility: true
  };

  const html = generator.generate(data, config);

  return {
    content: [
      {
        type: 'resource',
        resource: {
          uri: 'ui://auto-generated',
          mimeType: 'text/html',
          text: html
        }
      }
    ]
  };
}

/**
 * Пример интеграции с демо MCP сервером
 */
export class DemoMCPServerWithGenerator {
  private generator = new UIGenerator();

  // Улучшенная версия show_task_status с автогенерацией
  async showTaskStatus() {
    const tasksData = [
      {
        id: 'TASK-001',
        title: 'Реализовать аутентификацию',
        status: 'В работе',
        priority: 'Высокий',
        assignee: 'Иван Петров',
        progress: 75,
        dueDate: '2024-01-15',
        tags: ['backend', 'security']
      },
      {
        id: 'TASK-002', 
        title: 'Создать дизайн главной страницы',
        status: 'Завершена',
        priority: 'Средний',
        assignee: 'Мария Дизайнер',
        progress: 100,
        dueDate: '2024-01-10',
        tags: ['frontend', 'ui/ux']
      },
      {
        id: 'TASK-003',
        title: 'Настроить CI/CD pipeline',
        status: 'Новая',
        priority: 'Низкий', 
        assignee: null,
        progress: 0,
        dueDate: '2024-01-20',
        tags: ['devops', 'infrastructure']
      }
    ];

    const html = this.generator.generate(tasksData, {
      component: 'table',
      theme: 'modern',
      interactive: true,
      responsive: true,
      accessibility: true
    });

    return {
      content: [
        {
          type: 'resource',
          resource: {
            uri: 'ui://task-status-generated',
            mimeType: 'text/html', 
            text: html
          }
        }
      ]
    };
  }

  // Улучшенная версия show_user_status с автогенерацией
  async showUserStatus(userId: string = 'user-123') {
    const userData = {
      profile: {
        id: userId,
        name: 'Иван Петров',
        email: 'ivan.petrov@company.com',
        department: 'Разработка',
        position: 'Senior Developer',
        avatar: '👨‍💻'
      },
      stats: {
        tasksCompleted: 45,
        tasksInProgress: 3,
        projectsActive: 2,
        efficiency: 92
      },
      recentTasks: [
        { title: 'Исправить баг #123', status: 'Завершена', date: '2024-01-12' },
        { title: 'Код-ревью PR #456', status: 'В работе', date: '2024-01-13' },
        { title: 'Обновить документацию', status: 'Новая', date: '2024-01-14' }
      ]
    };

    const html = this.generator.generate(userData, {
      component: 'auto', // Автоматически выберет подходящий формат
      theme: 'modern',
      interactive: true,
      responsive: true
    });

    return {
      content: [
        {
          type: 'resource',
          resource: {
            uri: 'ui://user-status-generated',
            mimeType: 'text/html',
            text: html
          }
        }
      ]
    };
  }
}

// Экспорт для использования в других модулях
export { UIGenerator };
export default generator;