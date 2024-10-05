import json

from django.db import connection
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

    def get(self, request):
        sql = "select  \
r1.query as query, \
r1.doc_ids as doc_ids_mv, \
r2.doc_ids as doc_ids_es, \
r3.doc_ids as doc_ids_qd, \
r1.doc_names as doc_names_mv, \
r2.doc_names as doc_names_es, \
r3.doc_names as doc_names_qd, \
r1.paragraph_ids as paragraph_ids_mv, \
r2.paragraph_ids as paragraph_ids_es, \
r3.paragraph_ids as paragraph_ids_qd, \
r1.paragraph_contents as paragraph_contents_mv, \
r2.paragraph_contents as paragraph_contents_es, \
r3.paragraph_contents as paragraph_contents_qd \
from report as r1 \
left join report as r2 on r1.query = r2.query \
left join report as r3 on r1.query = r3.query \
where r1.method='milvus' and r2.method='ES+Milvus' and r3.method='qdrant';"
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
        
        for item in result:
            paragraph_ids_mv = json.loads(item["paragraph_ids_mv"])
            paragraph_ids_es = json.loads(item["paragraph_ids_es"])
            paragraph_ids_qd = json.loads(item["paragraph_ids_qd"])
            item["paragraph_contents_mv"] = json.loads(item["paragraph_contents_mv"])
            item["paragraph_contents_es"] = json.loads(item["paragraph_contents_es"])
            item["paragraph_contents_qd"] = json.loads(item["paragraph_contents_qd"])

            item["doc_names_mv"] = json.loads(item["doc_names_mv"])
            item["doc_names_es"] = json.loads(item["doc_names_es"])
            item["doc_names_qd"] = json.loads(item["doc_names_qd"])

            for i, content in enumerate(item["paragraph_contents_mv"]):
                item["paragraph_contents_mv"][i] = f"{str(paragraph_ids_mv[i]).ljust(4)} {content}"
            for i, content in enumerate(item["paragraph_contents_es"]):
                item["paragraph_contents_es"][i] = f"{str(paragraph_ids_es[i]).ljust(4)} {content}"
            for i, content in enumerate(item["paragraph_contents_qd"]):
                item["paragraph_contents_qd"][i] = f"{str(paragraph_ids_qd[i]).ljust(4)} {content}"

        return Response(result)
