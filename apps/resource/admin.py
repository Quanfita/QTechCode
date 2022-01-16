from django.conf import settings
from django.apps import apps
from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    # 这个的作用是给出一个筛选机制，一般按照时间比较好
    date_hierarchy = 'create_date'

    exclude = ('views','download')

    # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
    list_display = ('id', 'title', 'author', 'create_date', 'update_date', 'views', 'download', 'is_top')

    # 设置需要添加<a>标签的字段
    list_display_links = ('title',)

    # 激活过滤器，这个很有用
    list_filter = ('create_date', 'author', 'is_top')

    list_per_page = 50  # 控制每页显示的对象数量，默认是100

    filter_horizontal = ('keywords',)  # 给多选增加一个左右添加的框

    search_fields = ('author__username', 'title')

    # 限制用户权限，只能看到自己编辑的文章
    def get_queryset(self, request):
        qs = super(ResourceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        User = apps.get_model(settings.AUTH_USER_MODEL)
        if db_field.name == 'author':
            if request.user.is_superuser:
                kwargs['queryset'] = User.objects.filter(is_staff=True, is_active=True)
            else:
                kwargs['queryset'] = User.objects.filter(id=request.user.id)
        return super(ResourceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
