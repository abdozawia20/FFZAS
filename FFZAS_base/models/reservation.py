from odoo import fields, models

class Reservation(models.Model):
    _name = "reservation"

    customer = fields.Many2one(comodel_name='res.user', string="Customer", domain=[("type", 'in', "c")])
    time_from = fields.Datetime(string="Time From")
    time_to = fields.Datetime(string="Time To")
    field = fields.Many2one(comodel_name='field', string="Field")
    state = fields.Selection(selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('completed' ,'Completed')])
    price = fields.Float(string="Price")

