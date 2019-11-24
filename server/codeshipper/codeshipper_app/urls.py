from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r"^$", misc.root_path, name="index"),
    url(r"index$", misc.index, name="index"),
    url(r"^dashboard$", misc.index, name="index"),

    url(r"^server/?$", server.left_menu_server, name="index"),
    url(r"^server/list/?$", server.left_menu_server, name="index"),
    url(r"^server/create/?$", server.server_create, name="index"),
    url(r"^server/detail/?$", server.server_detail, name="index"),
    url(r"^server/test_connection/?$", server.controllers.test_connection, name="test_connection"),
    url(r"^server/create_new_server/?$", server.controllers.create_new_server, name="create_new_server"),


    url(r"^project/?$", project.left_menu_project, name="index"),
    url(r"^project/list/?$", project.left_menu_project, name="index"),
    url(r"^project/create/?$", project.project_create, name="index"),
    url(r"^project/create_new_project/?$", project.controllers.create_new_project, name="index"),
    url(r"^user/?$", misc.left_menu_users, name="index"),

    # fonts
    url(r"a1ecc3b826d01251edddf29c3e4e1e97.woff/?$", misc.a1ecc3b826d01251edddf29c3e4e1e97_woff),
    url(r"af7ae505a9eed503f8b8e6982036873e.woff2/?$", misc.af7ae505a9eed503f8b8e6982036873e_woff2),
    url(r"fee66e712a8a08eef5805a46892932ad.woff/?$", misc.fee66e712a8a08eef5805a46892932ad_woff),
]
