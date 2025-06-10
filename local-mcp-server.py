#!/usr/bin/env python3
"""
Демо MCP сервер с автоматической генерацией UI интерфейсов
Демонстрирует возможности UI Generator для различных типов данных
"""

import json
import sys
import logging
from datetime import datetime, timedelta
import random
from typing import Any, Dict, List, Optional
import http.server
import socketserver
import threading
import time
import urllib.parse

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp-server.log'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger('demo-mcp-server')

class UIGenerator:
    """Упрощенная версия UI Generator для Python MCP сервера"""
    
    @staticmethod
    def generate_table(data: List[Dict], title: str = "", description: str = "") -> str:
        """Генерация HTML таблицы"""
        if not data:
            return f"""
            <div class="ui-component">
                <h3>{title}</h3>
                <p>Нет данных для отображения</p>
            </div>
            """
        
        headers = list(data[0].keys())
        header_row = ''.join(f'<th>{header}</th>' for header in headers)
        
        rows = []
        for item in data:
            cells = ''.join(f'<td>{item.get(header, "")}</td>' for header in headers)
            rows.append(f'<tr>{cells}</tr>')
        
        table_html = f"""
        <style>
            .ui-component {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 16px 0;
                border-radius: 8px;
                overflow: hidden;
            }}
            .ui-table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                overflow: hidden;
            }}
            .ui-table th,
            .ui-table td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #dee2e6;
            }}
            .ui-table th {{
                background-color: #f8f9fa;
                font-weight: 600;
                color: #495057;
            }}
            .ui-table tr:last-child td {{
                border-bottom: none;
            }}
            .ui-table tr:hover {{
                background-color: #f8f9fa;
            }}
            .ui-title {{
                margin: 0 0 16px 0;
                color: #333;
                font-size: 18px;
                font-weight: 600;
            }}
            .ui-description {{
                margin: 0 0 16px 0;
                color: #666;
                font-size: 14px;
            }}
        </style>
        <div class="ui-component">
            {f'<h3 class="ui-title">{title}</h3>' if title else ''}
            {f'<p class="ui-description">{description}</p>' if description else ''}
            <table class="ui-table">
                <thead><tr>{header_row}</tr></thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """
        
        return table_html
    
    @staticmethod
    def generate_card(data: Dict, title: str = "", description: str = "") -> str:
        """Генерация HTML карточки"""
        fields = []
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                value = json.dumps(value, ensure_ascii=False, indent=2)
            fields.append(f"""
                <div class="ui-field">
                    <label class="ui-field-label">{key}</label>
                    <span class="ui-field-value">{value}</span>
                </div>
            """)
        
        card_html = f"""
        <style>
            .ui-component {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 16px 0;
            }}
            .ui-card {{
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .ui-field {{
                display: flex;
                justify-content: space-between;
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
                flex: 1;
                word-break: break-word;
            }}
            .ui-title {{
                margin: 0 0 16px 0;
                color: #333;
                font-size: 18px;
                font-weight: 600;
            }}
            .ui-description {{
                margin: 0 0 16px 0;
                color: #666;
                font-size: 14px;
            }}
        </style>
        <div class="ui-component">
            {f'<h3 class="ui-title">{title}</h3>' if title else ''}
            {f'<p class="ui-description">{description}</p>' if description else ''}
            <div class="ui-card">
                {''.join(fields)}
            </div>
        </div>
        """
        
        return card_html
    
    @staticmethod
    def generate_dashboard(metrics: List[Dict], title: str = "") -> str:
        """Генерация дашборда с метриками"""
        metric_cards = []
        for metric in metrics:
            value = metric.get('value', 0)
            change = metric.get('change', 0)
            change_type = metric.get('changeType', 'neutral')
            
            # Форматирование изменения
            if change != 0:
                change_color = '#28a745' if change_type == 'increase' else '#dc3545' if change_type == 'decrease' else '#6c757d'
                change_text = f'<span style="color: {change_color}; font-size: 12px;">{"+" if change > 0 else ""}{change}%</span>'
            else:
                change_text = ''
            
            metric_cards.append(f"""
                <div class="metric-card">
                    <div class="metric-title">{metric.get('title', '')}</div>
                    <div class="metric-value">{value}</div>
                    {f'<div class="metric-change">{change_text}</div>' if change_text else ''}
                </div>
            """)
        
        dashboard_html = f"""
        <style>
            .ui-component {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 16px 0;
            }}
            .dashboard {{
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
            }}
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 16px;
                margin-top: 16px;
            }}
            .metric-card {{
                padding: 16px;
                background: #f8f9fa;
                border-radius: 8px;
                text-align: center;
                border: 1px solid #e9ecef;
            }}
            .metric-title {{
                font-size: 14px;
                color: #6c757d;
                margin-bottom: 8px;
            }}
            .metric-value {{
                font-size: 24px;
                font-weight: 700;
                color: #333;
                margin-bottom: 4px;
            }}
            .metric-change {{
                font-size: 12px;
            }}
            .ui-title {{
                margin: 0;
                color: #333;
                font-size: 18px;
                font-weight: 600;
            }}
        </style>
        <div class="ui-component">
            <div class="dashboard">
                {f'<h3 class="ui-title">{title}</h3>' if title else ''}
                <div class="metrics-grid">
                    {''.join(metric_cards)}
                </div>
            </div>
        </div>
        """
        
        return dashboard_html

