/**
 * Вспомогательные утилиты для интеграции UI Generator с MCP серверами
 */

import { UIGenerator, GenerationConfig } from './ui-generator';

/**
 * Конфигурация MCP UI Helper
 */
export interface MCPUIConfig {
  defaultTheme?: string;
  enableInteractivity?: boolean;
  enableResponsive?: boolean;
  enableAccessibility?: boolean;
  customStyles?: string;
  componentMappings?: Record<string, string>;
}

/**
 * Результат генерации MCP UI
 */
export interface MCPUIResult {
  content: Array<{
    type: 'resource';
    resource: {
      uri: string;
      mimeType: string;
      text: string;
    };
  }>;
}

/**
 * Главный класс для интеграции с MCP серверами
 */
export class MCPUIHelper {
  private generator: UIGenerator;
  private config: MCPUIConfig;

  constructor(config: MCPUIConfig = {}) {
    this.generator = new UIGenerator();
    this.config = {
      defaultTheme: 'modern',
      enableInteractivity: true,
      enableResponsive: true,
      enableAccessibility: true,
      ...config
    };
  }

  /**
   * Создание UI ответа для MCP сервера
   */
  createUIResponse(
    data: any, 
    options: {
      uri?: string;
      component?: string;
      theme?: string;
      title?: string;
      description?: string;
    } = {}
  ): MCPUIResult {
    const generationConfig: GenerationConfig = {
      component: (options.component as any) || 'auto',
      theme: options.theme || this.config.defaultTheme,
      interactive: this.config.enableInteractivity,
      responsive: this.config.enableResponsive,
      accessibility: this.config.enableAccessibility
    };

    let html = this.generator.generate(data, generationConfig);

    // Добавление заголовка и описания
    if (options.title || options.description) {
      const header = `
        <div class="mcp-ui-header">
          ${options.title ? `<h2 class="mcp-ui-title">${options.title}</h2>` : ''}
          ${options.description ? `<p class="mcp-ui-description">${options.description}</p>` : ''}
        </div>
      `;
      html = header + html;
    }

    // Добавление кастомных стилей
    if (this.config.customStyles) {
      html = `<style>${this.config.customStyles}</style>` + html;
    }

    return {
      content: [
        {
          type: 'resource',
          resource: {
            uri: options.uri || `ui://generated-${Date.now()}`,
            mimeType: 'text/html',
            text: html
          }
        }
      ]
    };
  }

