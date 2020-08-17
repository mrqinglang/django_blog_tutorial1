from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image

class ArticleColumn(models.Model):
    """
    栏目的 Model
    """
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title

class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('article_detail', args=[self.id])
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    def save(self, *args, **kwargs):
        article = super(ArticlePost, self).save(*args, **kwargs)
        # 固定宽度缩放图片大小
        # 博文的标题图不是必须的，if中的self.avatar剔除掉没有标题图的文章，这些文章不需要处理图片。
        #
        # 不太好理解的是if中的这个not kwargs.get('update_fields')。还记得article_detail()
        # 视图中为了统计浏览量而调用了save(update_fields=['total_views'])吗？
        # 没错，就是为了排除掉统计浏览量调用的save()，免得每次用户进入文章详情页面都要处理标题图，太影响性能了。
        #接下来都是Pillow处理图片的流程了：打开原始图片，取得分辨率，将新图片的宽度设置为400并根据比例缩小高度，
        # 最后用新图片将原始图片覆盖掉。Image.ANTIALIAS表示缩放采用平滑滤波。
        # 最后一步，将父类save()返回的结果原封不动的返回去。
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article
