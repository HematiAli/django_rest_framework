from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person, Question, Answer
from .serializers import PersonSerializer, QuestionSerializer, AnswerSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from permissions import IsOwnerOrReadOnly
from django.core.paginator import Paginator

"""
from rest_framework.decorators import api_view
@api_view(['GET', 'POST', 'PUT'])
def home(request):
    return Response({'name': 'ali'})
"""


class Home(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        persons = Person.objects.all()
        page_number = self.request.query_params('page', 1)
        page_size = self.request.query_params('limit', 2)
        paginator = Paginator(persons, page_size)
        ser_data = PersonSerializer(instance=paginator.page(page_number), many=True)
        return Response(data=ser_data.data)


class QuestionListView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        srz_data = QuestionSerializer(instance=questions, many=True).data
        return Response(srz_data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        srz_data = QuestionSerializer(data=request.POST)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)
        srz_data = QuestionSerializer(instance=question, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response({'message': 'question deleted'}, status=status.HTTP_200_OK)
