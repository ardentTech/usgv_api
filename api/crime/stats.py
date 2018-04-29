from math import inf
import operator

from django.db.models import Count, Sum

from .models import GVAIncident
from geo.models import UsState


# @todo caching
class Calculator(object):

    # @todo accept category param
    def for_country(self, year, category=None):
        states = UsState.objects.all()
        categories = [category.lower()] if category is not None else [
            "incidents", "injured", "killed", "victims"]
        metrics = {c: 0 for c in categories}
        data = {s.id: metrics.copy() for s in states}

        stats = GVAIncident.objects.filter(date__year=year).extra(
            select={"year": "CAST(EXTRACT(year FROM date) as INT)"}).values(
                "year", "state").annotate(
                    incidents=Count("id"),
                    killed=Sum("killed"),
                    injured=Sum("injured")).order_by("year", "state__postal_code")
        for stat in stats:
            for c in categories:
                if c == "victims":
                    data[stat["state"]][c] = stat["injured"] + stat["killed"]
                else:
                    data[stat["state"]][c] = stat[c]

        payload = metrics.copy()
        payload["least"] = {c: dict(states=[], value=inf) for c in categories}
        payload["most"] = {c: dict(states=[], value=0) for c in categories}
        for state_id, v in data.items():
            for category in categories:
                datum = v[category]
                payload[category] += datum
                for qualifier, op_func in [("least", operator.lt), ("most", operator.gt)]:
                    qual_cat = payload[qualifier][category]
                    if datum == qual_cat["value"]:
                        qual_cat["states"].append(state_id)
                    elif op_func(datum, qual_cat["value"]):
                        qual_cat["value"] = datum
                        qual_cat["states"] = [state_id]

        return payload

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