class DemoMCPServer:
    """Демо MCP сервер с возможностями UI генерации"""
    
    def __init__(self):
        self.ui = UIGenerator()
        self.users_data = self._generate_users_data()
        self.tasks_data = self._generate_tasks_data()
        self.projects_data = self._generate_projects_data()
        logger.info("Demo MCP Server инициализирован")
    
    def _generate_users_data(self) -> List[Dict]:
        """Генерация тестовых данных пользователей"""
        names = [
            "Иван Петров", "Мария Сидорова", "Алексей Козлов", "Елена Волкова",
            "Дмитрий Смирнов", "Ольга Морозова", "Сергей Васильев", "Анна Федорова"
        ]
        departments = ["Разработка", "Дизайн", "QA", "Аналитика", "DevOps"]
        positions = ["Junior", "Middle", "Senior", "Lead", "Manager"]
        
        users = []
        for i, name in enumerate(names):
            users.append({
                "id": f"USER-{i+1:03d}",
                "name": name,
                "email": f"{name.split()[0].lower()}@company.com",
                "department": random.choice(departments),
                "position": random.choice(positions),
                "salary": random.randint(60, 200) * 1000,
                "active": random.choice([True, True, True, False]),  # больше активных
                "joinDate": (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d"),
                "tasksCompleted": random.randint(10, 150),
                "efficiency": random.randint(75, 98)
            })
        
        return users
    
    def _generate_tasks_data(self) -> List[Dict]:
        """Генерация тестовых данных задач"""
        task_titles = [
            "Реализовать аутентификацию",
            "Создать дизайн главной страницы", 
            "Настроить CI/CD pipeline",
            "Добавить мобильную версию",
            "Оптимизировать базу данных",
            "Написать документацию API",
            "Исправить баги в корзине",
            "Интегрировать платежную систему"
        ]
        
        statuses = ["Новая", "В работе", "На ревью", "Тестирование", "Завершена"]
        priorities = ["Низкий", "Средний", "Высокий", "Критический"]
        
        tasks = []
        for i, title in enumerate(task_titles):
            status = random.choice(statuses)
            progress = 0 if status == "Новая" else random.randint(10, 100) if status != "Завершена" else 100
            
            tasks.append({
                "id": f"TASK-{i+1:03d}",
                "title": title,
                "status": status,
                "priority": random.choice(priorities),
                "assignee": random.choice(self.users_data)["name"],
                "progress": progress,
                "estimatedHours": random.randint(8, 80),
                "loggedHours": int(progress / 100 * random.randint(8, 80)),
                "dueDate": (datetime.now() + timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d"),
                "created": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            })
        
        return tasks
    
    def _generate_projects_data(self) -> List[Dict]:
        """Генерация тестовых данных проектов"""
        return [
            {
                "id": "PROJ-001",
                "name": "Система управления задачами",
                "description": "Новая платформа для управления проектами и задачами",
                "status": "В разработке",
                "progress": 67,
                "budget": 2500000,
                "spent": 1675000,
                "teamSize": 8,
                "startDate": "2024-01-01",
                "endDate": "2024-06-30",
                "manager": "Анна Николаева"
            },
            {
                "id": "PROJ-002", 
                "name": "Мобильное приложение",
                "description": "iOS и Android приложение для клиентов",
                "status": "Планирование",
                "progress": 15,
                "budget": 1800000,
                "spent": 270000,
                "teamSize": 5,
                "startDate": "2024-03-01",
                "endDate": "2024-09-30",
                "manager": "Игорь Соколов"
            }
        ]
    
    def get_tools_list(self) -> List[Dict]:
        """Список доступных инструментов"""
        return [
            {
                "name": "show_users_table",
                "description": "Показать таблицу всех пользователей системы",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "show_user_profile",
                "description": "Показать профиль конкретного пользователя",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "userId": {
                            "type": "string",
                            "description": "ID пользователя (например: USER-001)"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "show_tasks_board",
                "description": "Показать доску задач с их статусами",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "show_project_dashboard",
                "description": "Показать дашборд с метриками проектов",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "show_team_statistics",
                "description": "Показать статистику работы команды",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "create_user_form",
                "description": "Создать форму для добавления нового пользователя",
                "inputSchema": {
                    "type": "object", 
                    "properties": {},
                    "required": []
                }
            }
        ]
    
    def call_tool(self, tool_name: str, arguments: Dict = None) -> Dict:
        """Вызов конкретного инструмента"""
        if arguments is None:
            arguments = {}
            
        try:
            if tool_name == "show_users_table":
                return self._show_users_table()
            elif tool_name == "show_user_profile":
                return self._show_user_profile(arguments.get("userId", ""))
            elif tool_name == "show_tasks_board":
                return self._show_tasks_board()
            elif tool_name == "show_project_dashboard":
                return self._show_project_dashboard()
            elif tool_name == "show_team_statistics":
                return self._show_team_statistics()
            elif tool_name == "create_user_form":
                return self._create_user_form()
            else:
                return {
                    "isError": True,
                    "content": [{"type": "text", "text": f"Неизвестный инструмент: {tool_name}"}]
                }
                
        except Exception as e:
            logger.error(f"Ошибка выполнения инструмента {tool_name}: {e}")
            return {
                "isError": True,
                "content": [{"type": "text", "text": f"Ошибка выполнения: {str(e)}"}]
            }
    
    def _show_users_table(self) -> Dict:
        """Показать таблицу пользователей"""
        # Упрощаем данные для таблицы
        table_data = []
        for user in self.users_data:
            table_data.append({
                "ID": user["id"],
                "Имя": user["name"],
                "Email": user["email"], 
                "Отдел": user["department"],
                "Должность": user["position"],
                "Зарплата": f"{user['salary']:,} ₽",
                "Статус": "Активен" if user["active"] else "Неактивен",
                "Задач": user["tasksCompleted"],
                "Эффективность": f"{user['efficiency']}%"
            })
        
        html = self.ui.generate_table(
            table_data,
            title="Сотрудники компании",
            description="Полный список всех сотрудников с основной информацией"
        )
        
        return {
            "content": [
                {
                    "type": "resource",
                    "resource": {
                        "uri": "ui://users-table",
                        "mimeType": "text/html",
                        "text": html
                    }
                }
            ]
        }
    
    def _show_user_profile(self, user_id: str) -> Dict:
        """Показать профиль пользователя"""
        # Найти пользователя по ID
        user = next((u for u in self.users_data if u["id"] == user_id), None)
        
        if not user:
            # Если ID не найден, показываем первого пользователя
            user = self.users_data[0]
        
        # Подготовить данные для карточки
        profile_data = {
            "ID": user["id"],
            "Полное имя": user["name"],
            "Email": user["email"],
            "Отдел": user["department"],
            "Должность": user["position"],
            "Зарплата": f"{user['salary']:,} ₽",
            "Дата найма": user["joinDate"],
            "Статус": "Активен" if user["active"] else "Неактивен",
            "Выполнено задач": user["tasksCompleted"],
            "Эффективность": f"{user['efficiency']}%"
        }
        
        html = self.ui.generate_card(
            profile_data,
            title=f"Профиль: {user['name']}",
            description="Подробная информация о сотруднике"
        )
        
        return {
            "content": [
                {
                    "type": "resource",
                    "resource": {
                        "uri": f"ui://user-profile-{user['id']}",
                        "mimeType": "text/html",
                        "text": html
                    }
                }
            ]
        }
    
    def _show_tasks_board(self) -> Dict:
        """Показать доску задач"""
        # Подготовить данные для таблицы
        table_data = []
        for task in self.tasks_data:
            table_data.append({
                "ID": task["id"],
                "Название": task["title"],
                "Статус": task["status"],
                "Приоритет": task["priority"],
                "Исполнитель": task["assignee"],
                "Прогресс": f"{task['progress']}%",
                "Часов": f"{task['loggedHours']}/{task['estimatedHours']}",
                "Срок": task["dueDate"]
            })
        
        html = self.ui.generate_table(
            table_data,
            title="Доска задач",
            description="Текущие задачи и их статусы"
        )
        
        return {
            "content": [
                {
                    "type": "resource",
                    "resource": {
                        "uri": "ui://tasks-board",
                        "mimeType": "text/html",
                        "text": html
                    }
                }
            ]
        }
    
    def _show_project_dashboard(self) -> Dict:
        """Показать дашборд проектов"""
        # Подсчет метрик
        total_tasks = len(self.tasks_data)
        completed_tasks = len([t for t in self.tasks_data if t["status"] == "Завершена"])
        in_progress_tasks = len([t for t in self.tasks_data if t["status"] == "В работе"])
        active_users = len([u for u in self.users_data if u["active"]])
        
        # Метрики для дашборда
        metrics = [
            {
                "title": "Всего задач",
                "value": total_tasks,
                "change": 12,
                "changeType": "increase"
            },
            {
                "title": "Завершено",
                "value": completed_tasks,
                "change": 8,
                "changeType": "increase"
            },
            {
                "title": "В работе", 
                "value": in_progress_tasks,
                "change": -3,
                "changeType": "decrease"
            },
            {
                "title": "Активных сотрудников",
                "value": active_users,
                "change": 0,
                "changeType": "neutral"
            }
        ]
        
        html = self.ui.generate_dashboard(
            metrics,
            title="Дашборд проектов"
        )
        
        return {
            "content": [
                {
                    "type": "resource",
                    "resource": {
                        "uri": "ui://project-dashboard",
                        "mimeType": "text/html",
                        "text": html
                    }
                }
            ]
        }
    
    def _show_team_statistics(self) -> Dict:
        """Показать статистику команды"""
        # Статистика по отделам
        departments = {}
        for user in self.users_data:
            dept = user["department"]
            if dept not in departments:
                departments[dept] = {"count": 0, "efficiency": 0, "tasks": 0}
            departments[dept]["count"] += 1
            departments[dept]["efficiency"] += user["efficiency"]
            departments[dept]["tasks"] += user["tasksCompleted"]
        
        # Средние значения
        for dept in departments:
            count = departments[dept]["count"]
            departments[dept]["efficiency"] = round(departments[dept]["efficiency"] / count)
            departments[dept]["avgTasks"] = round(departments[dept]["tasks"] / count)
        
        # Подготовка данных для таблицы
        table_data = []
        for dept, stats in departments.items():
            table_data.append({
                "Отдел": dept,
                "Сотрудников": stats["count"],
                "Средняя эффективность": f"{stats['efficiency']}%",
                "Среднее кол-во задач": stats["avgTasks"],
                "Всего задач": stats["tasks"]
            })
        
        html = self.ui.generate_table(
            table_data,
            title="Статистика по отделам",
            description="Анализ производительности команды по отделам"
        )
        
        return {
            "content": [
                {
                    "type": "resource",
                    "resource": {
                        "uri": "ui://team-statistics",
                        "mimeType": "text/html",
                        "text": html
                    }
                }
            ]
        }
    
    def _create_user_form(self) -> Dict:
        """Создать форму для добавления пользователя"""
        form_html = """
        <style>
            .ui-component {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 16px 0;
            }
            .ui-form {
                max-width: 500px;
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 24px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .ui-form-title {
                margin: 0 0 20px 0;
                color: #333;
                font-size: 18px;
                font-weight: 600;
            }
            .ui-form-field {
                margin-bottom: 16px;
            }
            .ui-form-field label {
                display: block;
                margin-bottom: 6px;
                font-weight: 500;
                color: #555;
            }
            .ui-form-field input,
            .ui-form-field select {
                width: 100%;
                padding: 10px 12px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                box-sizing: border-box;
                transition: border-color 0.2s;
            }
            .ui-form-field input:focus,
            .ui-form-field select:focus {
                outline: none;
                border-color: #007bff;
                box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
            }
            .ui-form-submit {
                background: #007bff;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                cursor: pointer;
                font-weight: 500;
                transition: background-color 0.2s;
            }
            .ui-form-submit:hover {
                background: #0056b3;
            }
            .required {
                color: #dc3545;
            }
        </style>
        <div class="ui-component">
            <div class="ui-form">
                <h3 class="ui-form-title">Добавить нового сотрудника</h3>
                <form>
                    <div class="ui-form-field">
                        <label for="name">Полное имя <span class="required">*</span></label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    
                    <div class="ui-form-field">
                        <label for="email">Email <span class="required">*</span></label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    
                    <div class="ui-form-field">
                        <label for="department">Отдел</label>
                        <select id="department" name="department">
                            <option value="">Выберите отдел</option>
                            <option value="Разработка">Разработка</option>
                            <option value="Дизайн">Дизайн</option>
                            <option value="QA">QA</option>
                            <option value="Аналитика">Аналитика</option>
                            <option value="DevOps">DevOps</option>
                        </select>
                    </div>
                    
                    <div class="ui-form-field">
                        <label for="position">Должность</label>
                        <select id="position" name="position">
                            <option value="">Выберите должность</option>
                            <option value="Junior">Junior</option>
                            <option value="Middle">Middle</option>
                            <option value="Senior">Senior</option>
                            <option value="Lead">Lead</option>
                            <option value="Manager">Manager</option>
                        </select>
                    </div>
                    
                    <div class="ui-form-field">
                        <label for="salary">Зарплата (₽)</label>
                        <input type="number" id="salary" name="salary" min="0" step="1000">
                    </div>
                    
                    <button type="submit" class="ui-form-submit">
                        Добавить сотрудника
                    </button>
                </form>
            </div>
        </div>
        """
        
        return {
            "content": [
                {
                    "type": "resource",
                    "resource": {
                        "uri": "ui://user-form",
                        "mimeType": "text/html",
                        "text": form_html
                    }
                }
            ]
        }

# HTTP сервер для SSE
class MCPSSEHandler(http.server.SimpleHTTPRequestHandler):
    server_instance = None
    
    def do_GET(self):
        if self.path == '/sse':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            try:
                # Отправляем информацию о доступных инструментах
                tools_data = {
                    "jsonrpc": "2.0",
                    "result": {
                        "tools": {}
                    }
                }
                
                if MCPSSEHandler.server_instance:
                    tools_list = MCPSSEHandler.server_instance.get_tools_list()
                    for tool in tools_list:
                        tools_data["result"]["tools"][tool["name"]] = {
                            "description": tool["description"],
                            "inputSchema": tool["inputSchema"]
                        }
                
                self.wfile.write(f'data: {json.dumps(tools_data, ensure_ascii=False)}\n\n'.encode('utf-8'))
                self.wfile.flush()
                
                # Отправляем heartbeat
                time.sleep(0.5)
                heartbeat = {"type": "heartbeat", "timestamp": time.time()}
                self.wfile.write(f'data: {json.dumps(heartbeat)}\n\n'.encode('utf-8'))
                self.wfile.flush()
                
            except Exception as e:
                logger.error(f"Ошибка SSE: {e}")
                
        elif self.path.startswith('/tool/'):
            self.handle_tool_call()
            
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'message': 'Demo MCP Server with UI Generator running', 
                'status': 'ok',
                'sse_endpoint': 'http://localhost:8813/sse',
                'available_tools': len(MCPSSEHandler.server_instance.get_tools_list()) if MCPSSEHandler.server_instance else 0
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path.startswith('/tool/'):
            self.handle_tool_call()
        else:
            self.send_error(404)
    
    def handle_tool_call(self):
        """Обработка вызова инструмента"""
        try:
            # Извлекаем имя инструмента из пути
            tool_name = self.path.split('/tool/')[-1].split('?')[0]
            
            # Парсим параметры из query string
            query_params = {}
            if '?' in self.path:
                query_string = self.path.split('?')[1]
                query_params = dict(urllib.parse.parse_qsl(query_string))
            
            # Читаем тело запроса для POST
            if self.command == 'POST':
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    post_data = self.rfile.read(content_length)
                    try:
                        post_params = json.loads(post_data.decode('utf-8'))
                        query_params.update(post_params)
                    except:
                        pass
            
            logger.info(f"Вызов инструмента: {tool_name} с параметрами: {query_params}")
            
            if MCPSSEHandler.server_instance:
                result = MCPSSEHandler.server_instance.call_tool(tool_name, query_params)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            else:
                self.send_error(500)
                
        except Exception as e:
            logger.error(f"Ошибка обработки вызова инструмента: {e}")
            self.send_error(500)
    
    def log_message(self, format, *args):
        logger.info(f"HTTP: {format % args}")

def run_sse_server():
    """Запуск HTTP сервера для SSE"""
    # Создаем экземпляр MCP сервера
    MCPSSEHandler.server_instance = DemoMCPServer()
    
    with socketserver.TCPServer(('', 8813), MCPSSEHandler) as httpd:
        logger.info('🚀 Demo MCP SSE server running on http://localhost:8813')
        logger.info('📡 SSE endpoint: http://localhost:8813/sse')
        logger.info('🎨 UI Generator demo tools available!')
        logger.info('🔧 Add this URL as SSE MCP server in the interface')
        httpd.serve_forever()

if __name__ == "__main__":
    run_sse_server()