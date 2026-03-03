# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProjectAgileBurndownChartReport(models.AbstractModel):
    _inherit = 'project.task.burndown.chart.report'

    sprint_id = fields.Many2one('project.sprint', string='Sprint', readonly=True)
    sprint_state = fields.Selection([
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Sprint State', readonly=True)

    @property
    def task_specific_fields(self):
        # Extend the list of fields to push down to project.task
        fields_list = super().task_specific_fields
        if 'sprint_id' not in fields_list:
            fields_list.append('sprint_id')
        if 'sprint_state' not in fields_list:
            fields_list.append('sprint_state')
        return fields_list
