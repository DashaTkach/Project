from django.contrib import admin

from .models import *


class UserImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_image', 'user_image_created', 'user_id')
    list_display_links = ('id', 'user_image', 'user_image_created',)
    search_fields = ('user_id',)

class UserPartFaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_part_face', 'user_image_id')
    list_display_links = ('id', 'user_part_face',)
    search_fields = ('user_image_id',)

class UserShadesAdmin(admin.ModelAdmin):
    list_display = ('id', 'bcor_user_photo', 'gcor_user_photo', 'rcor_user_photo', 'user_part_face_id')
    list_display_links = ('id', 'bcor_user_photo', 'gcor_user_photo', 'rcor_user_photo',)
    search_fields = ('user_part_face_id',)

class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_image', 'created')
    list_display_links = ('id', 'post_image', 'created')
    search_fields = ('id', )

class PartFaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_part_face', 'post_id')
    list_display_links = ('id', 'post_part_face')
    search_fields = ('post_id',)

class ShadesAdmin(admin.ModelAdmin):
    list_display = ('id', 'bcor_photo', 'gcor_photo', 'rcor_photo', 'part_face_id')
    list_display_links = ('id', 'bcor_photo', 'gcor_photo', 'rcor_photo')
    search_fields = ('part_face_id',)


admin.site.register(UserImages, UserImagesAdmin)
admin.site.register(UserPartFace, UserPartFaceAdmin)
admin.site.register(UserShades, UserShadesAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(PartFace, PartFaceAdmin)
admin.site.register(Shades, ShadesAdmin)
