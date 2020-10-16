from django.db import models
from django.db.models import Manager


# Create your models here.
# 创建朝代表(唐朝,宋朝等)
class Dynasty(models.Model):
    dynasty_no = models.AutoField(primary_key=True)
    dynasty_name = models.CharField(max_length=30)

    def __str__(self):
        return u'Dynasty:%s' % self.dynasty_name

    class Meta:
        db_table = 't_dynasty'


# 创建作者表(李白，杜甫等)
class Author(models.Model):
    author_no = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=30)
    author_dynasty = models.ForeignKey(Dynasty, on_delete=models.CASCADE)

    def __str__(self):
        return u'Author:%s' % self.author_name

    class Meta:
        db_table = 't_author'


# 创建标签表(言情，爱国等)
class Tag(models.Model):
    tag_no = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=30)

    def __str__(self):
        return u'Tag:%s' % self.tag_name

    class Meta:
        db_table = 't_tag'


# 创建题目表(静夜思，望庐山瀑布等)
class Title(models.Model):
    title_no = models.AutoField(primary_key=True)
    title_name = models.CharField(max_length=30)

    def __str__(self):
        return u'Title:%s' % self.title_name

    class Meta:
        db_table = 't_title'


# Poetry.objects.create(poetry_title='静夜思',poetry_author='李白',poetry_dynasty=‘唐’,poetry_tag=(‘月亮’，‘思乡’),poetry_text='窗前明月光，疑是地上霜。举头望明月，低头思故乡',poetry_translation='译文',poetry_annotation='注解',poetry_appreciation='赏析')

class MyManage(Manager):
    def getDynasty(self, dynasty):
        try:
            dy = Dynasty.objects.get(dynasty_name=dynasty)
        except Dynasty.DoesNotExist:
            dy = Dynasty.objects.create(dynasty_name=dynasty)
        return dy

    def getTitle(self, title):
        try:
            tl = Title.objects.get(title_name=title)
        except Title.DoesNotExist:
            tl = Title.objects.create(title_name=title)
        return tl

    def getAuthor(self, author, dynasty):
        try:
            au = Author.objects.get(author_name=author, author_dynasty=dynasty)
        except Author.DoesNotExist:
            au = Author.objects.create(author_name=author, author_dynasty=dynasty)
        return au

    def getTag(self, *tag):
        tagList = []
        for t in tag:
            try:
                ta = Tag.objects.get(tag_name=t)
            except Tag.DoesNotExist:
                ta = Tag.objects.create(tag_name=t)
            tagList.append(ta)
        return tagList

    def create(self, **kwargs):
        # 获取朝代对象
        dynasty = kwargs["poetry_dynasty"]
        dy = self.getDynasty(dynasty)
        kwargs["poetry_dynasty"] = dy
        # 获取题目对象
        title = kwargs["poetry_title"]
        tl = self.getTitle(title).title_name
        kwargs["poetry_title"] = tl
        # 获取作者对象
        author = kwargs["poetry_author"]
        au = self.getAuthor(author, dy)
        kwargs["poetry_author"] = au
        # 获取正文信息
        text = kwargs["poetry_text"]
        # 获取标签对象
        tagList = kwargs.pop("poetry_tag")
        try:
            poetry = Manager.get(self, poetry_text=text)
        except Poetry.DoesNotExist:
            poetry = Manager.create(self, **kwargs)
        tag = self.getTag(*tagList)
        poetry.poetry_tag.add(*tag)


# 创建古诗内容表(包含题目，朝代，作者，正文，译文，注解，赏析，标签)
class Poetry(models.Model):
    poetry_no = models.AutoField(primary_key=True)
    poetry_title = models.CharField(max_length=30)
    poetry_dynasty = models.ForeignKey(Dynasty, on_delete=models.CASCADE)
    poetry_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    poetry_tag = models.ManyToManyField(Tag)
    poetry_text = models.TextField()  # 正文
    poetry_translation = models.TextField()  # 译文
    poetry_annotation = models.TextField()  # 注解
    poetry_appreciation = models.TextField()  # 赏析
    objects = MyManage()

    def __str__(self):
        return u'Poetry:%s%s' % (self.poetry_title, self.poetry_no)

    class Meta:
        db_table = 't_poetry'


class AuthorDetails(models.Model):
    ad_no = models.AutoField(primary_key=True)
    ad_name = models.CharField(max_length=30)
    ad_introduce = models.TextField()

    def __str__(self):
        return u'AuthorDetails:%s' % self.ad_name

    class Meta:
        db_table = 't_authordetails'
