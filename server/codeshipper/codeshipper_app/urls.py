from django.conf.urls import url
from django.urls import path
from .views import *


urlpatterns = [
    url(r"^$", misc.root_path, name="index"),
    url(r"index$", misc.index, name="index"),
    url(r"^dashboard$", misc.index, name="index"),


    # Servers
    url(r"^server/?$", server.left_menu_server, name="server_list_index"),
    url(r"^server/list/?$", server.left_menu_server, name="server_list"),
    url(r"^server/test_connection/?$", server.controllers.test_connection, name="server_test_connection"),

    url(r"^server/create/?$", server.server_create, name="index"),
    path(r"server/<str:server_id>/", server.server_detail, name="server_detail"),

    url(r"^server/create_server/?$", server.controllers.create_server, name="create_server"),
    url(r"^server/update_server/?$", server.controllers.update_server, name="update_server"),
    url(r"^server/delete/?$", server.controllers.delete_server, name="delete_server"),


    # Projects
    url(r"^project/?$", project.left_menu_project, name="project_list_index"),
    url(r"^project/list/?$", project.left_menu_project, name="project_list"),
    url(r"^project/create/?$", project.project_create, name="project_create"),
    path(r"project/<str:project_id>/", project.project_detail, name="project_detail"),

    url(r"^project/create_project/?$", project.controllers.create_project, name="project_create_api"),
    url(r"^project/update/?$", project.controllers.update_project, name="project_update_api"),
    url(r"^project/delete/?$", project.controllers.delete_project, name="project_delete_api"),

    url(r"^project/type/?$", project.left_menu_project_type, name="index"),
    url(r"^project/type/create/?$", project.left_menu_project_type_create, name="index"),
    url(r"^project/type/create_project_type/?$", project.controllers.pt.pt_create_project_type, name="project_type_create"),
    url(r"^project/type/update/?$", project.controllers.pt.pt_update_project_type, name="project_type_update"),
    url(r"^project/type/delete/?$", project.controllers.pt.pt_delete_project_type, name="project_type_delete_api"),
    path(r"project/type/<str:project_type_id>/", project.project_type_detail, name="project_type_detail"),

    url(r"^project/get_config_project_type/?$", project.controllers.pt.get_config_project_type, name="project_get_config_project_type"),

    # Updating
    url(r"^update/?$", update.left_menu_update, name="update_list_index"),
    url(r"^update/list/?$", update.left_menu_update, name="update_list"),
    url(r"^update/create/?$", update.update_create, name="update_create"),
    path(r"update/<str:update_id>/", update.update_detail, name="update_detail"),

    url(r"update/get_config_project/?", update.controllers.get_config_project, name="update_get_config_project"),
    url(r"update/create_update/?", update.controllers.create_update, name="create_update_api"),

    # users
    url(r"^user/?$", user.left_menu_user, name="user_list"),
    url(r"user/add_role/?$", user.controllers.add_role, name="user_add_role"),
    url(r"user/delete_role/?$", user.controllers.delete_role, name="user_delete_role"),

    path(r"user/<str:user_id>/", user.user_detail, name="user_detail"),
    


    # fonts
    url(r"a1ecc3b826d01251edddf29c3e4e1e97.woff/?$", misc.a1ecc3b826d01251edddf29c3e4e1e97_woff),
    url(r"af7ae505a9eed503f8b8e6982036873e.woff2/?$", misc.af7ae505a9eed503f8b8e6982036873e_woff2),
    url(r"fee66e712a8a08eef5805a46892932ad.woff/?$", misc.fee66e712a8a08eef5805a46892932ad_woff),
]
