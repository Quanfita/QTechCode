from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify
from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from .models import Resource
from django.core.cache import cache
from django.views.decorators.http import require_POST
from django.contrib.auth.models import AnonymousUser
from markdown.extensions.toc import TocExtension  # 锚点的拓展
from django.views.decorators.csrf import csrf_exempt 
import markdown
import time
import json
import datetime

# Create your views here.

class IndexView(generic.ListView):
	model = Resource
	template_name = 'resource/index.html'
	context_object_name = 'resources'
	paginate_by = None
	paginate_orphans = 0

	def get_ordering(self):
		sort = self.kwargs.get('sort')
		if sort == 'v':
			return ('-views', '-update_date', '-id')
		return ('-is_top', '-create_date')

class DetailView(generic.DetailView):
	model = Resource
	template_name = 'resource/detail.html'
	context_object_name = 'resource'

	def get_object(self):
		obj = super(DetailView, self).get_object()
		# 设置浏览量增加时间判断,同一篇文章两次浏览超过半小时才重新统计阅览量,作者浏览忽略
		u = self.request.user
		ses = self.request.session
		the_key = 'is_read_{}'.format(obj.id)
		is_read_time = ses.get(the_key)
		if u != obj.author:
			if not is_read_time:
				obj.update_views()
				ses[the_key] = time.time()
			else:
				now_time = time.time()
				t = now_time - is_read_time
				if t > 60 * 30:
					obj.update_views()
					ses[the_key] = time.time()
		# 获取文章更新的时间，判断是否从缓存中取文章的markdown,可以避免每次都转换
		ud = obj.update_date.strftime("%Y%m%d%H%M%S")
		md_key = '{}_md_{}'.format(obj.id, ud)
		cache_md = cache.get(md_key)
		if cache_md:
			obj.body, obj.toc = cache_md
		else:
			md = markdown.Markdown(extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
				TocExtension(slugify=slugify),
			])
			obj.body = md.convert(obj.body)
			obj.toc = md.toc
			cache.set(md_key, (obj.body, obj.toc), 60 * 60 * 12)
		return obj

@require_POST
def update_downloads(request):
	if request.is_ajax() and request.method == "POST":
		data = request.POST
		_id = data.get('id')
		Resource.objects.filter(id=_id).first().update_download()
		return HttpResponse('ok')
	return HttpResponse('error')
