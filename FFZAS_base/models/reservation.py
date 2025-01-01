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
    def create(self, values):
        # Checking if field is available before creating the reservation
        field = self.env['field'].browse(values.get('field'))
        if self.is_field_available(values.get('time_from'), values.get('time_to'), field):
            raise UserError("The selected field is already booked during the specified time range.")

        return super(Reservation, self).create(values) # Proceed with creating the reservation

    def write(self, values):
        # Checking if field is available before updating the reservation
        field = self.env['field'].browse(values.get('field')) if values.get('field') else self.field
        if self.is_field_available(values.get('time_from', self.time_from), values.get('time_to', self.time_to), field): # checking the new time range
            raise UserError(
                f"Unable to update the reservation from {self.time_from} to {self.time_to} because it conflicts with another reservation.")

        return super(Reservation, self).write(values) # Proceed with updating the reservation
    # (^_^)

