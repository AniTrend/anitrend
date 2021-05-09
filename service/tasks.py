from django.utils import timezone

from service.dependencies import UseCaseProvider


def poll_from_xem(*args, **kwargs):
    """
    Syncs all the relation if any of them was last updated more than 1 week ago
    """
    one_week_ago = timezone.now() - timezone.timedelta(weeks=1)
    use_case = UseCaseProvider.xem_use_case()
    use_case.fetch_all_mappings(one_week_ago)


def poll_from_relations(*args, **kwargs):
    """
    Syncs all the relation if any of them was last updated more than 1 week ago
    """
    one_week_ago = timezone.now() - timezone.timedelta(weeks=1)
    use_case = UseCaseProvider.relation_use_case()
    use_case.fetch_all_records(one_week_ago)


def merge_entries(*args, **kwargs):
    """
    Mergers data from both source into one source of truth
    """
    pass


