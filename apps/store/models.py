from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from blog.models import Keyword
import markdown

# Create your models here.

class Item(models.Model):
    type_choice = (
        ('1', '自动发货'),
        ('2', '脚本发货'),
        ('3', '其他')
    )
    IMG_LINK = '/static/store/img/store.jpg'
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='提供者', on_delete=models.PROTECT)
    title = models.CharField(max_length=150, verbose_name='资源标题')
    summary = models.TextField('资源摘要', max_length=230, default='资源摘要等同于网页description内容，请务必填写...')
    body = models.TextField(verbose_name='资源内容')
    img_link = models.CharField('图片地址', default=IMG_LINK, max_length=255)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.IntegerField('浏览量', default=0)
    deliver_type = models.CharField('发货类型', choices=type_choice, max_length=1, default='1')
    deliver_info = models.TextField('发货信息', default='')
    
    slug = models.SlugField(unique=True)
    is_top = models.BooleanField('置顶', default=False)
    price = models.IntegerField('价格', default=0)
    amount = models.IntegerField('总量', default=0)
    sales = models.IntegerField('销售量', default=0)

    keywords = models.ManyToManyField(Keyword, verbose_name='资源关键词',
                                      help_text='资源关键词，用来作为SEO中keywords，最好使用长尾词，3-4个足够')

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']
    
    def get_deliver(self):
        if self.deliver_type == '1':
            return self.deliver_to_markdown()
        elif self.deliver_type == '2':
            return None
        elif self.deliver_type == '3':
            return self.deliver_info

    def __str__(self):
        return self.title[:20]

    def get_absolute_url(self):
        return reverse('store:detail', kwargs={'slug': self.slug})

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

    def get_pre(self):
        return Item.objects.filter(id__lt=self.id).order_by('-id').first()

    def get_next(self):
        return Item.objects.filter(id__gt=self.id).order_by('id').first()


class Order(models.Model):
    type_choice = (
        ('1', '微信'),
        ('2', '支付宝'),
    )
    good = models.ForeignKey(Item, verbose_name='商品', on_delete=models.PROTECT)
    remark = models.TextField('备注', max_length=200, default='')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    confirm_date = models.DateTimeField(verbose_name='支付时间', auto_now=True)
    realPrice = models.IntegerField('实际支付金额', default=0)
    uid = models.CharField('订单编号', max_length=128, unique=True)
    is_confirmed = models.BooleanField(default=False)
    pay_type = models.CharField('支付方式', choices=type_choice, max_length=1, default='1')
    pay_url = models.CharField('支付链接', max_length=256, default='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='购买者', on_delete=models.PROTECT)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.uid