class AppScaleApp:
    def __init__(self, **app_data):
        self.id = app_data.pop('id')
        self.name = app_data.pop('name', self.id)

        self.host = app_data.pop('host', None)
        self.ports = app_data.pop('ports', None)

        self.created_on = app_data.pop('creation_date', None)
        self.updated_on = app_data.pop('last_time_updated_date', None)

        self.update_id = app_data.pop('update_id', 0)
        if self.update_id is None:
            self.update_id = app_data.pop('version', 0)

        self.owner_email = app_data.pop('owner', None)

        self.extra = app_data
