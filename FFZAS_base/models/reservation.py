from odoo import fields, models, api
from odoo.exceptions import UserError


class Reservation(models.Model):
    _name = "reservation"

    customer = fields.Many2one(comodel_name='res.user', string="Customer", domain=[("type", 'in', "c")])
    time_from = fields.Datetime(string="Time From")
    time_to = fields.Datetime(string="Time To")
    field = fields.Many2one(comodel_name='field', string="Field")
    state = fields.Selection(selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('completed' ,'Completed')])
    price = fields.Float(string="Price")

    def is_field_available(self, time_from, time_to, field):
        field_id = field.id

        reservations = self.search([
            ('field', '=', field_id),
            ('time_from', '<', 'time_to'), # check if the time overlaps: the start time comes before the new end time
            ('time_to', '>', 'time_from'), # check if the time overlaps: the end time comes after the new start time
            ('state', '!=', 'completed') # to avoid checking any completed reservations
        ])
        if reservations:
            return True
        return False
    # (^_^)

    @api.model
    def unlink(self):

        for rec in self:
            if rec.state == 'confirmed':
                raise UserError(f"The reservation id: {rec.id} cannot be deleted because it's confirmed.")

        return super(Reservation, self).unlink()