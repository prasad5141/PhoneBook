from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated



# Create your views here.
from rest_framework.views import APIView
from phonebookapp.models import Contact
from phonebookapp.serializers import ContactSerializer

class ContactView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contacts = Contact.objects.filter(user=request.user)
        serializer = ContactSerializer(contacts, many=True)
        print(request.user)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={"message":"New Contact added Successfully!!!"})
        else:
            return Response(data={"error":"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


class ContactUpdateView(APIView):

    permission_classes = [IsAuthenticated]


    def put(self, request, pk):
        try:
            contact = Contact.objects.get(id=pk,user=request.user)
        except Exception as e:
            return Response(data={"error":"Object Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            contact.name = serializer.validated_data.get('name')
            contact.number = serializer.validated_data.get('number')
            contact.address = serializer.validated_data.get('address')
            contact.save()
            return Response(data={"message":"Contact Updated Successfully!!!"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"error":"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            contact = Contact.objects.get(id=pk, user=request.user)
            contact.delete()
            return Response(data={"message":"Contact Deleted Successfully!!!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error":"Object Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)
        


class SearchView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):
        q = request.GET.get('query')
        try:
            q = int(q)
            contacts = Contact.objects.filter(number__contains=q, user=request.user)
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data)
        except:
            contacts = Contact.objects.filter(name__contains=q, user=request.user)
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data)


