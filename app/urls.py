"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from typing import List

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls.resolvers import RoutePattern
from django.views.decorators.csrf import csrf_exempt

from app.views.graphql_view import AsyncPatchedGraphQLView
from app.views.graphql_ws import websocket_view
from app.graphql import schema


urlpatterns: List[RoutePattern] = [
    path("graphqlws", websocket_view(schema=schema)),
    path(
        "graphql",
        AsyncPatchedGraphQLView.as_view(
            schema=schema,
            graphql_ide=None,
            allow_queries_via_get=False,
            multipart_uploads_enabled=True,
        ),
    ),
]


if settings.DEBUG:
    urlpatterns += (
        [
            path(
                "playground",
                csrf_exempt(
                    AsyncPatchedGraphQLView.as_view(
                        schema=schema,
                        graphql_ide="apollo-sandbox",
                        multipart_uploads_enabled=True,
                    ),
                ),
            ),
        ]
    )
