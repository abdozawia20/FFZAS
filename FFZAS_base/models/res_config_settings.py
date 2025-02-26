from odoo import fields, models, api

# inheriting settings class to add more functionalities
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # adding new variable to handle the deleted user template
    deleted_user_template = fields.Many2one(
        comodel_name='res.users',
        string="Deleted User Template",
        required=True,
        default=1
    )

    # a function that runs everytime the module is upgraded to insure the database is in the state it should be in
    @api.model
    def upgrade_module(self):
        # Search for a user with the name 'Deleted User'
        deleted_user = self.env['res.users'].search([('name', '=', 'Deleted User')], limit=1)

        if deleted_user:
            # If found, return without creating a new user
            return

        # Otherwise, create the 'Deleted User' record
        deleted_user = self.env['res.users'].create({
            'name': 'Deleted User',
            'login': 'deleted_user',
            'email': 'deleted@example.com',
            'active': False,  # Inactive user
        })

        # Update the settings (res.config.settings) to use the created 'Deleted User' record
        config_settings = self.env['res.config.settings'].sudo().search([], limit=1)
        if config_settings:
            config_settings.write({
                'deleted_user_template': deleted_user.id
            })
