from django.conf.urls import url
from . import constants
from . import views

extra_context = {'SITE_TITLE': constants.SITE_TITLE}

app_name = 'main'
urlpatterns = [
    # URLs relacionadas al funcionamiento del sitio
    url('^$', views.TemplateViewWithContext.as_view(template_name='main/index.html'), name='index'),

    # TODO urls relacionadas al registro de usuario, configuracion de perfil, y cierre de cuenta

    # URLs relacionadas a login y to' eso.
    url('^forgot-password$', views.password_reset, kwargs=dict(
        template_name='main/forgot-password.html',
        email_template_name='main/mail/reset-password.txt',
        html_email_template_name='main/mail/reset-password.html',
        subject_template_name='main/mail/reset-password-subject.txt',
        post_reset_redirect='main:forgot-done',
        extra_email_context=extra_context,
        extra_context=extra_context
    ), name='forgot'),
    url('^forgot-password/done$', views.password_reset_done, kwargs=dict(
        template_name='main/forgot-password-done.html',
        extra_context=extra_context
    ), name='forgot-done'),
    url('^reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, kwargs=dict(
            post_reset_redirect='main:reset-done',
            template_name='main/reset-password.html',
            extra_context=extra_context
        ), name='reset'),
    url('^reset-password/done$', views.password_reset_complete, kwargs=dict(
        template_name='main/reset-password-done.html',
        extra_context=extra_context
    ), name='reset-done'),
    url('^profile/change-password$', views.password_change, kwargs=dict(
        post_change_redirect='main:password-change-done',
        template_name='main/change-password.html',
        extra_context=extra_context
    ), name='password-change'),
    url('^profile/change-password/done$', views.password_change_done, kwargs=dict(
        template_name='main/change-password-done.html',
        extra_context=extra_context
    ), name='password-change-done'),
    url('^login$', views.login, kwargs=dict(
        template_name='main/login.html',
        extra_context=extra_context
    ), name='login'),
    url('^logout$', views.logout, kwargs=dict(
        template_name='main/logout.html',
        extra_context=extra_context
    ), name='logout'),
]
