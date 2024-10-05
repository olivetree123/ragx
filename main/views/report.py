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
r1.paragraph_ids as paragraph_ids_mv, \
r4.paragraph_ids as paragraph_ids_mv2, \
r2.paragraph_ids as paragraph_ids_es, \
r3.paragraph_ids as paragraph_ids_qd, \
r1.paragraph_titles as paragraph_titles_mv, \
r4.paragraph_titles as paragraph_titles_mv2, \
r2.paragraph_titles as paragraph_titles_es, \
r3.paragraph_titles as paragraph_titles_qd \
from report as r1 \
left join report as r2 on r1.query = r2.query \
left join report as r3 on r1.query = r3.query \
left join report as r4 on r1.query = r4.query \
where r1.method='milvus' and r2.method='ES+Milvus' and r3.method='qdrant' and r4.method='Milvus+Rerank';"

# r1.doc_ids as doc_ids_mv, \
# r4.doc_ids as doc_ids_mv2, \
# r2.doc_ids as doc_ids_es, \
# r3.doc_ids as doc_ids_qd, \
# r1.doc_names as doc_names_mv, \
# r4.doc_names as doc_names_mv2, \
# r2.doc_names as doc_names_es, \
# r3.doc_names as doc_names_qd, \

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
        
        for item in result:
            paragraph_ids_mv = json.loads(item["paragraph_ids_mv"])
            paragraph_ids_mv2 = json.loads(item["paragraph_ids_mv2"])
            paragraph_ids_es = json.loads(item["paragraph_ids_es"])
            paragraph_ids_qd = json.loads(item["paragraph_ids_qd"])

            # doc_ids_mv = json.loads(item["doc_ids_mv"])
            # doc_ids_mv2 = json.loads(item["doc_ids_mv2"])
            # doc_ids_es = json.loads(item["doc_ids_es"])
            # doc_ids_qd = json.loads(item["doc_ids_qd"])

            item["paragraph_titles_mv"] = json.loads(item["paragraph_titles_mv"])
            item["paragraph_titles_mv2"] = json.loads(item["paragraph_titles_mv2"])
            item["paragraph_titles_es"] = json.loads(item["paragraph_titles_es"])
            item["paragraph_titles_qd"] = json.loads(item["paragraph_titles_qd"])

            # item["paragraph_contents_mv"] = json.loads(item["paragraph_contents_mv"])
            # item["paragraph_contents_es"] = json.loads(item["paragraph_contents_es"])
            # item["paragraph_contents_qd"] = json.loads(item["paragraph_contents_qd"])

            # item["doc_names_mv"] = json.loads(item["doc_names_mv"])
            # item["doc_names_mv2"] = json.loads(item["doc_names_mv2"])
            # item["doc_names_es"] = json.loads(item["doc_names_es"])
            # item["doc_names_qd"] = json.loads(item["doc_names_qd"])

            for i, title in enumerate(item["paragraph_titles_mv"]):
                item["paragraph_titles_mv"][i] = f"{str(paragraph_ids_mv[i]).ljust(4)} {title}"
            for i, title in enumerate(item["paragraph_titles_mv2"]):
                item["paragraph_titles_mv2"][i] = f"{str(paragraph_ids_mv2[i]).ljust(4)} {title}"
            for i, title in enumerate(item["paragraph_titles_es"]):
                item["paragraph_titles_es"][i] = f"{str(paragraph_ids_es[i]).ljust(4)} {title}"
            for i, title in enumerate(item["paragraph_titles_qd"]):
                item["paragraph_titles_qd"][i] = f"{str(paragraph_ids_qd[i]).ljust(4)} {title}"

            # for i, content in enumerate(item["paragraph_contents_mv"]):
            #     item["paragraph_contents_mv"][i] = f"{str(paragraph_ids_mv[i]).ljust(4)} {content}"
            # for i, content in enumerate(item["paragraph_contents_es"]):
            #     item["paragraph_contents_es"][i] = f"{str(paragraph_ids_es[i]).ljust(4)} {content}"
            # for i, content in enumerate(item["paragraph_contents_qd"]):
            #     item["paragraph_contents_qd"][i] = f"{str(paragraph_ids_qd[i]).ljust(4)} {content}"

            # for i, name in enumerate(item["doc_names_mv"]):
            #     item["doc_names_mv"][i] = f"{str(doc_ids_mv[i]).ljust(3)} {name}"
            # for i, name in enumerate(item["doc_names_mv2"]):
            #     item["doc_names_mv2"][i] = f"{str(doc_ids_mv2[i]).ljust(3)} {name}"
            # for i, name in enumerate(item["doc_names_es"]):
            #     item["doc_names_es"][i] = f"{str(doc_ids_es[i]).ljust(3)} {name}"
            # for i, name in enumerate(item["doc_names_qd"]):
            #     item["doc_names_qd"][i] = f"{str(doc_ids_qd[i]).ljust(3)} {name}"

        return Response(result)
