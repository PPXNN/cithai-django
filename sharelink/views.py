from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Sharelink
from .serializers import SharelinkSerializer

class SharelinkViewSet(APIView):
    def get(self, request, pk=None): # Get data or search data
        if pk:
            #Get by pk
            sharelink = Sharelink.objects.get(pk=pk)
            serializer = SharelinkSerializer(sharelink)
        else:
            sharelinks = Sharelink.objects.all() # List of object
            serializer = SharelinkSerializer(sharelinks, many=True)

        return Response(serializer.data)
    
    def post(self, request): 
        serializer = SharelinkSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        sharelink = Sharelink.objects.get(pk=pk)
        serializer = SharelinkSerializer(sharelink, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        sharelink = Sharelink.objects.get(pk=pk)
        sharelink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)