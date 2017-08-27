# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from django.utils.translation import ugettext_lazy as _
from . import models


class UserAdmin(OriginalUserAdmin):
    pass


class MediaFileAdmin(PolymorphicParentModelAdmin):

    base_model = models.MediaFile
    polymorphic_list = True
    list_display = ['title', 'uploaded_by', 'status', 'description', 'serialized_categories']
    list_display_links = ['title']

    class MediaFileHistoryInlineAdmin(admin.TabularInline):
        model = models.MediaFileHistory
        fields = ('created_on', 'changed_by', 'status', 'details')
        readonly_fields = ('created_on', 'changed_by', 'status', 'details')

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False

    inlines = [MediaFileHistoryInlineAdmin]

    def serialized_categories(self, obj):
        return ''.join([tag.name for tag in obj.categories.all()])
    serialized_categories.short_description = _(u'Categories')

    class ImageAdmin(PolymorphicChildModelAdmin):

        base_model = models.MediaFile

    class EmbedAdmin(PolymorphicChildModelAdmin):

        base_model = models.MediaFile

    # TODO logic for adding a new History when saving the object.
    # TODO this includes a distinct form with an additional field.
    # TODO also deleting the inspection notes field in the MediaFile model.

    def get_child_models(self):
        return [
            (models.Image, self.ImageAdmin),
            (models.Embed, self.EmbedAdmin)
        ]


class TagAdmin(admin.ModelAdmin):

    fields = ('code', 'name', 'special')
    list_display = ('code', 'name', 'special')
    list_display_links = ('code',)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.MediaFile, MediaFileAdmin)
admin.site.register(models.Tag, TagAdmin)
