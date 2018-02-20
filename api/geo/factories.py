import factory
from factory import Faker


class UsStateFactory(factory.DjangoModelFactory):

    fips_code = Faker("pystr", min_chars=2, max_chars=2)
    name = Faker("pystr", max_chars=64)
    postal_code = Faker("pystr", min_chars=2, max_chars=2)

    class Meta:
        model = "geo.UsState"
