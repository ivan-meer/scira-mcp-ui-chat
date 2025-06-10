/**
 * Автоматический генератор UI интерфейсов для MCP серверов
 * Создаёт интерактивные компоненты на основе данных и метаданных
 */

export interface DataTypeSchema {
  type: 'object' | 'array' | 'string' | 'number' | 'boolean' | 'date' | 'unknown';
  properties?: Record<string, DataTypeSchema>;
  items?: DataTypeSchema;
  format?: string;
  metadata?: UIMetadata;
}

export interface UIMetadata {
  displayName?: string;
  description?: string;
  component?: ComponentType;
  validation?: ValidationRules;
  styling?: StyleConfig;
  interactions?: InteractionConfig;
}

export type ComponentType = 'table' | 'card' | 'list' | 'form' | 'chart' | 'text' | 'auto';

export interface ValidationRules {
  required?: boolean;
  min?: number;
  max?: number;
  pattern?: string;
}

export interface StyleConfig {
  theme?: 'light' | 'dark' | 'auto';
  colors?: {
    primary?: string;
    secondary?: string;
    accent?: string;
  };
  spacing?: 'compact' | 'normal' | 'spacious';
}

export interface InteractionConfig {
  actions?: ActionConfig[];
  clickable?: boolean;
  sortable?: boolean;
  filterable?: boolean;
}

export interface ActionConfig {
  label: string;
  action: string;
  params?: string[];
  style?: 'primary' | 'secondary' | 'danger';
}

export interface ComponentDefinition {
  type: ComponentType;
  data: any;
  schema: DataTypeSchema;
  template: string;
  styles: string[];
  scripts: string[];
}

export interface GenerationConfig {
  component?: ComponentType;
  theme?: string;
  interactive?: boolean;
  responsive?: boolean;
  accessibility?: boolean;
}

export class UIGenerator {
  private templates: Map<ComponentType, string> = new Map();
  private themes: Map<string, StyleConfig> = new Map();

  constructor() {
    this.initializeTemplates();
    this.initializeThemes();
  }

  /**
   * Основной метод генерации UI
   */
  generate(data: any, config: GenerationConfig = {}): string {
    // 1. Анализ данных и создание схемы
    const schema = this.analyzeData(data);
    
    // 2. Выбор компонента
    const componentType = config.component === 'auto' || !config.component 
      ? this.selectComponent(schema) 
      : config.component;
    
    // 3. Генерация определения компонента
    const component = this.generateComponent(data, schema, componentType);
    
    // 4. Применение конфигурации
    const enhanced = this.applyConfiguration(component, config);
    
    // 5. Рендеринг в HTML
    return this.renderToHTML(enhanced);
  }

  /**
   * Анализ структуры данных
   */
  private analyzeData(data: any): DataTypeSchema {
    if (data === null || data === undefined) {
      return { type: 'unknown' };
    }

    if (Array.isArray(data)) {
      const itemSchema: DataTypeSchema = data.length > 0 ? this.analyzeData(data[0]) : { type: 'unknown' };
      return {
        type: 'array',
        items: itemSchema
      };
    }

    if (typeof data === 'object') {
      const properties: Record<string, DataTypeSchema> = {};
      for (const [key, value] of Object.entries(data)) {
        properties[key] = this.analyzeData(value);
      }
      return {
        type: 'object',
        properties
      };
    }

    if (typeof data === 'string') {
      // Определение формата строки
      if (this.isDate(data)) {
        return { type: 'date', format: 'datetime' };
      }
      if (this.isEmail(data)) {
        return { type: 'string', format: 'email' };
      }
      if (this.isURL(data)) {
        return { type: 'string', format: 'url' };
      }
      return { type: 'string' };
    }

    if (typeof data === 'number') {
      return { type: 'number' };
    }

    if (typeof data === 'boolean') {
      return { type: 'boolean' };
    }

    return { type: 'unknown' };
  }

  /**
   * Умный выбор компонента на основе схемы данных
   */
  private selectComponent(schema: DataTypeSchema): ComponentType {
    // Массив объектов
    if (schema.type === 'array' && schema.items?.type === 'object') {
      const properties = Object.keys(schema.items.properties || {});
      
      // Много полей → таблица
      if (properties.length > 5) {
        return 'table';
      }
      
      // Несколько полей → список карточек
      if (properties.length > 2) {
        return 'list';
      }
      
      // Мало полей → простой список
      return 'list';
    }

    // Массив чисел → график
    if (schema.type === 'array' && schema.items?.type === 'number') {
      return 'chart';
    }

    // Простой массив → список
    if (schema.type === 'array') {
      return 'list';
    }

    // Объект с множеством полей
    if (schema.type === 'object') {
      const properties = Object.keys(schema.properties || {});
      
      // Много полей → карточка
      if (properties.length > 3) {
        return 'card';
      }
      
      // Мало полей → простой текст
      return 'text';
    }

    // По умолчанию
    return 'text';
  }

