

class DatabaseRouter(object):
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen slave.
        """
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Writes always go to master.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the master/slave pool.
        """
        return True

    def allow_migrate(self, db, model):
        """
        All non-auth models end up in this pool.
        """
        return True