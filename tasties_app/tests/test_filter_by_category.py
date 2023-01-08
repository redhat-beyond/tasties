import pytest


@pytest.mark.django_db
class TestFilterByCategory:
    def test_recipes_filtered_by_category(self, client, categorized_recipes):
        #response = client.get(f'/?category?={categorized_recipes[1]}')
        import pdb
        pdb.set_trace()
