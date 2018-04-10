from django.db.models import Count, Sum

from rest_framework.decorators import list_route
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .filters import GVAIncidentFilter
from .gva.stats import Calculator, Mode
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

    def get(self, request, format=None):
        filters = dict(date__year=request.query_params.get("year"))
        calculator = Calculator()
        calculator.mode = Mode.COUNTRY

        state = request.query_params.get("state", None)
        if state is not None:
            filters["state"] = state
            calculator.mode = Mode.STATE

        incidents = GVAIncident.objects.filter(**filters)
        return Response(calculator.run(incidents))
