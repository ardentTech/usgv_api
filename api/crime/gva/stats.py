class Stats(object):

    def __init__(self):
        self.incidents = 0
        self.injured = 0
        self.killed = 0

    # @todo format(ter) arg?
    def calculate(self, incidents):
        self.incident = len(incidents)
        for i in incidents:
            self.injured += i.injured
            self.killed += i.killed
        return self

    @property
    def data(self):
        return dict(
            incidents=self.incidents,
            injured=self.injured,
            killed=self.killed,
            victims=self.victims)

    @property
    def victims(self):
        return self.injured + self.killed
