from rest_framework.views import (
    status,
    APIView,
    Response,
    Http404,
)

from main import models, serializers


class ProjectView(APIView):

    def get_object(self, pk):
        try:
            return models.Project.objects.get(pk=pk)
        except models.Project.DoesNotExist:
            raise Http404

    def get(self, request, project_id):
        project = self.get_object(project_id)
        serializer = serializers.ProjectSerializer(project)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, project_id):
        project = self.get_object(project_id)
        serializer = serializers.ProjectSerializer(instance=project,
                                                   data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        print(f"pretend to delete project where project_id={project_id}")


class ProjectListView(APIView):

    def get(self, request):
        projects = models.Project.objects.all()
        serializer = serializers.ProjectSerializer(projects, many=True)
        return Response(serializer.data)
