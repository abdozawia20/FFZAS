from odoo import fields, models

class Field(models.Model):
    _name = "field"

    capacity = fields.Integer(string="Capacity")
    location = fields.Text(string="Location")
    field_number = fields.Integer(string="Field Number")
