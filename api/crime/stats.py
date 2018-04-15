from math import inf
import operator

from django.db.models import Count, Sum

from .models import GVAIncident


class Calculator(object):

    def for_country(self, year=None):
        incidents = GVAIncident.objects.filter(date__year=year) if year is not None else GVAIncident.objects.all()
        results = dict(incidents=len(incidents), least=dict(), most=dict())
        # @todo make these enums
        categories = ["injured", "killed", "victims"]
        metrics = ["least", "most"]

        for key in categories:
            results[key] = 0
            for metric in metrics:
                val = inf if metric == "least" else 0
                results[metric][key] = dict(states=[], value=val)

        for i in incidents:
            results["injured"] += i.injured
            results["killed"] += i.killed

            for k in categories:
                val = getattr(i, k)
                for metric in metrics:
                    op_func = operator.lt if metric == "least" else operator.gt

                    if val == results[metric][k]["value"]:
                        results[metric][k]["states"].append(i.state.fips_code)
                    elif op_func(val, results[metric][k]["value"]):
                        results[metric][k]["value"] = val
                        results[metric][k]["states"] = [i.state.fips_code]

        for m in metrics:
            for c in categories:
                results[m][c]["states"] = set(results[m][c]["states"])

        results["victims"] = results["injured"] + results["killed"]
        return results

    # @todo victims = injured + killed
    def for_states(self):
        return GVAIncident.objects.extra(
            select={"year": "CAST(EXTRACT(year FROM date) as INT)"}).values(
                "year", "state").annotate(
                    incidents=Count("id"),
                    killed=Sum("killed"),
                    injured=Sum("injured")).order_by("year", "state__postal_code")

    def for_state(self, state, year):
        data = GVAIncident.objects.values("state").annotate(
            incidents=Count("id"),
            injured=Sum("injured"),
            killed=Sum("killed")
        ).filter(date__year=year, state=state)[0]
        data["year"] = int(year)
        return data
