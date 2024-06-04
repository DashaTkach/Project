import os
from datetime import datetime

from django.core.management.base import BaseCommand
import requests as requests
from dateutil.relativedelta import relativedelta
from numpy import mean

from .face_detection import Neuro
from .models import *


class Statistic(BaseCommand):

    def get_data(self, params):
        URL = 'https://api.vk.com/method/wall.get'
        res = requests.get(URL, params=params).json()
        list_of_posts = []
        for inf in res['response']['items']:
            dict_for_post = {}
            dict_for_post['likes'] = inf['likes']['count']
            dict_for_post['views'] = inf['views']['count']
            post = []
            list_of_photos = []
            for d in inf['attachments']:
                for key, value in d.items():
                    if key == 'photo':
                        dict_for_post['create_date'] = datetime.fromtimestamp(value['date']).strftime('%Y-%m-%d')
                        for size in value['sizes']:
                            if size['type'] == 'x':
                                list_of_photos.append(size['url'])
            post.append(list_of_photos)
            post.append(dict_for_post)
            list_of_posts.append(post)
        return list_of_posts

    def filter(self, list_of_posts):
        relations = []
        date_gap = datetime.now() - relativedelta(years=1)
        res_photos = []
        for post in list_of_posts:
            relation = post[1]['likes'] / post[1]['views']
            post.append(relation)
            relations.append(relation)
        avarage_ind = mean(relations)
        for post in list_of_posts:
            if 'create_date' in list(post[1].keys()):
                if post[2] > avarage_ind and post[1]['create_date'] > str(date_gap.strftime('%Y-%m-%d')):
                    res_photos.append(post[0])
        return res_photos

    def dowload_photos(self, res_photos):
        path = os.path.abspath("demo/catalog_posts")
        list_of_titles = []
        for post in res_photos:
            ind_post = res_photos.index(post)
            for photo in post:
                ind_photo = post.index(photo)
                img_data = requests.get(photo).content
                list_of_titles.append(fr'face-{ind_post}.{ind_photo}.jpg')
                with open(fr'{path}\face-{ind_post}.{ind_photo}.jpg', 'wb') as file:
                    file.write(img_data)
        return list_of_titles

    def post_data_posts(self):
        path = os.path.dirname(
            os.path.abspath(__file__)) + '\catalog_posts'
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        neuro = Neuro()
        neu = neuro.neuro(image_paths)
        for photo in neu:
            for key_ph, dict in photo.items():
                post = Posts.objects.create(post_image=key_ph)
                for key, value in dict.items():
                    part_face = PartFace.objects.create(post_part_face=key, post=post)
                    Shades.objects.create(part_face=part_face, bcor_photo=value[2],
                                          gcor_photo=value[1], rcor_photo=value[0])
