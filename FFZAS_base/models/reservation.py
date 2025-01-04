from odoo import fields, models, api
from odoo.exceptions import UserError


class Reservation(models.Model):
    _name = "reservation"

    customer = fields.Many2one(comodel_name='res.users', string="Customer", required=True)
    time_from = fields.Datetime(string="Time From")
    time_to = fields.Datetime(string="Time To")
    field = fields.Many2one(comodel_name='field', string="Field")
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('completed' ,'Completed')],
        default="draft",
        readonly=True
    )
    price = fields.Float(string="Price")

    # Temp variables:
    name = fields.Char(related='customer.name', compute="_compute_name", string="Name", readonly=True, default="")
    surname = fields.Text(related='customer.surname', compute="_compute_surname", string="Surname", readonly=True, default="")
    telephone = fields.Text(related='customer.telephone', compute="_compute_telephone", string="Telephone", readonly=True, default="")
    capacity = fields.Integer(related='field.capacity', compute="_compute_capacity", string="Capacity", readonly=True, default=None)

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

    @api.model
    def create(self, values):
        # Checking if field is available before creating the reservation
        field = self.env['field'].browse(values.get('field'))
        if self.is_field_available(values.get('time_from'), values.get('time_to'), field):
            raise UserError("The selected field is already booked during the specified time range.")

            # Create the reservation record
            new_reservation = super(Reservation, self).create(values)

            # Get the customer's username for the success message
            customer_name = new_reservation.customer.name

            #Display Success message along with the username
            message = f"Success! Reservation has been created for {customer_name}."
            new_reservation.message_post(body=message)

            return new_reservation


    def write(self, values):
        # Checking if field is available before updating the reservation
        field = self.env['field'].browse(values.get('field')) if values.get('field') else self.field
        if self.is_field_available(values.get('time_from', self.time_from), values.get('time_to', self.time_to), field): # checking the new time range
            raise UserError(
                f"Unable to update the reservation from {self.time_from} to {self.time_to} because it conflicts with another reservation.")

        # Update the reservation record
        result = super(Reservation, self).write(values)

        # Get the customer's username for the success message
        for reservation in self:
            customer_name = reservation.customer.name

            #Display Success message along with the username
            message = f"Success! Reservation for {customer_name} has been updated."
            reservation.message_post(body=message)

        return result

    @api.depends("customer")
    def _compute_name(self):
        self.name = self.customer.name

    @api.depends("customer")
    def _compute_surname(self):
        self.surname = self.customer.surname

    @api.depends("customer")
    def _compute_telephone(self):
        self.telephone = self.customer.telephone

    @api.depends("customer")
    def _compute_capacity(self):
        self.capacity = self.field.capacity

    @api.model
    def unlink(self):

        for rec in self:
            if rec.state == 'confirmed':
                raise UserError(f"The reservation id: {rec.id} cannot be deleted because it's confirmed.")

        return super(Reservation, self).unlink()
