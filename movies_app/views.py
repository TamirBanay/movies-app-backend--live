from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Favorite, Favorite_series
from .serializers import FavoriteSerializer, FavoriteMovieSerializer, FavoriteSeriesSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator


# Function to add CORS headers to response
def add_cors_headers(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


class AddSeriesFavoriteView(APIView):
    def post(self, request):
        serializer = FavoriteSeriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            return add_cors_headers(response)
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return add_cors_headers(response)


def post(self, request):
    serializer = FavoriteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        return add_cors_headers(response)
    response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return add_cors_headers(response)


# add to favorite
class AddFavoriteView(APIView):
    def post(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            return add_cors_headers(response)
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return add_cors_headers(response)


@method_decorator(csrf_exempt, name='dispatch')
class RemoveFavoriteView(View):
    def delete(self, request, tmdb_movie_id, user_id):
        try:
            # Fetch the Favorite object by tmdb_movie_id and user_id
            favorite = get_object_or_404(Favorite, tmdb_movie_id=tmdb_movie_id, user__id=user_id)
            # Delete the favorite
            favorite.delete()
            response = JsonResponse({'success': True, 'message': 'Movie removed from favorites successfully.'})
            return add_cors_headers(response)
        except Exception as e:
            response = JsonResponse({'success': False, 'error': str(e)})
            return add_cors_headers(response)


# get the favorite movies
class FavoriteMoviesView(APIView):
    def get(self, request, user_id, format=None):
        print(user_id)
        movies = Favorite.objects.filter(user_id=user_id)
        serializer = FavoriteMovieSerializer(movies, many=True)
        response = Response({'movies': serializer.data}, status=status.HTTP_200_OK)
        return add_cors_headers(response)


class getFavoriteSeriesView(APIView):
    def get(self, request, user_id, format=None):
        print(user_id)
        series = Favorite_series.objects.filter(user_id=user_id)
        serializer = FavoriteSeriesSerializer(series, many=True)
        response = Response({'series': serializer.data}, status=status.HTTP_200_OK)
        return add_cors_headers(response)


@method_decorator(csrf_exempt, name='dispatch')
class RemoveFavoriteSeriesView(View):
    def delete(self, request, tmdb_series_id, user_id):
        try:
            # Fetch the Favorite object by tmdb_series_id and user_id
            favorite_series = get_object_or_404(Favorite_series, tmdb_series_id=tmdb_series_id, user_id=user_id)
            # Delete the favorite
            favorite_series.delete()
            response = JsonResponse({'success': True, 'message': 'Series removed from favorites successfully.'})
            return add_cors_headers(response)
        except Exception as e:
            response = JsonResponse({'success': False, 'error': str(e)})
            return add_cors_headers(response)
