from oscar.apps.shipping import repository

from shipping import methods


class Repository(repository.Repository):
    methods = (methods.FreeRoyalMailFirstClass(),)