  /**
   * Декоратор для автоматического создания UI из результата функции
   */
  autoUI(options: {
    component?: string;
    theme?: string;
    title?: string;
    description?: string;
  } = {}) {
    return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
      const originalMethod = descriptor.value;

      descriptor.value = async function (...args: any[]) {
        const result = await originalMethod.apply(this, args);
        
        // Если результат уже в формате MCP UI, возвращаем как есть
        if (result && result.content && Array.isArray(result.content)) {
          return result;
        }

        // Создаем UI автоматически
        const helper = new MCPUIHelper();
        return helper.createUIResponse(result, {
          ...options,
          uri: `ui://${propertyKey}-auto`
        });
      };

      return descriptor;
    };
  }

  /**
   * Создание интерактивной формы
   */
  createForm(
    fields: Array<{
      name: string;
      label: string;
      type: 'text' | 'email' | 'number' | 'select' | 'textarea';
      required?: boolean;
      options?: string[];
      value?: any;
    }>,
    options: {
      title?: string;
      submitLabel?: string;
      action?: string;
      method?: string;
    } = {}
  ): MCPUIResult {
    const formFields = fields.map(field => {
      let input = '';
      
      switch (field.type) {
        case 'select':
          const options = field.options?.map(opt => 
            `<option value="${opt}" ${field.value === opt ? 'selected' : ''}>${opt}</option>`
          ).join('') || '';
          input = `<select name="${field.name}" ${field.required ? 'required' : ''}>${options}</select>`;
          break;
        
        case 'textarea':
          input = `<textarea name="${field.name}" ${field.required ? 'required' : ''}>${field.value || ''}</textarea>`;
          break;
        
        default:
          input = `<input type="${field.type}" name="${field.name}" value="${field.value || ''}" ${field.required ? 'required' : ''}>`;
      }

      return `
        <div class="mcp-form-field">
          <label for="${field.name}">${field.label}${field.required ? ' *' : ''}</label>
          ${input}
        </div>
      `;
    }).join('');

    const html = `
      <style>
        .mcp-form {
          max-width: 500px;
          margin: 20px 0;
          padding: 20px;
          border: 1px solid #ddd;
          border-radius: 8px;
          background: white;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .mcp-form-title {
          margin: 0 0 20px 0;
          color: #333;
          font-size: 18px;
          font-weight: 600;
        }
        .mcp-form-field {
          margin-bottom: 16px;
        }
        .mcp-form-field label {
          display: block;
          margin-bottom: 6px;
          font-weight: 500;
          color: #555;
        }
        .mcp-form-field input,
        .mcp-form-field select,
        .mcp-form-field textarea {
          width: 100%;
          padding: 8px 12px;
          border: 1px solid #ccc;
          border-radius: 4px;
          font-size: 14px;
          box-sizing: border-box;
        }
        .mcp-form-field textarea {
          resize: vertical;
          min-height: 80px;
        }
        .mcp-form-submit {
          background: #007bff;
          color: white;
          padding: 10px 20px;
          border: none;
          border-radius: 4px;
          font-size: 14px;
          cursor: pointer;
          font-weight: 500;
        }
        .mcp-form-submit:hover {
          background: #0056b3;
        }
      </style>
      <div class="mcp-form">
        ${options.title ? `<h3 class="mcp-form-title">${options.title}</h3>` : ''}
        <form action="${options.action || '#'}" method="${options.method || 'POST'}">
          ${formFields}
          <button type="submit" class="mcp-form-submit">
            ${options.submitLabel || 'Отправить'}
          </button>
        </form>
      </div>
    `;

    return {
      content: [
        {
          type: 'resource',
          resource: {
            uri: 'ui://generated-form',
            mimeType: 'text/html',
            text: html
          }
        }
      ]
    };
  }

  /**
   * Создание дашборда с метриками
   */
  createDashboard(
    metrics: Array<{
      title: string;
      value: number | string;
      change?: number;
      changeType?: 'increase' | 'decrease' | 'neutral';
      format?: 'number' | 'currency' | 'percentage';
    }>,
    options: {
      title?: string;
      columns?: number;
    } = {}
  ): MCPUIResult {
    const formatValue = (value: number | string, format?: string) => {
      if (typeof value === 'string') return value;
      
      switch (format) {
        case 'currency':
          return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value);
        case 'percentage':
          return `${value}%`;
        default:
          return value.toLocaleString('ru-RU');
      }
    };

    const formatChange = (change: number, type?: string) => {
      const sign = change > 0 ? '+' : '';
      const color = type === 'increase' ? '#28a745' : type === 'decrease' ? '#dc3545' : '#6c757d';
      return `<span style="color: ${color}; font-size: 12px;">${sign}${change}%</span>`;
    };

    const metricCards = metrics.map(metric => `
      <div class="mcp-metric-card">
        <div class="mcp-metric-title">${metric.title}</div>
        <div class="mcp-metric-value">${formatValue(metric.value, metric.format)}</div>
        ${metric.change !== undefined ? `<div class="mcp-metric-change">${formatChange(metric.change, metric.changeType)}</div>` : ''}
      </div>
    `).join('');

    const columns = options.columns || Math.min(metrics.length, 4);
    
    const html = `
      <style>
        .mcp-dashboard {
          margin: 20px 0;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .mcp-dashboard-title {
          margin: 0 0 20px 0;
          color: #333;
          font-size: 20px;
          font-weight: 600;
        }
        .mcp-metrics-grid {
          display: grid;
          grid-template-columns: repeat(${columns}, 1fr);
          gap: 16px;
        }
        .mcp-metric-card {
          padding: 20px;
          background: white;
          border: 1px solid #e9ecef;
          border-radius: 8px;
          text-align: center;
        }
        .mcp-metric-title {
          font-size: 14px;
          color: #6c757d;
          margin-bottom: 8px;
        }
        .mcp-metric-value {
          font-size: 24px;
          font-weight: 700;
          color: #333;
          margin-bottom: 4px;
        }
        .mcp-metric-change {
          font-size: 12px;
        }
        @media (max-width: 768px) {
          .mcp-metrics-grid {
            grid-template-columns: repeat(2, 1fr);
          }
        }
        @media (max-width: 480px) {
          .mcp-metrics-grid {
            grid-template-columns: 1fr;
          }
        }
      </style>
      <div class="mcp-dashboard">
        ${options.title ? `<h3 class="mcp-dashboard-title">${options.title}</h3>` : ''}
        <div class="mcp-metrics-grid">
          ${metricCards}
        </div>
      </div>
    `;

    return {
      content: [
        {
          type: 'resource',
          resource: {
            uri: 'ui://generated-dashboard',
            mimeType: 'text/html',
            text: html
          }
        }
      ]
    };
  }

  /**
   * Создание уведомления
   */
  createNotification(
    message: string,
    options: {
      type?: 'info' | 'success' | 'warning' | 'error';
      title?: string;
      dismissible?: boolean;
    } = {}
  ): MCPUIResult {
    const type = options.type || 'info';
    const colors = {
      info: { bg: '#d1ecf1', border: '#bee5eb', text: '#0c5460' },
      success: { bg: '#d4edda', border: '#c3e6cb', text: '#155724' },
      warning: { bg: '#fff3cd', border: '#ffeaa7', text: '#856404' },
      error: { bg: '#f8d7da', border: '#f5c6cb', text: '#721c24' }
    };

    const color = colors[type];

    const html = `
      <style>
        .mcp-notification {
          padding: 12px 16px;
          margin: 16px 0;
          border: 1px solid ${color.border};
          background-color: ${color.bg};
          color: ${color.text};
          border-radius: 4px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          position: relative;
        }
        .mcp-notification-title {
          font-weight: 600;
          margin-bottom: 4px;
        }
        .mcp-notification-close {
          position: absolute;
          top: 8px;
          right: 12px;
          background: none;
          border: none;
          font-size: 18px;
          cursor: pointer;
          color: ${color.text};
          opacity: 0.7;
        }
        .mcp-notification-close:hover {
          opacity: 1;
        }
      </style>
      <div class="mcp-notification">
        ${options.title ? `<div class="mcp-notification-title">${options.title}</div>` : ''}
        <div>${message}</div>
        ${options.dismissible ? '<button class="mcp-notification-close" onclick="this.parentElement.remove()">&times;</button>' : ''}
      </div>
    `;

    return {
      content: [
        {
          type: 'resource',
          resource: {
            uri: 'ui://generated-notification',
            mimeType: 'text/html',
            text: html
          }
        }
      ]
    };
  }
}

