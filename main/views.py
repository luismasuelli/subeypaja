from django.views.generic import TemplateView
from . import constants


# These views are pretty standard.
from django.contrib.auth.views import (
    login, logout, password_change, password_change_done,
    password_reset, password_reset_complete, password_reset_confirm, password_reset_done,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin


class BaseContextMixin(ContextMixin):
    context_data = {}

    def get_context_data(self, **kwargs):
        context_data = super(BaseContextMixin, self).get_context_data(**kwargs)
        context_data.update({
            'SITE_TITLE': constants.SITE_TITLE
        })
        if self.context_data:
            context_data.update(self.context_data)
        return context_data


# This view will be used as base for static views (requires login!)
class UserTemplateViewWithContext(BaseContextMixin, LoginRequiredMixin, TemplateView):
    pass


# This one is the same but will not require login.
class TemplateViewWithContext(BaseContextMixin, TemplateView):
    pass


# Involved views and logic:
#
# 1. User logic
#
# - Main profile view (will work as a dashboard and few account details)
# - My Content (filterable content I uploaded)
# - View certain content (the content type will determine which template to render)
# - Edit/Delete/[Un]Publish certain content (the content type will determine which form to render)
# - Edit action, Delete action, Publish action, Unpublish action for the post attendants of the former screen.
# - Add content (get/post - You will be able to add 3 different elements: Image, Album, Embedded Video)
# - My Bookmarks (filterable list of bookmarks of contents or even user profiles)
# - Delete bookmark (get/post)
# - My Account (will work as account edition - several forms)
#
# Those views will be static and all located under /me urlspace.
