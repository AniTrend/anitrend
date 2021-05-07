from django.utils import timezone

from service.dependencies import UseCaseProvider


def get_all_data_from_xem():
    """
    Syncs all the relation if any of them was last updated more than 1 week ago
    """
    one_week_ago = timezone.now() - timezone.timedelta(weeks=1)
    use_case = UseCaseProvider.xem_use_case()
    use_case.fetch_all_mappings(one_week_ago)


def get_all_data_from_relations():
    """
    Syncs all the relation if any of them was last updated more than 1 week ago
    """
    one_week_ago = timezone.now() - timezone.timedelta(weeks=1)
    use_case = UseCaseProvider.relation_use_case()
    use_case.fetch_all_records(one_week_ago)


def merge_relational_entries():
    """
    Deletes dead entries if any of them was last updated more than 1 week ago
    """
    one_week_ago = timezone.now() - timezone.timedelta(weeks=1)
    pass


def delete_dead_entries():
    """
    Deletes dead entries if any of them was last updated more than 1 week ago
    """
    one_week_ago = timezone.now() - timezone.timedelta(weeks=1)
    pass
