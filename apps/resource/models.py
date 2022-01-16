from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from blog.models import Keyword
import markdown

# Create your models here.

class Resource(models.Model):
    types_choice=(
        ('1', 'PDF'),
        ('2', 'ZIP'),
    )
    IMG_LINK = '/static/resource/img/resource.png'
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='提供者', on_delete=models.PROTECT)
    title = models.CharField(max_length=150, verbose_name='资源标题')
    summary = models.TextField('资源摘要', max_length=230, default='资源摘要等同于网页description内容，请务必填写...')
    body = models.TextField(verbose_name='资源内容')
    resource_type = models.CharField('资源格式', choices=types_choice, max_length=1, default='1')
    img_link = models.CharField('图片地址', default=IMG_LINK, max_length=255)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.PositiveIntegerField('浏览量', default=0)
    download = models.PositiveIntegerField('下载量', default=0)
    url = models.CharField('资源链接', max_length=255, default='',blank=True,null=True)
    baidu_url = models.CharField('资源百度网盘链接', max_length=255, default='',blank=True,null=True)
    baidu_code = models.CharField('资源百度网盘提取码', max_length=10, default='',blank=True,null=True)

    slug = models.SlugField(unique=True)
    is_top = models.BooleanField('置顶', default=False)

    keywords = models.ManyToManyField(Keyword, verbose_name='资源关键词',
                                      help_text='资源关键词，用来作为SEO中keywords，最好使用长尾词，3-4个足够')

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title[:20]

    def get_absolute_url(self):
        return reverse('resource:detail', kwargs={'slug': self.slug})

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
    
    def deliver_to_markdown(self):
        return markdown.markdown(self.deliver_info, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def update_download(self):
        self.download += 1
        self.save(update_fields=['download'])

    def get_pre(self):
        return Resource.objects.filter(id__lt=self.id).order_by('-id').first()

    def get_next(self):
        return Resource.objects.filter(id__gt=self.id).order_by('id').first()
    
    def get_filename(self):
        return Resource.objects.filter(id=self.id).first().url.split('/')[-1]
