from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .serializers import PetSerializer
from rest_framework.decorators import api_view
from app.settings import API_KEY

from .models import Pet, Photo


# Create your views here.


@api_view(['GET', 'DELETE', 'POST'])
def pet_list(request):
    key = request.headers.get('X-API-KEY', None)
    if key != API_KEY:
        return JsonResponse({'message': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

    limit, offset, has_photo = get_params(request)

    if request.method == 'DELETE':
        return delete_all(request)
    elif request.method == 'POST':
        return add_pet(request)
    elif request.method == 'GET':
        return get_pets(has_photo, limit, offset)


@api_view(['GET', 'DELETE'])
def pet_detail(request, pk):
    try:
        pet = Pet.objects.get(pk=pk)
    except Pet.DoesNotExist:
        return JsonResponse({'message': 'Pet does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        pet_serializer = PetSerializer(pet)
        return JsonResponse(pet_serializer.data)

    elif request.method == 'DELETE':
        pet.delete()
        return JsonResponse({'message': 'Product was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def upload_photo(request, pk):
    image = request.data
    pet = Pet.objects.get(pk=pk)
    new_photo = Photo(pet=pet, photo=image['image'])  # save=True?
    new_photo.save()
    return JsonResponse({'message': 'added'}, status=status.HTTP_201_CREATED)


def get_pets(has_photo, limit, offset):
    if has_photo != 'nothing':
        if has_photo.upper() == 'TRUE':
            is_photo = True
        elif has_photo.upper() == 'FALSE':
            is_photo = False

        pets = Pet.objects.all().exclude(photo__isnull=is_photo)  # убрать all
        serialize_pet = PetSerializer(pets[offset:limit], many=True)
    else:
        pets = Pet.objects.all()
        serialize_pet = PetSerializer(pets[offset:limit], many=True)
    return JsonResponse(serialize_pet.data, safe=False)


def add_pet(request):
    pet_data = JSONParser().parse(request)
    pet_serializer = PetSerializer(data=pet_data)
    if pet_serializer.is_valid():
        pet_serializer.save()
        return JsonResponse(pet_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(pet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_params(request):
    params = request.query_params.dict()
    limit = int(params.get('limit', 20))
    offset = int(params.get('offset', 0))
    has_photo = params.get('has_photo', 'nothing')
    return limit, offset, has_photo


def delete_all(request):
    data = JSONParser().parse(request)
    delete_list = data.get('ids', [])
    Pet.objects.filter(pk__in=delete_list).delete()
    return JsonResponse({'message': 'Products were deleted successfully!'},
                        status=status.HTTP_204_NO_CONTENT)