  /**
   * Генерация определения компонента
   */
  private generateComponent(data: any, schema: DataTypeSchema, type: ComponentType): ComponentDefinition {
    const template = this.templates.get(type) || this.templates.get('text')!;
    
    return {
      type,
      data,
      schema,
      template,
      styles: this.getComponentStyles(type),
      scripts: this.getComponentScripts(type)
    };
  }

  /**
   * Применение конфигурации к компоненту
   */
  private applyConfiguration(component: ComponentDefinition, config: GenerationConfig): ComponentDefinition {
    // Применение темы
    if (config.theme) {
      const themeConfig = this.themes.get(config.theme);
      if (themeConfig) {
        component.styles.push(this.generateThemeCSS(themeConfig));
      }
    }

    // Добавление интерактивности
    if (config.interactive) {
      component.scripts.push(this.getInteractivityScript());
    }

    // Добавление адаптивности
    if (config.responsive) {
      component.styles.push(this.getResponsiveCSS());
    }

    // Добавление доступности
    if (config.accessibility) {
      component.styles.push(this.getAccessibilityCSS());
    }

    return component;
  }

  /**
   * Рендеринг компонента в HTML
   */
  private renderToHTML(component: ComponentDefinition): string {
    const { data, template, styles, scripts } = component;
    
    // Простая замена переменных в шаблоне
    let html = template;
    
    // Замена основных переменных
    html = html.replace(/\{\{data\}\}/g, JSON.stringify(data));
    html = html.replace(/\{\{dataString\}\}/g, this.formatDataForDisplay(data, component.type));
    
    // Добавление стилей и скриптов
    const styleTag = styles.length > 0 ? `<style>${styles.join('\n')}</style>` : '';
    const scriptTag = scripts.length > 0 ? `<script>${scripts.join('\n')}</script>` : '';
    
    return `${styleTag}${html}${scriptTag}`;
  }

  /**
   * Форматирование данных для отображения
   */
  private formatDataForDisplay(data: any, type: ComponentType): string {
    switch (type) {
      case 'table':
        return this.formatAsTable(data);
      case 'card':
        return this.formatAsCard(data);
      case 'list':
        return this.formatAsList(data);
      case 'chart':
        return this.formatAsChart(data);
      default:
        return this.formatAsText(data);
    }
  }

  /**
   * Форматирование как таблица
   */
  private formatAsTable(data: any): string {
    if (!Array.isArray(data) || data.length === 0) {
      return '<p>Нет данных для отображения</p>';
    }

    const headers = Object.keys(data[0]);
    const headerRow = headers.map(h => `<th>${h}</th>`).join('');
    
    const rows = data.map(item => {
      const cells = headers.map(h => `<td>${item[h] || ''}</td>`).join('');
      return `<tr>${cells}</tr>`;
    }).join('');

    return `
      <table class="ui-table">
        <thead><tr>${headerRow}</tr></thead>
        <tbody>${rows}</tbody>
      </table>
    `;
  }

  /**
   * Форматирование как карточка
   */
  private formatAsCard(data: any): string {
    if (typeof data !== 'object' || data === null) {
      return `<div class="ui-card"><p>${String(data)}</p></div>`;
    }

    const fields = Object.entries(data).map(([key, value]) => {
      return `
        <div class="ui-field">
          <label class="ui-field-label">${key}</label>
          <span class="ui-field-value">${value}</span>
        </div>
      `;
    }).join('');

    return `
      <div class="ui-card">
        <div class="ui-card-content">
          ${fields}
        </div>
      </div>
    `;
  }

  /**
   * Форматирование как список
   */
  private formatAsList(data: any): string {
    if (!Array.isArray(data)) {
      return this.formatAsCard(data);
    }

    const items = data.map(item => {
      if (typeof item === 'object') {
        return this.formatAsCard(item);
      }
      return `<div class="ui-list-item">${String(item)}</div>`;
    }).join('');

    return `<div class="ui-list">${items}</div>`;
  }

  /**
   * Форматирование как график
   */
  private formatAsChart(data: any): string {
    // Простая реализация для числовых данных
    if (!Array.isArray(data)) {
      return '<p>Данные не подходят для графика</p>';
    }

    const values = data.filter(item => typeof item === 'number');
    if (values.length === 0) {
      return '<p>Нет числовых данных для графика</p>';
    }

    const max = Math.max(...values);
    const bars = values.map((value, index) => {
      const height = (value / max) * 100;
      return `
        <div class="ui-chart-bar" style="height: ${height}%">
          <span class="ui-chart-value">${value}</span>
        </div>
      `;
    }).join('');

    return `
      <div class="ui-chart">
        <div class="ui-chart-bars">${bars}</div>
      </div>
    `;
  }

