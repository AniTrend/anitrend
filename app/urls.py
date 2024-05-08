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
from django.contrib import admin
from django.urls import path, include
from django.urls.resolvers import RoutePattern
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphql_playground.views import GraphQLPlaygroundView


def build_url_patterns() -> List[RoutePattern]:
    if settings.DEBUG:
        static_routes = static(
            prefix=settings.STATIC_URL,
            document_root=settings.STATIC_ROOT
        ) + static(
            prefix=settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT
        )
        return [
            path("", include('web.urls')),
            path('admin', admin.site.urls),
            path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=False))),
            path("playground", csrf_exempt(GraphQLPlaygroundView.as_view(endpoint="/graphql"))),
        ] + static_routes
    return [
        path("", include('web.urls')),
        path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=False))),
    ]


urlpatterns = build_url_patterns()
