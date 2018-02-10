import factory


class TagFactory(factory.DjangoModelFactory):

    name = factory.Sequence(lambda n: "name-{0}".format(n))

    class Meta:
        model = "taxonomy.Tag"
