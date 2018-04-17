from rest_framework.decorators import list_route
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filters import GVAIncidentFilter
from .models import GVAIncident
from .serializers import GVAIncidentSerializer
from .stats import Calculator


class GVAIncidentViewSet(ListModelMixin, GenericViewSet):

    filter_class = GVAIncidentFilter
    queryset = GVAIncident.objects.all()
    serializer_class = GVAIncidentSerializer

    @list_route(methods=["get"], url_path="stats-country")
    def stats_country(self, request):
        return Response(Calculator().for_country(year=request.query_params.get("year")))

    @list_route(methods=["get"], url_path="stats-state")
    def stats_state(self, request):
        return Response(Calculator().for_state(
            year=request.query_params.get("year"),
            state=request.query_params.get("state")))

    @list_route(methods=["get"], url_path="stats-states")
    def stats_states(self, request):
        return Response(Calculator().for_states())

    # @todo should this go on the model?
    @list_route(methods=["get"], url_path="years")
    def years(self, request):
        try:
            start_year = GVAIncident.objects.all().order_by("date")[0].date.year
            end_year = GVAIncident.objects.all().order_by("-date")[0].date.year
            years = list(range(start_year, end_year + 1)) if start_year != end_year else [end_year]
        except:
            years = []
        return Response(years)
