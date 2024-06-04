import os

from django.core.management.base import BaseCommand
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .face_detection import Neuro


class UserPhoto(BaseCommand):

    @csrf_exempt
    def get_photo(self, request):
        if request.FILES.get('photo'):
            photo = request.FILES['photo']
            user_id = list(UserImages.objects.values_list('user_id', flat=True).distinct())
            if request.user.id in user_id:
                count_prevphoto = UserImages.objects.filter(user_id=request.user.id).count()
            else:
                count_prevphoto = 0
            file_path = os.path.join("demo/catalog_users", f'face-{request.user.id}.{count_prevphoto + 1}.jpg')
            with open(file_path, 'wb+') as destination:
                for chunk in photo.chunks():
                    destination.write(chunk)
        return file_path

    def post_photos(self, request):
        image_paths = []
        path = os.path.dirname(
            os.path.abspath(__file__)) + '\catalog_users'
        image_path = [os.path.join(path, f) for f in os.listdir(path)]
        image_paths.append(image_path[-1])
        neuro_user_photo = Neuro()
        neu = neuro_user_photo.neuro(image_paths)
        for photo in neu:
            for key_ph, dict in photo.items():
                user_image = UserImages.objects.create(user_image=key_ph, user_id=request.user.id)
                for key, value in dict.items():
                    user_part_face = UserPartFace.objects.create(user_part_face=key, user_image_id=user_image.id)
                    UserShades.objects.create(user_part_face_id=user_part_face.id, rcor_user_photo=value[0],
                                              gcor_user_photo=value[1],
                                              bcor_user_photo=value[2])
