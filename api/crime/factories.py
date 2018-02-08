import datetime
import pytz

import factory
from factory import Faker, fuzzy
from localflavor.us.us_states import US_STATES


class GVAIncidentFactory(factory.DjangoModelFactory):

    city_county = Faker("pystr", max_chars=128)
    date = fuzzy.FuzzyDateTime(datetime.datetime.now(tz=pytz.UTC))
    gva_id = fuzzy.FuzzyInteger(1000)
    injured = fuzzy.FuzzyInteger(10)
    killed = fuzzy.FuzzyInteger(10)
    state = fuzzy.FuzzyChoice([s[0] for s in US_STATES])
    street = Faker("pystr", max_chars=128)

    class Meta:
        model = "crime.GVAIncident"

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)


class GVAIncidentCategoryFactory(factory.DjangoModelFactory):

    name = factory.Sequence(lambda n: "name-{0}".format(n))

    class Meta:
        model = "crime.GVAIncidentCategory"
