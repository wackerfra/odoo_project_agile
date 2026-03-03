# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sprint_id = fields.Many2one(
        'project.sprint',
        string='Sprint',
        index=True,
        domain="[('project_id', '=', project_id)]",
        group_expand='_read_group_sprint_ids',
        help='Sprint to which this task belongs.')
    sprint_state = fields.Selection(
        related='sprint_id.state',
        string='Sprint State',
        selection=[('planned', 'Planned'), ('active', 'Active'), ('closed', 'Closed')],
        index=True,
        readonly=True
    )

    def _read_group_sprint_ids(self, sprints, domain, *args, **kwargs):
        # Only show sprints of the current project if we are in one, 
        # otherwise show all active/planned sprints.
        project_id = self.env.context.get('default_project_id')
        search_domain = [('state', 'in', ('planned', 'active'))]
        if project_id:
            search_domain.append(('project_id', '=', project_id))
        return sprints.search(search_domain)

    # Lead time: from creation to first close (approx: last stage update if closed)
    lead_time_days = fields.Float(string='Lead Time (days)', compute='_compute_lead_cycle_time', store=False)
    # Cycle time: from assign/start to close (approx)
    cycle_time_days = fields.Float(string='Cycle Time (days)', compute='_compute_lead_cycle_time', store=False)

    @api.depends('create_date', 'date_assign', 'date_last_stage_update', 'state')
    def _compute_lead_cycle_time(self):
        for task in self:
            lead = 0.0
            cycle = 0.0
            if task.state in ('1_done', '1_canceled') and task.date_last_stage_update:
                if task.create_date:
                    delta = fields.Datetime.to_datetime(task.date_last_stage_update) - fields.Datetime.to_datetime(task.create_date)
                    lead = max(delta.days + (delta.seconds / 86400.0), 0.0)
                if task.date_assign:
                    delta2 = fields.Datetime.to_datetime(task.date_last_stage_update) - fields.Datetime.to_datetime(task.date_assign)
                    cycle = max(delta2.days + (delta2.seconds / 86400.0), 0.0)
            task.lead_time_days = lead
            task.cycle_time_days = cycle

    @api.onchange('project_id')
    def _onchange_project_clear_sprint(self):
        if self.sprint_id and self.project_id and self.sprint_id.project_id != self.project_id:
            self.sprint_id = False
