from django.db.models import Count, Sum

from rest_framework.decorators import list_route
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .filters import GVAIncidentFilter
from .gva.stats import Stats
from .models import GVAIncident
from .serializers import GVAIncidentSerializer, GVAIncidentStatsSerializer


class GVAIncidentViewSet(ListModelMixin, GenericViewSet):

    filter_class = GVAIncidentFilter
    queryset = GVAIncident.objects.all()
    serializer_class = GVAIncidentSerializer

    @list_route(methods=["get"], url_path="yearly-stats")
    def yearly_stats(self, request):
        incidents = GVAIncident.objects.extra(
            select={"year": "CAST(EXTRACT(year FROM date) as INT)"}).values(
                "year", "state").annotate(
                    incidents=Count("id"),
                    killed=Sum("killed"),
                    injured=Sum("injured")).order_by("year", "state__postal_code")

        page = self.paginate_queryset(incidents)
        if page is not None:
            serializer = GVAIncidentStatsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = GVAIncidentStatsSerializer(incidents, many=True)
        return Response(serializer.data)

    @list_route(methods=["get"], url_path="years")
    def years(self, request):
        try:
            start_year = GVAIncident.objects.all().order_by("date")[0].date.year
            end_year = GVAIncident.objects.all().order_by("-date")[0].date.year
            years = list(range(start_year, end_year + 1)) if start_year != end_year else [end_year]
        except:
            years = []
        return Response(years)


class GVAStats(APIView):

    # @todo stats generator class
    def get(self, request, format=None):
        filters = dict(date__year=request.query_params.get("year"))
        stats = Stats()

        state = request.query_params.get("state", None)
        if state is not None:
            filters["state"] = state
            # @todo update stats mode

        incidents = GVAIncident.objects.filter(**filters)
        stats.calculate(incidents)

        return Response(stats.data)

#        filters = dict(date__year=2018)
#        incidents = GVAIncident.objects.filter(**filters)
#        stats = dict(
#            incidents=0, injured=0, killed=0, victims=0,
#            least_injured=dict(states=[], value=math.inf),
#            most_injured=dict(states=[], value=0),
#            least_killed=dict(states=[], value=math.inf),
#            most_killed=dict(states=[], value=0),
#            least_victims=dict(states=[], value=math.inf),
#            most_victims=dict(states=[], value=0),
#        )
#
#        for i in incidents:
#            stats["injured"] += i.injured
#            stats["killed"] += i.killed
#
#            # @todo only calculate if state is None
#            # least injured
#            if i.injured == stats["least_injured"]["value"]:
#                stats["least_injured"]["states"].append(i.state.id)
#            elif i.injured < stats["least_injured"]["value"]:
#                stats["least_injured"]["value"] = i.injured
#                stats["least_injured"]["states"] = [i.state.id]
#
#            # most injured
#            if i.injured == stats["most_injured"]["value"]:
#                stats["most_injured"]["states"].append(i.state.id)
#            elif i.injured > stats["most_injured"]["value"]:
#                stats["most_injured"]["value"] = i.injured
#                stats["most_injured"]["states"] = [i.state.id]
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
#
#        stats["incidents"] = len(incidents)
#        stats["victims"] = stats["injured"] + stats["killed"]
#
#        return Response(json.dumps(stats))
