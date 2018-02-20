import datetime

import factory
from factory import Faker, fuzzy


class GVAIncidentFactory(factory.DjangoModelFactory):

    city_county = Faker("pystr", max_chars=128)
    date = fuzzy.FuzzyDate(datetime.date.today() - datetime.timedelta(days=7))
    gva_id = fuzzy.FuzzyInteger(1000)
    injured = fuzzy.FuzzyInteger(10)
    killed = fuzzy.FuzzyInteger(10)
    state = factory.SubFactory("geo.factories.UsStateFactory")
    street = Faker("pystr", max_chars=128)

    class Meta:
        model = "crime.GVAIncident"

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
