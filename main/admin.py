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
    list_display = ['created_on', 'title', 'uploaded_by', 'status', 'details', 'serialized_tags']
    list_display_links = ['title']
    search_fields = ['uploaded_by__username', 'title', 'details']

    def serialized_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])
    serialized_tags.short_description = _(u'Tags')

    child_models = (models.Image, models.Embed, models.Album)


class MediaChildAdmin(PolymorphicChildModelAdmin):

    fieldsets = (
        (_('Life Cycle'), {'fields': (('uploaded_by', 'status'),)}),
        (_('Details'), {'fields': ('title', 'details', 'tags')}),
        (_('Internal'), {'fields': ('inspection_notes',)})
    )
    base_model = models.Media

    class MediaHistoryInlineAdmin(admin.TabularInline):
        fk_name = 'media_file'
        model = models.MediaHistory
        fields = ('created_on', 'changed_by', 'status', 'details')
        readonly_fields = ('created_on', 'changed_by', 'status', 'details')

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return True

        def has_delete_permission(self, request, obj=None):
            return False

    inlines = [MediaHistoryInlineAdmin]

    def save_model(self, request, obj, form, change):
        """
        Creates an instance of history if status is changed or the obj is just created
        """

        notes = obj.inspection_notes
        super(MediaChildAdmin, self).save_model(request, obj, form, change)
        if not change or 'status' in form.changed_data:
            obj.histories.create(changed_by=request.user, details=notes, status=obj.status)


class ImageAdmin(MediaChildAdmin):

    fieldsets = MediaChildAdmin.fieldsets + (
        (_('Content'), {'fields': ('file',)}),
    )


class EmbedAdmin(MediaChildAdmin):

    fieldsets = MediaChildAdmin.fieldsets + (
        (_('Content'), {'fields': (('engine', 'content'),)}),
    )


class AlbumAdmin(MediaChildAdmin):

    class AlbumEntryInline(admin.TabularInline):
        fk_name = 'album'
        model = models.AlbumEntry
        fields = ('created_on', 'sequence', 'element')
        readonly_fields = ('created_on',)

    inlines = [AlbumEntryInline] + MediaChildAdmin.inlines


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
