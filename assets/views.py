"""
This module maps the routes of API paths to respective views.

Author: Shashank Shekhar
"""

from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView

from .models import Asset
from .serializer import *
# from drf_yasg.utils import swagger_auto_schema


class AssetsView(APIView):
    """
    Defines different asset views.

    Methods:
        get(request): Defines the GET method to get all available assets.
        post(request): Defines the POST method to create a new asset.
    """

    @staticmethod
    def get(request):
        """
        Get list of assets

        Fetches list of all available assets
        """
        data = Asset.objects.all()

        serializer = AssetSerializer(
            data, context={
                'request': request}, many=True)

        return Response(serializer.data)

    @staticmethod
    def post(request):
        """
        Add an asset

        Adds an asset to list of available assets
        """
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST'])
# def asset_list(request):
#     if request.method == 'GET':
#         data = Asset.objects.all()

#         serializer = AssetSerializer(data, context={'request': request}, many=True)

#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = AssetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)

# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT', 'DELETE'])
# def asset_detail(request, pk):
#     try:
#         student = Asset.objects.get(pk=pk)
#     except Asset.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = AssetSerializer(student, data=request.data,context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         Asset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
