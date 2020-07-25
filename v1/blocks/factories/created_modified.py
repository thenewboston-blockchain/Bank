from factory import DjangoModelFactory, Faker

from thenewboston.models.created_modified import CreatedModified


class CreatedModifiedFactory(DjangoModelFactory):

    class Meta:
        model = CreatedModified
        abstract = True

    created_date = Faker('date')
    modified_date = Faker('date')
