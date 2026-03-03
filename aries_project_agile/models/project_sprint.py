# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectSprint(models.Model):
    _name = 'project.sprint'
    _description = 'Project Sprint'
    _order = 'start_date desc, id desc'

    name = fields.Char(required=True, index=True)
    project_id = fields.Many2one('project.project', string='Project', required=True, index=True, ondelete='cascade')
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    state = fields.Selection([
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], default='planned', required=True, index=True)
    capacity_hours = fields.Float(string='Capacity (Hours)', help='Team capacity for the sprint in hours.', aggregator="sum")

    task_ids = fields.One2many('project.task', 'sprint_id', string='Tasks')
    task_count = fields.Integer(compute='_compute_task_counts', string='Task Count', store=True, aggregator="sum")
    done_task_count = fields.Integer(compute='_compute_task_counts', string='Done Tasks', store=True, aggregator="sum")

    committed_hours = fields.Float(compute='_compute_commitment', string='Committed (Hours)', store=True, aggregator="sum")
    completed_hours = fields.Float(compute='_compute_commitment', string='Completed (Hours)', store=True, aggregator="sum")
    remaining_hours = fields.Float(compute='_compute_commitment', string='Remaining (Hours)', store=True, aggregator="sum")

    consumed_hours = fields.Float(compute='_compute_timesheets', string='Timesheeted (Hours)', store=True, aggregator="sum")

    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color')
    goal = fields.Char(string='Sprint Goal')

    _date_range_check = models.Constraint(
        'check(start_date <= end_date)',
        'The sprint start date must be before or equal to the end date.',
    )

    @api.constrains('state', 'project_id')
    def _check_one_active_per_project(self):
        for sprint in self:
            if sprint.state == 'active':
                other = self.search([
                    ('id', '!=', sprint.id),
                    ('project_id', '=', sprint.project_id.id),
                    ('state', '=', 'active'),
                ], limit=1)
                if other:
                    raise ValidationError(_("Only one active sprint is allowed per project."))

    @api.constrains('project_id')
    def _check_task_project_consistency(self):
        # Ensure that all tasks linked to the sprint belong to the same project
        for sprint in self:
            if not sprint.task_ids:
                continue
            wrong = sprint.task_ids.filtered(lambda t: t.project_id != sprint.project_id)
            if wrong:
                raise ValidationError(_("All tasks in a sprint must belong to the same project as the sprint."))

    @api.depends('task_ids', 'task_ids.state', 'task_ids.allocated_hours')
    def _compute_task_counts(self):
        for sprint in self:
            sprint.task_count = len(sprint.task_ids)
            done = sprint.task_ids.filtered(lambda t: t.state in ('1_done', '1_canceled'))
            sprint.done_task_count = len(done)

    @api.depends('task_ids.allocated_hours', 'task_ids.state')
    def _compute_commitment(self):
        for sprint in self:
            committed = sum(sprint.task_ids.mapped('allocated_hours'))
            completed = sum(sprint.task_ids.filtered(lambda t: t.state in ('1_done', '1_canceled')).mapped('allocated_hours'))
            sprint.committed_hours = committed
            sprint.completed_hours = completed
            sprint.remaining_hours = max(committed - completed, 0.0)

    @api.depends('task_ids', 'start_date', 'end_date')
    def _compute_timesheets(self):
        AnalyticLine = self.env['account.analytic.line']
        for sprint in self:
            total = 0.0
            if sprint.start_date and sprint.end_date and sprint.task_ids:
                total = AnalyticLine.search_read([
                    ('task_id', 'in', sprint.task_ids.ids),
                    ('date', '>=', sprint.start_date),
                    ('date', '<=', sprint.end_date),
                ], ['unit_amount'])
                total = sum(line['unit_amount'] for line in total)
            sprint.consumed_hours = total

    def action_start(self):
        for sprint in self:
            if sprint.state == 'active':
                continue
            # ensure only one active per project
            existing = self.search([
                ('project_id', '=', sprint.project_id.id),
                ('state', '=', 'active')
            ], limit=1)
            if existing:
                raise ValidationError(_("Project %s already has an active sprint: %s") % (sprint.project_id.display_name, existing.display_name))
            sprint.state = 'active'
        return True

    def action_close(self):
        self.write({'state': 'closed'})
        return True

    def action_view_tasks(self):
        self.ensure_one()
        # Prefer a stable CE action; gracefully fallback if not found
        action_ref = (self.env.ref('project.action_view_all_task', raise_if_not_found=False)
                      or self.env.ref('project.action_view_task', raise_if_not_found=False))
        if action_ref:
            action = action_ref.read()[0]
        else:
            action = {
                'type': 'ir.actions.act_window',
                'name': _('Tasks'),
                'res_model': 'project.task',
                'view_mode': 'kanban,list,form',
            }
        action['domain'] = [('sprint_id', '=', self.id)]
        # Force a fresh context dictionary to avoid string/eval issues from XML actions
        action['context'] = {
            'default_project_id': self.project_id.id,
            'search_default_group_by_stage': 1,
            'default_sprint_id': self.id,
        }
        return action

    def action_open_burndown(self):
        self.ensure_one()
        action = self.env.ref('project_agile.action_project_agile_sprint_burndown').read()[0]
        # Filter on this sprint and restrict to sprint date window
        action['domain'] = [('sprint_id', '=', self.id), ('date', '>=', fields.Date.to_date(self.start_date)), ('date', '<=', fields.Date.to_date(self.end_date))]
        # Overwrite context to ensure specific grouping and sprint filter
        action['context'] = {
            'search_default_sprint_id': self.id,
            'search_default_group_by_date': 1,
            'search_default_group_by_stage': 1,
            'search_default_filter_date': 1,
        }
        return action

    def action_open_burnup(self):
        self.ensure_one()
        action = self.env.ref('project_agile.action_project_agile_sprint_burnup').read()[0]
        action['domain'] = [('sprint_id', '=', self.id), ('date', '>=', fields.Date.to_date(self.start_date)), ('date', '<=', fields.Date.to_date(self.end_date))]
        action['context'] = {
            'search_default_sprint_id': self.id,
            'search_default_group_by_date': 1,
            'search_default_group_by_is_closed': 1,
            'search_default_filter_date': 1,
        }
        return action
