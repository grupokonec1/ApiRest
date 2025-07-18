class DatabaseRouter:
    db_mapping = {
        'api': 'api',
        'global': 'global',
        'avo': 'avo',
        'acsa': 'acsa',
        'cnorte': 'cnorte',
        'vsur': 'vsur',
        'condeza': 'condeza',
        'knet': 'knet',
        'storage': 'storage',
        'report': 'report',
        'pass': 'pass',
        'svia': 'svia',
        'config_ssis': 'config_ssis',
        'main': 'main',
    }

    def db_for_read(self, model, **hints):
        return self.db_mapping.get(model._meta.app_label, 'default')

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == obj2._state.db:
            return True
        return False  # No permite relaciones entre bases de datos distintas

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return self.db_mapping.get(app_label) == db