  /**
   * Форматирование как текст
   */
  private formatAsText(data: any): string {
    if (typeof data === 'string') {
      return `<p class="ui-text">${data}</p>`;
    }
    
    return `<pre class="ui-text-data">${JSON.stringify(data, null, 2)}</pre>`;
  }

  /**
   * Инициализация шаблонов
   */
  private initializeTemplates(): void {
    this.templates.set('table', `
      <div class="ui-component ui-table-container">
        {{dataString}}
      </div>
    `);

    this.templates.set('card', `
      <div class="ui-component ui-card-container">
        {{dataString}}
      </div>
    `);

    this.templates.set('list', `
      <div class="ui-component ui-list-container">
        {{dataString}}
      </div>
    `);

    this.templates.set('chart', `
      <div class="ui-component ui-chart-container">
        {{dataString}}
      </div>
    `);

    this.templates.set('text', `
      <div class="ui-component ui-text-container">
        {{dataString}}
      </div>
    `);
  }

  /**
   * Инициализация тем
   */
  private initializeThemes(): void {
    this.themes.set('modern', {
      theme: 'light',
      colors: {
        primary: '#007bff',
        secondary: '#6c757d',
        accent: '#28a745'
      },
      spacing: 'normal'
    });

    this.themes.set('dark', {
      theme: 'dark',
      colors: {
        primary: '#0d6efd',
        secondary: '#6c757d',
        accent: '#198754'
      },
      spacing: 'normal'
    });
  }

  /**
   * Получение стилей компонента
   */
  private getComponentStyles(type: ComponentType): string[] {
    const baseStyles = `
      .ui-component {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        margin: 16px 0;
        border-radius: 8px;
        overflow: hidden;
      }
      
      .ui-table {
        width: 100%;
        border-collapse: collapse;
        background: white;
      }
      
      .ui-table th,
      .ui-table td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #dee2e6;
      }
      
      .ui-table th {
        background-color: #f8f9fa;
        font-weight: 600;
      }
      
      .ui-card {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
      }
      
      .ui-field {
        display: flex;
        justify-content: space-between;
        margin: 8px 0;
      }
      
      .ui-field-label {
        font-weight: 600;
        color: #495057;
      }
      
      .ui-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }
      
      .ui-list-item {
        padding: 8px 12px;
        background: #f8f9fa;
        border-radius: 4px;
      }
      
      .ui-chart {
        height: 200px;
        padding: 16px;
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
      }
      
      .ui-chart-bars {
        display: flex;
        align-items: flex-end;
        height: 100%;
        gap: 4px;
      }
      
      .ui-chart-bar {
        flex: 1;
        background: #007bff;
        min-height: 4px;
        border-radius: 2px 2px 0 0;
        position: relative;
        display: flex;
        align-items: flex-end;
        justify-content: center;
      }
      
      .ui-chart-value {
        position: absolute;
        bottom: 100%;
        font-size: 12px;
        color: #495057;
      }
      
      .ui-text {
        padding: 16px;
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
      }
      
      .ui-text-data {
        padding: 16px;
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        overflow-x: auto;
        font-size: 14px;
      }
    `;

    return [baseStyles];
  }

  /**
   * Получение скриптов компонента
   */
  private getComponentScripts(type: ComponentType): string[] {
    return [];
  }

  /**
   * Генерация CSS темы
   */
  private generateThemeCSS(theme: StyleConfig): string {
    return `
      .ui-component {
        --ui-primary: ${theme.colors?.primary || '#007bff'};
        --ui-secondary: ${theme.colors?.secondary || '#6c757d'};
        --ui-accent: ${theme.colors?.accent || '#28a745'};
      }
    `;
  }

  /**
   * Скрипт интерактивности
   */
  private getInteractivityScript(): string {
    return `
      // Базовая интерактивность для UI компонентов
      console.log('UI Generator: интерактивность активирована');
    `;
  }

  /**
   * CSS адаптивности
   */
  private getResponsiveCSS(): string {
    return `
      @media (max-width: 768px) {
        .ui-table {
          font-size: 14px;
        }
        .ui-table th,
        .ui-table td {
          padding: 8px;
        }
        .ui-chart {
          height: 150px;
        }
      }
    `;
  }

  /**
   * CSS доступности
   */
  private getAccessibilityCSS(): string {
    return `
      .ui-component:focus-within {
        outline: 2px solid var(--ui-primary, #007bff);
        outline-offset: 2px;
      }
      
      @media (prefers-reduced-motion: reduce) {
        .ui-component * {
          animation-duration: 0.01ms !important;
          animation-iteration-count: 1 !important;
          transition-duration: 0.01ms !important;
        }
      }
    `;
  }

  // Вспомогательные методы для определения форматов
  private isDate(str: string): boolean {
    return !isNaN(Date.parse(str));
  }

  private isEmail(str: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(str);
  }

  private isURL(str: string): boolean {
    try {
      new URL(str);
      return true;
    } catch {
      return false;
    }
  }
}