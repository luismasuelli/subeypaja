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
