from typing import Any

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from strawberry.django.views import AsyncGraphQLView, GraphQLView


@method_decorator(ensure_csrf_cookie, 'dispatch')
class AsyncPatchedGraphQLView(AsyncGraphQLView):
    async def get_context(self, request, response) -> Any:
        ctx = await super().get_context(request, response)
        # we currently don't have any dataloaders, because we're leveraging HTTP
        # we'll revisit this when we implement subscriptions
        # inject_dataloaders(ctx)
        return ctx


@method_decorator(ensure_csrf_cookie, 'dispatch')
class PatchedGraphQLView(GraphQLView):
    pass
