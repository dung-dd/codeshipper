from django.conf.urls import url
from django.urls import path
from .views import *


urlpatterns = [
    url(r"^$", misc.root_path, name="index"),
    url(r"index$", misc.index, name="index"),
    url(r"^dashboard$", misc.index, name="index"),


    # Servers
    url(r"^server/?$", server.left_menu_server, name="index"),
    url(r"^server/list/?$", server.left_menu_server, name="index"),
    url(r"^server/test_connection/?$", server.controllers.test_connection, name="test_connection"),

    url(r"^server/create/?$", server.server_create, name="index"),
    path(r"server/<str:server_id>/", server.server_detail, name="server_detail"),

    url(r"^server/create_server/?$", server.controllers.create_server, name="create_server"),
    url(r"^server/update_server/?$", server.controllers.update_server, name="update_server"),
    url(r"^server/delete/?$", server.controllers.delete_server, name="delete_server"),


    # Projects
    url(r"^project/?$", project.left_menu_project, name="index"),
    url(r"^project/list/?$", project.left_menu_project, name="index"),
    url(r"^project/create/?$", project.project_create, name="index"),
    path(r"project/<str:project_id>/", project.project_detail, name="index"),

    url(r"^project/create_project/?$", project.controllers.create_project, name="index"),
    url(r"^project/update/?$", project.controllers.update_project, name="index"),
    url(r"^project/delete/?$", project.controllers.delete_project, name="index"),


    url(r"^project/type/?$", project.left_menu_project_type, name="index"),
    url(r"^project/type/create/?$", project.left_menu_project_type_create, name="index"),
    url(r"^project/type/create_project_type/?$", project.controllers.pt.pt_create_project_type, name="index"),
    url(r"^project/type/update/?$", project.controllers.pt.pt_update_project_type, name="index"),
    url(r"^project/type/delete/?$", project.controllers.pt.pt_delete_project_type, name="index"),
    path(r"project/type/<str:project_type_id>/", project.project_type_detail, name="index"),

    url(r"^project/get_config_project_type/?$", project.controllers.pt.get_config_project_type, name="index"),

    url(r"^user/?$", misc.left_menu_users, name="index"),

    # fonts
    url(r"a1ecc3b826d01251edddf29c3e4e1e97.woff/?$", misc.a1ecc3b826d01251edddf29c3e4e1e97_woff),
    url(r"af7ae505a9eed503f8b8e6982036873e.woff2/?$", misc.af7ae505a9eed503f8b8e6982036873e_woff2),
    url(r"fee66e712a8a08eef5805a46892932ad.woff/?$", misc.fee66e712a8a08eef5805a46892932ad_woff),
]
