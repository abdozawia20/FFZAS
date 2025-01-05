from email.policy import default

from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = "res.users"

    telephone = fields.Text(string="Telephone Number")
    surname = fields.Text(string="Last Name")
    type = fields.Selection(selection=[('c', "Customer"),
                                       ('e', "Employee"),
                                       ('s', "Super User")]
                            , default='c'
                            , string="User Type")

    @api.model
    def create(self, values):
        # Create the record
        record = super(ResUsers, self).create(values)

        #Display Success message along with the username
        if record.name:
            message = f"User '{record.name}' has been successfully created."
            self.env.user.notify_info(message)

        return record

    def write(self, values):
        # Update the record
        result = super(ResUsers, self).write(values)

        #Display Success message along with the username
        for record in self:
            if record.name:
                message = f"User '{record.name}' has been successfully updated."
                self.env.user.notify_info(message)

        return result

    def unlink(self):
        for rec in self:
            reservations = rec.env['reservation'].search(['customer', '=', rec.id])
            reservations.customer = rec.env['res.config.settings'].deleted_user_template

        return super(ResUsers, self).unlink()