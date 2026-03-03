# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from datetime import date


@tagged('post_install', '-at_install')
class TestProjectSprint(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Project = self.env['project.project']
        self.Task = self.env['project.task']
        self.Sprint = self.env['project.sprint']
        self.AnalyticLine = self.env['account.analytic.line']

        self.project = self.Project.create({'name': 'Test Agile'})
        self.sprint = self.Sprint.create({
            'name': 'Sprint A',
            'project_id': self.project.id,
            'start_date': date(2026, 1, 1),
            'end_date': date(2026, 1, 14),
            'capacity_hours': 100,
        })

    def test_add_tasks_and_metrics(self):
        t1 = self.Task.create({
            'name': 'Task 1',
            'project_id': self.project.id,
            'allocated_hours': 10,
            'sprint_id': self.sprint.id,
        })
        t2 = self.Task.create({
            'name': 'Task 2',
            'project_id': self.project.id,
            'allocated_hours': 5,
            'sprint_id': self.sprint.id,
        })
        # Mark one task done
        t1.write({'state': '1_done'})

        self.sprint.invalidate_recordset(['task_ids', 'committed_hours', 'completed_hours', 'remaining_hours'])
        self.assertEqual(self.sprint.task_count, 2)
        self.assertEqual(self.sprint.done_task_count, 1)
        self.assertAlmostEqual(self.sprint.committed_hours, 15.0, places=2)
        self.assertAlmostEqual(self.sprint.completed_hours, 10.0, places=2)
        self.assertAlmostEqual(self.sprint.remaining_hours, 5.0, places=2)

        # Add timesheets
        self.AnalyticLine.create({
            'name': 'Work on Task 1',
            'task_id': t1.id,
            'project_id': self.project.id,
            'unit_amount': 3.5,
            'date': date(2026, 1, 5),
        })
        self.AnalyticLine.create({
            'name': 'Work on Task 2',
            'task_id': t2.id,
            'project_id': self.project.id,
            'unit_amount': 2.0,
            'date': date(2026, 1, 10),
        })
        self.sprint.invalidate_recordset(['consumed_hours'])
        self.assertAlmostEqual(self.sprint.consumed_hours, 5.5, places=2)

    def test_one_active_sprint_per_project(self):
        self.sprint.action_start()
        with self.assertRaises(Exception):
            self.Sprint.create({
                'name': 'Sprint B',
                'project_id': self.project.id,
                'start_date': date(2026, 1, 15),
                'end_date': date(2026, 1, 28),
                'state': 'active',
            })
