# search_indexes.py

from haystack import indexes
from .models import RopaHombre

class RopaHombreIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    precio = indexes.CharField(model_attr='precio')

    def get_model(self):
        return RopaHombre
