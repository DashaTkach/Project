from django.db import connection

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render

from .statistics import Statistic
from .user_photo import UserPhoto
from .utils import DataMixin
from .forms import *


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'demo/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'demo/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        if self.request.user.is_admin == True:
            return reverse_lazy('admin_page')
        else:
            return reverse_lazy('get_photo')


def logout_user(request):
    logout(request)
    return redirect('login')


def index(request):
    return render(request, 'demo/index.html')


def dowload_statistics(request):
    list_of_models = [Posts, PartFace, Shades]
    if request.method == 'POST':
        for model in list_of_models:
            with connection.cursor() as cursor:
                cursor.execute(f'TRUNCATE TABLE "{model._meta.db_table}" CASCADE;')

        VK_token = ''
        # здесь надо словарь с названиями и айдишниками пабликов, добавить очередь
        params = {
            'owner_id': '197545707',
            'count': 20,
            'domain': 'nadin_artmakeup',
            'access_token': VK_token,
            'v': '5.131'
        }
        some = Statistic()  # потом это будет паблик (один из)
        some.dowload_photos(some.filter(some.get_data(params)))
        some.post_data_posts()
        return render(request, 'demo/dowload_statistics.html')
    return render(request, 'demo/dowload_statistics.html', {'numbers': [1, 2]})


def user_photo(request):
    if request.method == 'POST':
        user_photo = UserPhoto()
        user_photo.get_photo(request)
        user_photo.post_photos(request)
        return redirect('criteria')
    return render(request, 'demo/get_photo.html', {'numbers': [1, 2]})


def find_nearest_hue(rgb):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    max_value = max(r, g, b)
    min_value = min(r, g, b)
    if max_value == min_value:
        hue = 0
    elif max_value == r:
        hue = (60 * ((g - b) / (max_value - min_value)) + 360) % 360
    elif max_value == g:
        hue = (60 * ((b - r) / (max_value - min_value)) + 120) % 360
    else:
        hue = (60 * ((r - g) / (max_value - min_value)) + 240) % 360
    nearest_hue = round(hue)
    hue_names = {
        0: "Красный",
        15: "Оранжево-красный",
        30: "Оранжевый",
        45: "Оранжево-желтый",
        60: "Желтый",
        75: "Лимонно-желтый",
        90: "Лимонный",
        105: "Лаймовый",
        120: "Зеленый",
        135: "Зелено-голубой",
        150: "Голубой",
        165: "Сине-голубой",
        180: "Голубой",
        195: "Сине-фиолетовый",
        210: "Синий",
        225: "Сине-фиолетовый",
        240: "Синий",
        255: "Фиолетово-синий",
        270: "Фиолетовый",
        285: "Малиновый",
        300: "Розовый",
        315: "Розово-красный",
        330: "Красный",
        345: "Оранжево-красный",
        360: "Красный"
    }
    nearest_name = hue_names[min(hue_names.keys(), key=lambda x: abs(x - nearest_hue))]
    return nearest_name


def post_part_category():
    posts = Posts.objects.all().values()
    list_of_posts = []
    for post in list(posts):
        dict_post = {}
        post_part_face = PartFace.objects.filter(post_id=post['id']).values()
        image = post['post_image']
        part_faces = {}
        for part_face in list(post_part_face):
            shade_list = []
            post_shade = Shades.objects.filter(part_face_id=part_face['id']).values().first()
            rgb = [
                post_shade['rcor_photo'],
                post_shade['gcor_photo'],
                post_shade['bcor_photo']
            ]
            shade_list.append(rgb)
            post_part_category = find_nearest_hue(rgb)
            shade_list.append(post_part_category)
            part_faces[f'{part_face["post_part_face"]}'] = shade_list
        dict_post[image] = part_faces
        list_of_posts.append(dict_post)
    return list_of_posts


def criteria(request):
    context = {}
    if request.method == 'POST':
        form = CriteriaForm(request.POST)
        if form.is_valid():
            temp = form.cleaned_data.get("field")  # здесь части лица, по которым отбор (губы)
            if '1' in temp:
                temp[0] = 'upper_lip'
                if '2' in temp:
                    temp[1] = 'left_eyel'
            else:
                temp[0] = 'left_eyel'
            temp.append('face_tone')
            nes_images = []
            images = UserImages.objects.filter(user_id=request.user.id)
            if images.exists():
                image = images.latest('id')
                parts = UserPartFace.objects.filter(user_image_id=image.id).values()
                p_f = {}
                for part in list(parts):
                    rgb = []
                    if part['user_part_face'] in temp:
                        shade = UserShades.objects.filter(user_part_face_id=part['id']).values().first()
                        if shade:
                            rcor_user_photo = shade['rcor_user_photo']
                            rgb.append(rcor_user_photo)
                            gcor_user_photo = shade['gcor_user_photo']
                            rgb.append(gcor_user_photo)
                            bcor_user_photo = shade['bcor_user_photo']
                            rgb.append(bcor_user_photo)
                            user_part_category = find_nearest_hue(rgb)
                            p_f[f'{part["user_part_face"]}'] = user_part_category
                list_of_posts = post_part_category()
                for nes_part, nes_cat in p_f.items():
                    for post in list_of_posts:
                        for k, v in post.items():
                            for key, value in v.items():
                                if nes_part == key and nes_cat == value[1]:
                                    # image_path = str(Path(*Path(k).parts[-3:]))
                                    # image_path = k.replace("\\", "/")
                                    # nes_images.append(k)
                                    nes_images.append(k)
                return render(request, "demo/result.html", {'temp': list_of_posts})
            # return render(request, "demo/result.html", {'photo_paths': nes_images})
    else:
        form = CriteriaForm()
    context['form'] = form
    return render(request, "demo/criteria.html", context)
