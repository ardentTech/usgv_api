from enum import Enum
from math import inf


class Mode(Enum):
    COUNTRY = 0
    STATE = 1


class Calculator(object):

    def __init__(self):
        self._mode = None

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, val):
        self._mode = val

    def run(self, incidents):
        self.incidents = len(incidents)

        if self.mode == Mode.STATE:
            return self._for_state(incidents)
        elif self.mode == Mode.COUNTRY:
            return self._for_country(incidents)
        else:
            raise Exception("Unsupported calculator mode {}".format(self.mode))

    # PRIVATE
    def _for_country(self, incidents):
        results = dict(incidents=len(incidents), least=dict(), most=dict())
        categories = ["injured", "killed", "victims"]

        for key in categories:
            results[key] = 0
            results["least"][key] = dict(states=[], value=inf)
            results["most"][key] = dict(states=[], value=0)

        # todo avgs
        for i in incidents:
            results["injured"] += i.injured
            results["killed"] += i.killed

            for k in categories:
                val = getattr(i, k)
                if val == results["least"][k]["value"]:
                    results["least"][k]["states"].append(i.state.id)
                elif val < results["least"][k]["value"]:
                    results["least"][k]["value"] = val
                    results["least"][k]["states"] = [i.state.id]

                if val == results["most"][k]["value"]:
                    results["most"][k]["states"].append(i.state.id)
                elif val > results["most"][k]["value"]:
                    results["most"][k]["value"] = val
                    results["most"][k]["states"] = [i.state.id]

        results["victims"] = results["injured"] + results["killed"]
        return results

    def _for_state(self, incidents):
        results = dict(incidents=len(incidents), least=dict(), most=dict())

        for key in ["injured", "killed", "victims"]:
            results[key] = 0

        for i in incidents:
            results["injured"] += i.injured
            results["killed"] += i.killed

        results["victims"] = results["injured"] + results["killed"]
        return results

#
#            # most injured
#            if i.injured == self.most_injured["value"]:
#                self.most_injured["states"].append(i.state.id)
#            elif i.injured > self.most_injured["value"]:
#                self.most_injured["value"] = i.injured
#                self.most_injured["states"] = [i.state.id]
#
#            # least killed
#            if i.killed == stats["least_killed"]["value"]:
#                stats["least_killed"]["states"].append(i.state.id)
#            elif i.killed < stats["least_killed"]["value"]:
#                stats["least_killed"]["value"] = i.killed
#                stats["least_killed"]["states"] = [i.state.id]
#
#            # most killed
#            if i.killed == stats["most_killed"]["value"]:
#                stats["most_killed"]["states"].append(i.state.id)
#            elif i.killed > stats["most_killed"]["value"]:
#                stats["most_killed"]["value"] = i.killed
#                stats["most_killed"]["states"] = [i.state.id]
#
#            # least victims
#            if i.victims == stats["least_victims"]["value"]:
#                stats["least_victims"]["states"].append(i.state.id)
#            elif i.victims < stats["least_victims"]["value"]:
#                stats["least_victims"]["value"] = i.victims
#                stats["least_victims"]["states"] = [i.state.id]
#
#            # most victims
#            if i.victims == stats["most_victims"]["value"]:
#                stats["most_victims"]["states"].append(i.state.id)
#            elif i.victims > stats["most_victims"]["value"]:
#                stats["most_victims"]["value"] = i.victims
#                stats["most_victims"]["states"] = [i.state.id]
