# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models , api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class medical_patient(models.Model):

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'A ID already exists with this value !'),
        ('national_id_uniq', 'unique (national_id)', 'This National ID is already registered'),
        ('mobile_no_uniq', 'unique (mobile_no)', 'This Mobile number is already registered')
    ]

    _inherit = 'medical.patient'
    name = fields.Char(string='ID', readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('medical.patient1'))
    national_id = fields.Char(string='National ID')
    mobile_no = fields.Char(string='Mobile No')
    has_a_kids = fields.Boolean('Has a kid?')
    number_of_kids = fields.Integer('Number of kids')
    source_id =fields.Many2one(
        'source.managing',
        string='Source')
    profession = fields.Text('Profession')
    created_by = fields.Text('Created by',required=True)
    surgery_name = fields.Text('Surgery name')
    date = fields.Date(string="Date")

    @api.model
    def create(self, val):
        appointment = self._context.get('appointment_id')
        res_partner_obj = self.env['res.partner']
        if appointment:
            val_1 = {'name': self.env['res.partner'].browse(val['patient_id']).name}
            patient = res_partner_obj.create(val_1)
            val.update({'patient_id': patient.id})
        if val.get('date_of_birth'):
            dt = val.get('date_of_birth')
            d1 = datetime.strptime(str(dt), "%Y-%m-%d").date()
            d2 = datetime.today().date()
            rd = relativedelta(d2, d1)
            age = str(rd.years) + "y" + " " + str(rd.months) + "m" + " " + str(rd.days) + "d"
            val.update({'age': age})

        result = super(medical_patient, self).create(val)
        return result


class SourceManaging(models.Model):
    _name = 'source.managing'
    source = fields.Char(string='Source')
