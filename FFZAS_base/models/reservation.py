from odoo import fields, models, api
from odoo.exceptions import UserError

# creating reservation class
class Reservation(models.Model):
    _name = "reservation"
    # adding variables
    customer = fields.Many2one(comodel_name='res.users', string="Customer")
    time_from = fields.Datetime(string="Time From")
    time_to = fields.Datetime(string="Time To")
    field = fields.Many2one(comodel_name='field', string="Field")
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('completed' ,'Completed')],
        default="draft"
    )
    price = fields.Float(string="Price")

    # adding variables that are computed (not stored in the database)
    name = fields.Char(related='customer.name', compute="_compute_name", string="Name", readonly=True, default="")
    surname = fields.Text(related='customer.surname', compute="_compute_surname", string="Surname", readonly=True, default="")
    telephone = fields.Text(related='customer.telephone', compute="_compute_telephone", string="Telephone", readonly=True, default="")
    capacity = fields.Integer(related='field.capacity', compute="_compute_capacity", string="Capacity", readonly=True, default=None)

    # a function to check for conflicts between two reservations
    def is_field_available(self, time_from, time_to, field):
        field_id = field.id

        domain = [('state', '!=', 'completed')]
        # fields are not always provided, hence an if statement is required for the function to run properly
        if field_id:
            domain.append(('field', '=', field_id))

        domain.append(('time_from', '<=', time_to))
        domain.append(('time_to', '>=', time_from))

        # get all reservations with the information state above
        reservations = self.env['reservation'].search(domain)

        # if any reservations was found, return true, and visa versa
        if reservations:
            return True
        return False

    # overriding create function to add functionality
    @api.model
    def create(self, values):
        # Checking if field is available before creating the reservation
        field = self.env['field'].browse(values.get('field'))
        if self.is_field_available(values.get('time_from'), values.get('time_to'), field):
            raise UserError("The selected field is already booked during the specified time range.")

        reservation = super(Reservation, self).create(values)  # Proceed with creating the reservation
        reservation.customer = self.env.user.id # modify the user to be the current logged in user

        return reservation

    # overriding update/write function to add functionality
    def write(self, values):
        # Checking if field is available before updating the reservation
        field = self.env['field'].browse(values.get('field')) if values.get('field') else self.field
        if self.is_field_available(values.get('time_from', self.time_from), values.get('time_to', self.time_to),field):  # checking the new time range
            raise UserError(
                f"Unable to update the reservation from {self.time_from} to {self.time_to} because it conflicts with another reservation.")

        return super(Reservation, self).write(values)  # Proceed with updating the reservation

    # a function to handle confirming reservations
    def confirm(self):
        if self.state=='draft':
            self.state = 'confirmed' # draft reservations will change to confirmed
        else:
            self.state='completed' # confirmed reservations will change to completed
    # functions that handles the computed variables
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

    # overriding delete function to add functionality
    def unlink(self):

        for rec in self:
            if rec.state == 'confirmed': # confirmed reservations cannot be deleted
                raise UserError(f"The reservation id: {rec.id} cannot be deleted because it's confirmed.")

        return super(Reservation, self).unlink()
