# -*- coding: utf-8 -*-
{
    'name': 'Project Agile (Sprints & Reports)',
    'version': '19.0.1.0.0',
    'summary': 'Agile Sprint Management: Planning Boards, Burndown, Burnup, Velocity & CFD Reports',
    'description': """
Project Agile (Sprints & Reports)
================================
This add-on extends Odoo's project management with agile methodologies, 
specifically focusing on Scrum-like sprint management and agile reporting.

Key Features:
-------------
* **Sprint Management**: Create and track sprints with states (Planned, Active, Closed).
* **Sprint Planning Board**: Specialized Kanban view to drag tasks between the Backlog and sprints.
* **Active Sprint Board**: Professional Scrum board for day-to-day progress.
* **Hour-Based Metrics**: Automatic tracking of Committed, Completed, Remaining, and Consumed hours.
* **Agile Reports**:
    * Sprint Burndown & Burnup charts.
    * Sprint Velocity (Completed vs Committed).
    * Capacity vs Commitment tracking.
    * Cumulative Flow Diagram (CFD).
* **Data Integrity**: Enforced rules for sprint activation and project consistency.
    """,
    'author': 'Aries Software',
    'website': 'https://www.aries-software.net',
    'license': 'LGPL-3',
    'price': 149.0,
    'currency': 'EUR',
    'category': 'Services/Project',
    'depends': ['project', 'hr_timesheet', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_sprint_views.xml',
        'views/project_task_views.xml',
        'reports/agile_report_actions.xml',
    ],
    'demo': [
        'data/project_agile_demo.xml',
    ],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
}