from rest_framework.views import (
    status,
    APIView,
    Response,
    Http404,
)

from main import models, serializers


class ReportView(APIView):

    def get_object(self, pk):
        try:
            return models.Report.objects.get(pk=pk)
        except models.Report.DoesNotExist:
            raise Http404

    def get_by_query(self, project_id, method, query):
        return models.Report.objects.filter(project_id=project_id,
                                            method=method,
                                            query=query).first()

    def get(self, request, report_id):
        report = self.get_object(report_id)
        serializer = serializers.ReportSerializer(report)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.instance = self.get_by_query(
                project_id=serializer.validated_data.get("project_id"),
                method=serializer.validated_data.get("method"),
                query=serializer.validated_data.get("query"))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, report_id):
        report = self.get_object(report_id)
        serializer = serializers.ReportSerializer(instance=report,
                                                  data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, report_id):
        print(f"pretend to delete report where report_id={report_id}")


class ReportListView(APIView):

    def get(self, request, report_id):
        reports = models.Report.objects.filter(report_id=report_id)
        serializer = serializers.ReportSerializer(reports, many=True)
        return Response(serializer.data)