/**
 * Экспорт готового экземпляра для быстрого использования
 */
export const mcpUI = new MCPUIHelper();

/**
 * Функции-хелперы для быстрого использования
 */
export const createTable = (data: any[], options: { title?: string } = {}) => 
  mcpUI.createUIResponse(data, { component: 'table', ...options });

export const createCard = (data: any, options: { title?: string } = {}) => 
  mcpUI.createUIResponse(data, { component: 'card', ...options });

export const createList = (data: any[], options: { title?: string } = {}) => 
  mcpUI.createUIResponse(data, { component: 'list', ...options });

export const createChart = (data: number[], options: { title?: string } = {}) => 
  mcpUI.createUIResponse(data, { component: 'chart', ...options });

export const createAuto = (data: any, options: { title?: string } = {}) => 
  mcpUI.createUIResponse(data, { component: 'auto', ...options });

/**
 * Пример класса MCP сервера с интегрированным UI Generator
 */
export class ExampleMCPServer {
  private ui = new MCPUIHelper({
    defaultTheme: 'modern',
    enableInteractivity: true,
    enableResponsive: true,
    enableAccessibility: true
  });

  // Автоматическая генерация UI для задач
  async getTasks() {
    const tasks = [
      { id: 1, title: 'Задача 1', status: 'В работе', priority: 'Высокий' },
      { id: 2, title: 'Задача 2', status: 'Завершена', priority: 'Средний' },
    ];

    return this.ui.createUIResponse(tasks, {
      title: 'Список задач',
      component: 'table',
      uri: 'ui://tasks-table'
    });
  }

  // Создание дашборда
  async getDashboard() {
    const metrics = [
      { title: 'Всего задач', value: 156, change: 12, changeType: 'increase' as const },
      { title: 'Завершено', value: 89, change: -5, changeType: 'decrease' as const },
      { title: 'В работе', value: 23, change: 8, changeType: 'increase' as const },
      { title: 'Эффективность', value: 87, format: 'percentage' as const }
    ];

    return this.ui.createDashboard(metrics, {
      title: 'Панель управления проектом'
    });
  }

  // Создание формы
  async createTaskForm() {
    const fields = [
      { name: 'title', label: 'Название задачи', type: 'text' as const, required: true },
      { name: 'description', label: 'Описание', type: 'textarea' as const },
      { name: 'priority', label: 'Приоритет', type: 'select' as const, options: ['Низкий', 'Средний', 'Высокий'] },
      { name: 'assignee', label: 'Исполнитель', type: 'text' as const }
    ];

    return this.ui.createForm(fields, {
      title: 'Создание новой задачи',
      submitLabel: 'Создать задачу'
    });
  }
}