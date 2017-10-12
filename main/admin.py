# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from django.utils.translation import ugettext_lazy as _
from . import models


class UserAdmin(OriginalUserAdmin):
    pass


class MediaAdmin(PolymorphicParentModelAdmin):

    base_model = models.Media
    polymorphic_list = True
    list_display = ['created_on', 'title', 'uploaded_by', 'status', 'details', 'serialized_categories']
    list_display_links = ['title']
    search_fields = ['uploaded_by__username', 'title', 'details']

    class MediaHistoryInlineAdmin(admin.TabularInline):
        model = models.MediaHistory
        fields = ('created_on', 'changed_by', 'status', 'details')
        readonly_fields = ('created_on', 'changed_by', 'status', 'details')

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False

    inlines = [MediaHistoryInlineAdmin]

    def serialized_categories(self, obj):
        return ', '.join([tag.name for tag in obj.categories.all()])
    serialized_categories.short_description = _(u'Categories')

    # TODO logic for adding a new History when saving the object.
    # TODO this includes a distinct form with an additional field.
    # TODO also deleting the inspection notes field in the Media model.

    child_models = (models.Image, models.Embed, models.Album)


class PolymorphicMediaChildModelAdmin(PolymorphicChildModelAdmin):

    fieldsets = (
        (_('Life Cycle'), {'fields': (('uploaded_by', 'status'),)}),
        (_('Details'), {'fields': ('title', ('details', 'tags'))}),
        (_('Internal'), {'fields': ('inspection_notes',)})
    )
    base_model = models.Media


class ImageAdmin(PolymorphicMediaChildModelAdmin):

    fieldsets = PolymorphicMediaChildModelAdmin.fieldsets + (
        (_('Content'), {'fields': ('file',)}),
    )


class EmbedAdmin(PolymorphicMediaChildModelAdmin):

    fieldsets = PolymorphicMediaChildModelAdmin.fieldsets + (
        (_('Content'), {'fields': (('engine', 'content'),)}),
    )


class AlbumAdmin(PolymorphicMediaChildModelAdmin):

    pass


class TagAdmin(admin.ModelAdmin):

    fields = ('code', 'name', 'special')
    list_display = ('code', 'name', 'special')
    list_display_links = ('code',)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Media, MediaAdmin)
admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.Embed, EmbedAdmin)
admin.site.register(models.Album, AlbumAdmin)
admin.site.register(models.Tag, TagAdmin)
