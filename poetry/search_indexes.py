from haystack import indexes
from poetry.models import *


# 注意格式  （模型类名+Index）
class PoetryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    # 给title,dynasty,author,tag,text2,translation,annotation,appreciation设置索引
    poetry_title = indexes.NgramField(model_attr='poetry_title')
    poetry_text = indexes.NgramField(model_attr='poetry_text')
    poetry_translation = indexes.NgramField(model_attr='poetry_translation')
    poetry_annotation = indexes.NgramField(model_attr='poetry_annotation')
    poetry_appreciation = indexes.NgramField(model_attr='poetry_appreciation')

    poetry_dynasty = indexes.CharField()
    poetry_author = indexes.CharField()
    poetry_tag = indexes.CharField()

    def get_model(self):
        return Poetry

    def index_queryset(self, using=None):
        return self.get_model().objects.order_by('poetry_no')
