from math import inf
import operator

from django.db.models import Count, Sum

from .models import GVAIncident


class Calculator(object):

    def for_country(self, year):
        stats = GVAIncident.objects.filter(date__year=year).extra(
            select={"year": "CAST(EXTRACT(year FROM date) as INT)"}).values(
                "year", "state").annotate(
                    incidents=Count("id"),
                    killed=Sum("killed"),
                    injured=Sum("injured")).order_by("year", "state__postal_code")

        data = dict(incidents=0, least=dict(), most=dict())
        categories = ["injured", "killed", "victims"]
        metrics = ["least", "most"]

        for key in categories:
            data[key] = 0
            for metric in metrics:
                val = inf if metric == "least" else 0
                data[metric][key] = dict(states=[], value=val)

        for stat in stats:
            data["incidents"] += stat["incidents"]
            data["injured"] += stat["injured"]
            data["killed"] += stat["killed"]
            data["victims"] += stat["injured"] + stat["killed"]

            for category in categories:
                for metric in metrics:
                    op_func = operator.lt if metric == "least" else operator.gt

                    if category == "victims":
                        victims = stat["injured"] + stat["killed"]
                        if victims == data[metric]["victims"]["value"]:
                            data[metric]["victims"]["states"].append(stat["state"])
                        elif op_func(victims, data[metric]["victims"]["value"]):
                            data[metric]["victims"]["value"] = victims
                            data[metric]["victims"]["states"] = [stat["state"]]
                    else:
                        if stat[category] == data[metric][category]["value"]:
                            data[metric][category]["states"].append(stat["state"])
                        elif op_func(stat[category], data[metric][category]["value"]):
                            data[metric][category]["value"] = stat[category]
                            data[metric][category]["states"] = [stat["state"]]

        return data

    def for_states(self):
        data = GVAIncident.objects.extra(
            select={"year": "CAST(EXTRACT(year FROM date) as INT)"}).values(
                "year", "state").annotate(
                    incidents=Count("id"),
                    killed=Sum("killed"),
                    injured=Sum("injured")).order_by("year", "state__postal_code")
        for d in data:
            d["victims"] = d["injured"] + d["killed"]
        return data

    def for_state(self, state, year):
        data = GVAIncident.objects.filter(date__year=year, state=state).aggregate(
            incidents=Count("id"),
            injured=Sum("injured"),
            killed=Sum("killed"))
        if data["incidents"] > 0:
            data["victims"] = data["injured"] + data["killed"]
        else:
            data["incidents"] = 0
            data["injured"] = 0
            data["killed"] = 0
            data["victims"] = 0
        data["state"] = int(state)
        data["year"] = int(year)
        return data
