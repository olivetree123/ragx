import json

from django.db import connection
from rest_framework.views import (
    status,
    APIView,
    Response,
    Http404,
)

from main import models, serializers


class Report2View(APIView):

    def get_object(self, pk):
        try:
            return models.Report2.objects.get(pk=pk)
        except models.Report2.DoesNotExist:
            raise Http404

    def get_by_query(self, project_id, method, query, paragraph_id):
        return models.Report2.objects.filter(
            query=query,
            method=method,
            project_id=project_id,
            paragraph_id=paragraph_id).first()

    def get(self, request, report_id):
        report = self.get_object(report_id)
        serializer = serializers.Report2Serializer(report)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.Report2Serializer(data=request.data)
        if serializer.is_valid():
            serializer.instance = self.get_by_query(
                query=serializer.validated_data.get("query"),
                method=serializer.validated_data.get("method"),
                project_id=serializer.validated_data.get("project_id"),
                paragraph_id=serializer.validated_data.get("paragraph_id"))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, report_id):
        report = self.get_object(report_id)
        serializer = serializers.Report2Serializer(instance=report,
                                                   data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, report_id):
        print(f"pretend to delete report where report_id={report_id}")


# class ResultItem(object):
#     def __init__(self, query, method, paragraph_id):
#         self.query = query  
#         self.method = method
#         self.paragraph_id = paragraph_id


# class ResultEntity(object):
#     def __init__(self, query):
#         self.query = query
#         self.intersection = []
#         self.items = []
    
#     def add_item(self, item: ResultItem):
#         current_item = None
#         for item in self.items:
#             if item.method == item.method:
#                 current_item = item
#                 break
#         if current_item is None:
#             current_item = 
        
#         current_item


class Report2ListView(APIView):

    def get(self, request):
        reports = models.Report2.objects.all()
        result = {}
        for report in reports:
            query = report.query
            if query not in result:
                result[query] = {
                    "query": report.query,
                    "intersection": [],
                    "items": [],
                    "project_id": report.project_id,
                }
            current_item = None
            items = result[query]["items"]
            for item in items:
                if item["method"] == report.method:
                    current_item = item
                    break
            if current_item is None:
                current_item = {
                    "method": report.method,
                    "paragraphs": [],
                    "positive": 0,
                    "negative": 0
                }
                items.append(current_item)
            
            current_item["paragraphs"].append({
                "id": report.paragraph_id,
                "title": report.paragraph_title,
                "status": 0,
            })
        return Response(list(result.values()))
