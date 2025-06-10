#!/usr/bin/env python3
"""
Демо MCP сервер для демонстрации возможностей UI Generator
Создаёт интерактивные интерфейсы для различных типов данных
"""

import asyncio
import json
import logging
from typing import Any, Dict, List
from datetime import datetime, timedelta
import random

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("demo-ui-generator-server")

class UIGeneratorDemoServer:
    """Демо сервер с примерами UI Generator"""
    
    def __init__(self):
        self.name = "UI Generator Demo Server"
        self.version = "1.0.0"
        
        # Тестовые данные
        self.users_data = [
            {
                "id": 1,
                "name": "Иван Петров",
                "email": "ivan.petrov@company.com",
                "department": "Разработка",
                "position": "Senior Developer",
                "salary": 120000,
                "active": True,
                "joinDate": "2022-03-15",
                "skills": ["JavaScript", "React", "Node.js", "PostgreSQL"],
                "tasksCompleted": 145,
                "efficiency": 92
            },
            {
                "id": 2,
                "name": "Мария Сидорова",
                "email": "maria.sidorova@company.com",
                "department": "Дизайн",
                "position": "UI/UX Designer",
                "salary": 95000,
                "active": True,
                "joinDate": "2023-01-20",
                "skills": ["Figma", "Adobe XD", "Sketch", "Prototyping"],
                "tasksCompleted": 98,
                "efficiency": 88
            },
            {
                "id": 3,
                "name": "Алексей Козлов",
                "email": "alex.kozlov@company.com",
                "department": "QA",
                "position": "QA Engineer",
                "salary": 85000,
                "active": True,
                "joinDate": "2021-08-10",
                "skills": ["Selenium", "Cypress", "Jest", "API Testing"],
                "tasksCompleted": 176,
                "efficiency": 95
            },
            {
                "id": 4,
                "name": "Анна Николаева",
                "email": "anna.nikolaeva@company.com",
                "department": "Менеджмент",
                "position": "Project Manager",
                "salary": 110000,
                "active": True,
                "joinDate": "2020-11-05",
                "skills": ["Jira", "Scrum", "Leadership", "Planning"],
                "tasksCompleted": 234,
                "efficiency": 89
            }
        ]
        
        self.tasks_data = [
            {
                "id": "TASK-001",
                "title": "Реализовать систему аутентификации",
                "description": "Добавить JWT токены и OAuth2 интеграцию",
                "status": "В работе",
                "priority": "Высокий",
                "assignee": "Иван Петров",
                "reporter": "Анна Николаева",
                "created": "2024-01-10T09:00:00Z",
                "updated": "2024-01-13T14:30:00Z",
                "dueDate": "2024-01-20T23:59:59Z",
                "progress": 75,
                "estimatedHours": 40,
                "loggedHours": 30,
                "tags": ["backend", "security", "critical"],
                "comments": 12
            },
            {
                "id": "TASK-002",
                "title": "Создать мобильную версию дашборда",
                "description": "Адаптивный дизайн для планшетов и телефонов",
                "status": "Новая",
                "priority": "Средний",
                "assignee": "Мария Сидорова",
                "reporter": "Иван Петров",
                "created": "2024-01-12T11:15:00Z",
                "updated": "2024-01-12T11:15:00Z",
                "dueDate": "2024-01-25T23:59:59Z",
                "progress": 0,
                "estimatedHours": 32,
                "loggedHours": 0,
                "tags": ["frontend", "mobile", "ui"],
                "comments": 3
            },
            {
                "id": "TASK-003",
                "title": "Настроить автоматические тесты",
                "description": "CI/CD pipeline с автоматическим тестированием",
                "status": "Завершена",
                "priority": "Средний",
                "assignee": "Алексей Козлов",
                "reporter": "Анна Николаева",
                "created": "2024-01-05T10:00:00Z",
                "updated": "2024-01-11T16:45:00Z",
                "dueDate": "2024-01-15T23:59:59Z",
                "progress": 100,
                "estimatedHours": 24,
                "loggedHours": 26,
                "tags": ["testing", "devops", "automation"],
                "comments": 8
            }
        ]
        
        self.project_data = {
            "info": {
                "name": "Проект Alpha",
                "description": "Система управления задачами нового поколения",
                "status": "В разработке",
                "startDate": "2024-01-01",
                "endDate": "2024-06-30",
                "budget": 2500000,
                "spent": 1250000,
                "currency": "RUB",
                "completion": 65
            },
            "team": [
                {"name": "Иван Петров", "role": "Tech Lead", "load": 100, "efficiency": 92},
                {"name": "Мария Сидорова", "role": "Designer", "load": 80, "efficiency": 88},
                {"name": "Алексей Козлов", "role": "QA Engineer", "load": 60, "efficiency": 95},
                {"name": "Анна Николаева", "role": "Project Manager", "load": 90, "efficiency": 89}
            ],
            "metrics": {
                "totalTasks": 156,
                "completedTasks": 89,
                "inProgressTasks": 23,
                "blockedTasks": 5,
                "efficiency": 87,
                "velocity": 15.3,
                "quality": 94
            }
        }

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Получить список доступных инструментов"""
        return [
            {
                "name": "show_users_table",
                "description": "Показать таблицу пользователей (демо UI Generator - Table)"
            },
            {
                "name": "show_user_profile",
                "description": "Показать профиль пользователя (демо UI Generator - Card)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "userId": {
                            "type": "integer",
                            "description": "ID пользователя (1-4)"
                        }
                    }
                }
            },
            {
                "name": "show_tasks_list",
                "description": "Показать список задач (демо UI Generator - List)"
            },
            {
                "name": "show_project_dashboard",
                "description": "Показать дашборд проекта (демо UI Generator - Dashboard)"
            },
            {
                "name": "show_statistics_chart",
                "description": "Показать график статистики (демо UI Generator - Chart)"
            },
            {
                "name": "create_user_form",
                "description": "Показать форму создания пользователя (демо UI Generator - Form)"
            },
            {
                "name": "show_notifications_demo",
                "description": "Показать различные уведомления (демо UI Generator - Notifications)"
            },
            {
                "name": "auto_generate_interface",
                "description": "Автоматическая генерация интерфейса для любых данных",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "dataType": {
                            "type": "string",
                            "enum": ["users", "tasks", "project", "random"],
                            "description": "Тип данных для генерации"
                        }
                    }
                }
            },
            {
                "name": "performance_test",
                "description": "Тест производительности UI Generator"
            }
        ]

    def create_ui_response(self, data: Any, title: str = "", component_type: str = "auto") -> Dict[str, Any]:
        """Создать ответ с UI используя встроенный генератор"""
        
        # Определяем тип компонента автоматически если не указан
        if component_type == "auto":
            if isinstance(data, list) and len(data) > 0:
                if isinstance(data[0], dict):
                    # Массив объектов
                    fields_count = len(data[0].keys()) if data[0] else 0
                    component_type = "table" if fields_count > 5 else "list"
                elif isinstance(data[0], (int, float)):
                    # Массив чисел
                    component_type = "chart"
                else:
                    component_type = "list"
            elif isinstance(data, dict):
                component_type = "card"
            else:
                component_type = "text"

        # Генерируем HTML в зависимости от типа компонента
        if component_type == "table":
            html = self.generate_table(data, title)
        elif component_type == "card":
            html = self.generate_card(data, title)
        elif component_type == "list":
            html = self.generate_list(data, title)
        elif component_type == "chart":
            html = self.generate_chart(data, title)
        elif component_type == "dashboard":
            html = self.generate_dashboard(data, title)
        elif component_type == "form":
            html = self.generate_form(data, title)
        elif component_type == "notification":
            html = self.generate_notification(data, title)
        else:
            html = self.generate_text(data, title)

        return {
            "content": [
                {
                    "type": "resource",
                    "resource": {
                        "uri": f"ui://demo-{component_type}-{datetime.now().timestamp()}",
                        "mimeType": "text/html",
                        "text": html
                    }
                }
            ]
        }

    def generate_table(self, data: List[Dict], title: str) -> str:
        """Генерация таблицы"""
        if not data:
            return f"<div class='no-data'>Нет данных для отображения</div>"
        
        headers = list(data[0].keys())
        header_row = "".join([f"<th>{self.format_header(h)}</th>" for h in headers])
        
        rows = []
        for item in data:
            cells = []
            for header in headers:
                value = item.get(header, "")
                formatted_value = self.format_cell_value(value, header)
                cells.append(f"<td>{formatted_value}</td>")
            rows.append(f"<tr>{''.join(cells)}</tr>")
        
        return f"""
        <style>
            .ui-container {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 20px 0;
            }}
            .ui-title {{
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 16px;
                color: #333;
            }}
            .ui-table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .ui-table th {{
                background: #f8f9fa;
                padding: 12px;
                text-align: left;
                font-weight: 600;
                color: #495057;
                border-bottom: 2px solid #dee2e6;
            }}
            .ui-table td {{
                padding: 12px;
                border-bottom: 1px solid #dee2e6;
                color: #212529;
            }}
            .ui-table tr:hover {{
                background: #f8f9fa;
            }}
            .status-badge {{
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 500;
            }}
            .status-active {{ background: #d4edda; color: #155724; }}
            .status-inactive {{ background: #f8d7da; color: #721c24; }}
            .status-work {{ background: #fff3cd; color: #856404; }}
            .status-done {{ background: #d1ecf1; color: #0c5460; }}
            .status-new {{ background: #e2e3e5; color: #495057; }}
        </style>
        <div class="ui-container">
            {f'<h2 class="ui-title">{title}</h2>' if title else ''}
            <table class="ui-table">
                <thead><tr>{header_row}</tr></thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """

    def generate_card(self, data: Dict, title: str) -> str:
        """Генерация карточки"""
        fields = []
        for key, value in data.items():
            formatted_key = self.format_header(key)
            formatted_value = self.format_cell_value(value, key)
            fields.append(f"""
                <div class="ui-field">
                    <label class="ui-field-label">{formatted_key}</label>
                    <span class="ui-field-value">{formatted_value}</span>
                </div>
            """)
        
        return f"""
        <style>
            .ui-container {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 20px 0;
            }}
            .ui-title {{
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 16px;
                color: #333;
            }}
            .ui-card {{
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                max-width: 500px;
            }}
            .ui-field {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 12px 0;
                padding: 8px 0;
                border-bottom: 1px solid #f1f3f4;
            }}
            .ui-field:last-child {{
                border-bottom: none;
            }}
            .ui-field-label {{
                font-weight: 600;
                color: #495057;
                min-width: 120px;
            }}
            .ui-field-value {{
                color: #212529;
                text-align: right;
            }}
        </style>
        <div class="ui-container">
            {f'<h2 class="ui-title">{title}</h2>' if title else ''}
            <div class="ui-card">
                {''.join(fields)}
            </div>
        </div>
        """

    def generate_dashboard(self, data: Dict, title: str) -> str:
        """Генерация дашборда"""
        metrics = data.get('metrics', {})
        info = data.get('info', {})
        team = data.get('team', [])
        
        metric_cards = []
        if metrics:
            metric_items = [
                ('Всего задач', metrics.get('totalTasks', 0), 'primary'),
                ('Завершено', metrics.get('completedTasks', 0), 'success'),
                ('В работе', metrics.get('inProgressTasks', 0), 'warning'),
                ('Заблокировано', metrics.get('blockedTasks', 0), 'danger'),
                ('Эффективность', f"{metrics.get('efficiency', 0)}%", 'info'),
                ('Скорость', metrics.get('velocity', 0), 'secondary')
            ]
            
            for label, value, color in metric_items:
                metric_cards.append(f"""
                    <div class="metric-card metric-{color}">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                    </div>
                """)
        
        team_cards = []
        for member in team:
            team_cards.append(f"""
                <div class="team-card">
                    <div class="team-name">{member.get('name', '')}</div>
                    <div class="team-role">{member.get('role', '')}</div>
                    <div class="team-stats">
                        <span>Загрузка: {member.get('load', 0)}%</span>
                        <span>Эффективность: {member.get('efficiency', 0)}%</span>
                    </div>
                </div>
            """)
        
        return f"""
        <style>
            .ui-container {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 20px 0;
            }}
            .ui-title {{
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 20px;
                color: #333;
            }}
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 16px;
                margin-bottom: 24px;
            }}
            .metric-card {{
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 16px;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .metric-label {{
                font-size: 12px;
                color: #6c757d;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .metric-value {{
                font-size: 24px;
                font-weight: 700;
                color: #333;
            }}
            .metric-primary {{ border-left: 4px solid #007bff; }}
            .metric-success {{ border-left: 4px solid #28a745; }}
            .metric-warning {{ border-left: 4px solid #ffc107; }}
            .metric-danger {{ border-left: 4px solid #dc3545; }}
            .metric-info {{ border-left: 4px solid #17a2b8; }}
            .metric-secondary {{ border-left: 4px solid #6c757d; }}
            .team-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 16px;
            }}
            .team-card {{
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 16px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .team-name {{
                font-weight: 600;
                color: #333;
                margin-bottom: 4px;
            }}
            .team-role {{
                color: #6c757d;
                font-size: 14px;
                margin-bottom: 8px;
            }}
            .team-stats {{
                display: flex;
                flex-direction: column;
                gap: 4px;
            }}
            .team-stats span {{
                font-size: 12px;
                color: #495057;
            }}
        </style>
        <div class="ui-container">
            {f'<h2 class="ui-title">{title}</h2>' if title else ''}
            <div class="metrics-grid">
                {''.join(metric_cards)}
            </div>
            {f'<h3>Команда проекта</h3><div class="team-grid">{"".join(team_cards)}</div>' if team_cards else ''}
        </div>
        """

    def generate_chart(self, data: List, title: str) -> str:
        """Генерация графика"""
        if not data or not all(isinstance(x, (int, float)) for x in data):
            return "<div>Некорректные данные для графика</div>"
        
        max_val = max(data) if data else 1
        bars = []
        
        for i, value in enumerate(data):
            height = (value / max_val) * 100 if max_val > 0 else 0
            bars.append(f"""
                <div class="chart-bar">
                    <div class="chart-bar-fill" style="height: {height}%"></div>
                    <div class="chart-bar-label">{value}</div>
                    <div class="chart-bar-index">{i+1}</div>
                </div>
            """)
        
        return f"""
        <style>
            .ui-container {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 20px 0;
            }}
            .ui-title {{
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 16px;
                color: #333;
            }}
            .chart-container {{
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .chart {{
                display: flex;
                align-items: flex-end;
                height: 200px;
                gap: 8px;
                margin: 20px 0;
            }}
            .chart-bar {{
                flex: 1;
                display: flex;
                flex-direction: column;
                align-items: center;
                height: 100%;
                position: relative;
            }}
            .chart-bar-fill {{
                width: 100%;
                background: linear-gradient(to top, #007bff, #0056b3);
                border-radius: 4px 4px 0 0;
                min-height: 4px;
                transition: all 0.3s ease;
            }}
            .chart-bar:hover .chart-bar-fill {{
                background: linear-gradient(to top, #0056b3, #004085);
            }}
            .chart-bar-label {{
                position: absolute;
                top: -20px;
                font-size: 12px;
                font-weight: 600;
                color: #495057;
            }}
            .chart-bar-index {{
                margin-top: 8px;
                font-size: 12px;
                color: #6c757d;
            }}
        </style>
        <div class="ui-container">
            {f'<h2 class="ui-title">{title}</h2>' if title else ''}
            <div class="chart-container">
                <div class="chart">
                    {''.join(bars)}
                </div>
            </div>
        </div>
        """

    def generate_list(self, data: List, title: str) -> str:
        """Генерация списка"""
        items = []
        for item in data:
            if isinstance(item, dict):
                # Объект - создаём мини-карточку
                fields = []
                for key, value in list(item.items())[:4]:  # Показываем только первые 4 поля
                    if key != 'id':
                        formatted_value = self.format_cell_value(value, key)
                        fields.append(f"<span class='item-field'><strong>{self.format_header(key)}:</strong> {formatted_value}</span>")
                
                items.append(f"""
                    <div class="list-item">
                        <div class="item-header">{item.get('title', item.get('name', f'Элемент {item.get("id", "")}')))}</div>
                        <div class="item-content">{'<br>'.join(fields)}</div>
                    </div>
                """)
            else:
                # Простое значение
                items.append(f'<div class="list-item simple">{item}</div>')
        
        return f"""
        <style>
            .ui-container {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 20px 0;
            }}
            .ui-title {{
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 16px;
                color: #333;
            }}
            .list-container {{
                display: flex;
                flex-direction: column;
                gap: 12px;
            }}
            .list-item {{
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 16px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                transition: all 0.2s ease;
            }}
            .list-item:hover {{
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transform: translateY(-1px);
            }}
            .list-item.simple {{
                padding: 12px 16px;
                color: #495057;
            }}
            .item-header {{
                font-weight: 600;
                color: #333;
                margin-bottom: 8px;
                font-size: 16px;
            }}
            .item-content {{
                color: #6c757d;
                font-size: 14px;
                line-height: 1.5;
            }}
            .item-field {{
                display: inline-block;
                margin-right: 16px;
            }}
        </style>
        <div class="ui-container">
            {f'<h2 class="ui-title">{title}</h2>' if title else ''}
            <div class="list-container">
                {''.join(items)}
            </div>
        </div>
        """

    def generate_form(self, fields: List[Dict], title: str) -> str:
        """Генерация формы"""
        form_fields = []
        for field in fields:
            field_name = field.get('name', '')
            field_label = field.get('label', field_name)
            field_type = field.get('type', 'text')
            required = field.get('required', False)
            options = field.get('options', [])
            
            if field_type == 'select':
                options_html = ''.join([f'<option value="{opt}">{opt}</option>' for opt in options])
                input_html = f'<select name="{field_name}" {"required" if required else ""}>{options_html}</select>'
            elif field_type == 'textarea':
                input_html = f'<textarea name="{field_name}" rows="3" {"required" if required else ""}></textarea>'
            else:
                input_html = f'<input type="{field_type}" name="{field_name}" {"required" if required else ""}>'
            
            form_fields.append(f"""
                <div class="form-field">
                    <label for="{field_name}">{field_label}{' *' if required else ''}</label>
                    {input_html}
                </div>
            """)
        
        return f"""
        <style>
            .ui-container {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 20px 0;
            }}
            .ui-title {{
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 16px;
                color: #333;
            }}
            .form-container {{
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 24px;
                max-width: 500px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .form-field {{
                margin-bottom: 20px;
            }}
            .form-field label {{
                display: block;
                margin-bottom: 6px;
                font-weight: 500;
                color: #495057;
            }}
            .form-field input,
            .form-field select,
            .form-field textarea {{
                width: 100%;
                padding: 10px 12px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
                box-sizing: border-box;
                transition: border-color 0.15s ease-in-out;
            }}
            .form-field input:focus,
            .form-field select:focus,
            .form-field textarea:focus {{
                outline: none;
                border-color: #007bff;
                box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
            }}
            .form-submit {{
                background: #007bff;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 4px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                transition: background-color 0.15s ease-in-out;
            }}
            .form-submit:hover {{
                background: #0056b3;
            }}
        </style>
        <div class="ui-container">
            {f'<h2 class="ui-title">{title}</h2>' if title else ''}
            <div class="form-container">
                <form>
                    {''.join(form_fields)}
                    <button type="submit" class="form-submit">Отправить</button>
                </form>
            </div>
        </div>
        """

    def generate_notification(self, notifications: List[Dict], title: str) -> str:
        """Генерация уведомлений"""
        notification_items = []
        for notif in notifications:
            notif_type = notif.get('type', 'info')
            notif_title = notif.get('title', '')
            notif_message = notif.get('message', '')
            
            type_classes = {
                'success': 'notif-success',
                'warning': 'notif-warning', 
                'error': 'notif-error',
                'info': 'notif-info'
            }
            
            notification_items.append(f"""
                <div class="notification {type_classes.get(notif_type, 'notif-info')}">
                    {f'<div class="notif-title">{notif_title}</div>' if notif_title else ''}
                    <div class="notif-message">{notif_message}</div>
                </div>
            """)
        
        return f"""
        <style>
            .ui-container {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 20px 0;
            }}
            .ui-title {{
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 16px;
                color: #333;
            }}
            .notifications-container {{
                display: flex;
                flex-direction: column;
                gap: 12px;
            }}
            .notification {{
                padding: 16px;
                border-radius: 8px;
                border-left: 4px solid;
            }}
            .notif-success {{
                background: #d4edda;
                border-color: #28a745;
                color: #155724;
            }}
            .notif-warning {{
                background: #fff3cd;
                border-color: #ffc107;
                color: #856404;
            }}
            .notif-error {{
                background: #f8d7da;
                border-color: #dc3545;
                color: #721c24;
            }}
            .notif-info {{
                background: #d1ecf1;
                border-color: #17a2b8;
                color: #0c5460;
            }}
            .notif-title {{
                font-weight: 600;
                margin-bottom: 6px;
            }}
            .notif-message {{
                line-height: 1.4;
            }}
        </style>
        <div class="ui-container">
            {f'<h2 class="ui-title">{title}</h2>' if title else ''}
            <div class="notifications-container">
                {''.join(notification_items)}
            </div>
        </div>
        """

    def generate_text(self, data: Any, title: str) -> str:
        """Генерация текста"""
        if isinstance(data, (dict, list)):
            content = json.dumps(data, ensure_ascii=False, indent=2)
            content_class = "text-json"
        else:
            content = str(data)
            content_class = "text-simple"
        
        return f"""
        <style>
            .ui-container {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 20px 0;
            }}
            .ui-title {{
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 16px;
                color: #333;
            }}
            .text-container {{
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .text-json {{
                background: #f8f9fa;
                padding: 16px;
                border-radius: 4px;
                font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                font-size: 14px;
                white-space: pre-wrap;
                overflow-x: auto;
                color: #495057;
            }}
            .text-simple {{
                color: #212529;
                line-height: 1.6;
            }}
        </style>
        <div class="ui-container">
            {f'<h2 class="ui-title">{title}</h2>' if title else ''}
            <div class="text-container">
                <div class="{content_class}">{content}</div>
            </div>
        </div>
        """

    def format_header(self, header: str) -> str:
        """Форматирование заголовков"""
        translations = {
            'id': 'ID',
            'name': 'Имя',
            'email': 'Email',
            'department': 'Отдел',
            'position': 'Должность',
            'salary': 'Зарплата',
            'active': 'Активен',
            'joinDate': 'Дата найма',
            'skills': 'Навыки',
            'tasksCompleted': 'Задач выполнено',
            'efficiency': 'Эффективность',
            'title': 'Название',
            'description': 'Описание',
            'status': 'Статус',
            'priority': 'Приоритет',
            'assignee': 'Исполнитель',
            'reporter': 'Автор',
            'created': 'Создана',
            'updated': 'Обновлена',
            'dueDate': 'Срок',
            'progress': 'Прогресс',
            'estimatedHours': 'Часов оценка',
            'loggedHours': 'Часов потрачено',
            'tags': 'Теги',
            'comments': 'Комментарии'
        }
        return translations.get(header, header)

    def format_cell_value(self, value: Any, header: str) -> str:
        """Форматирование значений ячеек"""
        if value is None:
            return ""
        
        if header in ['salary']:
            return f"{value:,} ₽"
        elif header in ['efficiency', 'progress']:
            return f"{value}%"
        elif header == 'active':
            return f"<span class='status-badge status-{'active' if value else 'inactive'}'>{'Да' if value else 'Нет'}</span>"
        elif header == 'status':
            status_map = {
                'В работе': 'work',
                'Завершена': 'done',
                'Новая': 'new'
            }
            status_class = status_map.get(value, 'new')
            return f"<span class='status-badge status-{status_class}'>{value}</span>"
        elif header in ['joinDate', 'created', 'updated', 'dueDate']:
            if isinstance(value, str) and 'T' in value:
                # ISO формат
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    return dt.strftime('%d.%m.%Y')
                except:
                    return value
            return value
        elif isinstance(value, list):
            return ", ".join(str(item) for item in value[:3]) + ("..." if len(value) > 3 else "")
        
        return str(value)

    # Методы инструментов
    async def show_users_table(self, **kwargs) -> Dict[str, Any]:
        """Показать таблицу пользователей"""
        return self.create_ui_response(
            self.users_data,
            "Список сотрудников компании",
            "table"
        )

    async def show_user_profile(self, userId: int = 1, **kwargs) -> Dict[str, Any]:
        """Показать профиль пользователя"""
        user = next((u for u in self.users_data if u['id'] == userId), self.users_data[0])
        return self.create_ui_response(
            user,
            f"Профиль: {user['name']}",
            "card"
        )

    async def show_tasks_list(self, **kwargs) -> Dict[str, Any]:
        """Показать список задач"""
        return self.create_ui_response(
            self.tasks_data,
            "Активные задачи проекта",
            "list"
        )

    async def show_project_dashboard(self, **kwargs) -> Dict[str, Any]:
        """Показать дашборд проекта"""
        return self.create_ui_response(
            self.project_data,
            "Дашборд проекта Alpha",
            "dashboard"
        )

    async def show_statistics_chart(self, **kwargs) -> Dict[str, Any]:
        """Показать график статистики"""
        # Генерируем случайную статистику
        stats = [random.randint(10, 50) for _ in range(12)]
        return self.create_ui_response(
            stats,
            "Статистика активности по месяцам",
            "chart"
        )

    async def create_user_form(self, **kwargs) -> Dict[str, Any]:
        """Показать форму создания пользователя"""
        form_fields = [
            {"name": "name", "label": "Полное имя", "type": "text", "required": True},
            {"name": "email", "label": "Email адрес", "type": "email", "required": True},
            {"name": "department", "label": "Отдел", "type": "select", "options": ["Разработка", "Дизайн", "QA", "Менеджмент"]},
            {"name": "position", "label": "Должность", "type": "text", "required": True},
            {"name": "salary", "label": "Зарплата", "type": "number"},
            {"name": "skills", "label": "Навыки", "type": "textarea"}
        ]
        return self.create_ui_response(
            form_fields,
            "Добавление нового сотрудника",
            "form"
        )

    async def show_notifications_demo(self, **kwargs) -> Dict[str, Any]:
        """Показать различные уведомления"""
        notifications = [
            {
                "type": "success",
                "title": "Успех!",
                "message": "Пользователь успешно добавлен в систему."
            },
            {
                "type": "warning", 
                "title": "Внимание",
                "message": "Некоторые поля формы заполнены некорректно."
            },
            {
                "type": "error",
                "title": "Ошибка",
                "message": "Не удалось сохранить данные. Проверьте подключение к серверу."
            },
            {
                "type": "info",
                "title": "Информация",
                "message": "Система будет недоступна с 02:00 до 04:00 по МСК для обновления."
            }
        ]
        return self.create_ui_response(
            notifications,
            "Примеры уведомлений",
            "notification"
        )

    async def auto_generate_interface(self, dataType: str = "users", **kwargs) -> Dict[str, Any]:
        """Автоматическая генерация интерфейса"""
        data_map = {
            "users": self.users_data,
            "tasks": self.tasks_data,
            "project": self.project_data,
            "random": [random.randint(1, 100) for _ in range(10)]
        }
        
        data = data_map.get(dataType, self.users_data)
        return self.create_ui_response(
            data,
            f"Автоматически сгенерированный интерфейс для: {dataType}",
            "auto"
        )

    async def performance_test(self, **kwargs) -> Dict[str, Any]:
        """Тест производительности"""
        import time
        
        start_time = time.time()
        
        # Генерируем большой набор данных
        large_dataset = []
        for i in range(100):
            large_dataset.append({
                "id": i + 1,
                "name": f"Пользователь {i + 1}",
                "email": f"user{i + 1}@test.com",
                "department": random.choice(["IT", "HR", "Sales", "Marketing"]),
                "salary": random.randint(50000, 200000),
                "active": random.choice([True, False])
            })
        
        # Измеряем время генерации
        gen_start = time.time()
        response = self.create_ui_response(large_dataset, "Тест производительности (100 записей)", "table")
        gen_time = time.time() - gen_start
        
        total_time = time.time() - start_time
        
        # Добавляем информацию о производительности
        perf_info = {
            "records": len(large_dataset),
            "generation_time": f"{gen_time:.3f}",
            "total_time": f"{total_time:.3f}",
            "html_size": len(response["content"][0]["resource"]["text"]),
            "performance": "Отлично" if gen_time < 0.1 else "Хорошо" if gen_time < 0.5 else "Удовлетворительно"
        }
        
        # Возвращаем и данные, и информацию о производительности
        combined_response = response.copy()
        perf_html = self.generate_card(perf_info, "Результаты теста производительности")
        combined_response["content"][0]["resource"]["text"] = perf_html + "<br>" + response["content"][0]["resource"]["text"]
        
        return combined_response

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка запросов к серверу"""
        method = request.get("method", "")
        params = request.get("params", {})
        
        if method == "tools/list":
            return {
                "tools": self.get_available_tools()
            }
        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            
            # Маппинг инструментов
            tool_methods = {
                "show_users_table": self.show_users_table,
                "show_user_profile": self.show_user_profile,
                "show_tasks_list": self.show_tasks_list,
                "show_project_dashboard": self.show_project_dashboard,
                "show_statistics_chart": self.show_statistics_chart,
                "create_user_form": self.create_user_form,
                "show_notifications_demo": self.show_notifications_demo,
                "auto_generate_interface": self.auto_generate_interface,
                "performance_test": self.performance_test
            }
            
            if tool_name in tool_methods:
                try:
                    result = await tool_methods[tool_name](**arguments)
                    return {"content": result["content"]}
                except Exception as e:
                    logger.error(f"Error executing tool {tool_name}: {e}")
                    return {"content": [{"type": "text", "text": f"Ошибка выполнения инструмента: {str(e)}"}]}
            else:
                return {"content": [{"type": "text", "text": f"Неизвестный инструмент: {tool_name}"}]}
        
        return {"error": "Неподдерживаемый метод"}

if __name__ == "__main__":
    # Простой HTTP сервер для демонстрации
    import json
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    server = UIGeneratorDemoServer()
    
    class RequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                request = json.loads(post_data.decode('utf-8'))
                response = asyncio.run(server.handle_request(request))
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    print("Запуск демо сервера UI Generator на порту 8000...")
    print("Доступные инструменты:")
    for tool in server.get_available_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    
    httpd = HTTPServer(('localhost', 8000), RequestHandler)
    httpd.serve_forever()