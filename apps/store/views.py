from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify
from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from .models import Item, Order
from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser
from markdown.extensions.toc import TocExtension  # 锚点的拓展
from .utils import getOrderInfo, checkCallback
from django.views.decorators.csrf import csrf_exempt 
import markdown
import time
import json
import datetime

# Create your views here.

class IndexView(generic.ListView):
	model = Item
	template_name = 'store/index.html'
	context_object_name = 'items'
	paginate_by = None
	paginate_orphans = 0

	def get_ordering(self):
		sort = self.kwargs.get('sort')
		if sort == 'v':
			return ('-views', '-update_date', '-id')
		return ('-is_top', '-create_date')

class DetailView(generic.DetailView):
	model = Item
	template_name = 'store/detail.html'
	context_object_name = 'item'

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


# Create your views here.

def PayView(request):
	if request.method == 'POST':
		pay_id = request.POST.get('pay_id')
		goodid = request.POST.get('goodid')
		create_time = request.POST.get('create_time')
		p_type = request.POST.get('p_type')
		good = Item.objects.get(id=goodid)
		notifyUrl = 'https://quanfita.cn/store/callback/'
		returnUrl = 'https://quanfita.cn/store/deliver/?orderid=%s' % pay_id
		res = getOrderInfo(pay_id, p_type, '%.2f' % (good.price/100), good.title, notifyUrl=notifyUrl, returnUrl=returnUrl)
		order = Order(
			uid=pay_id,
			create_date=datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S'),
			pay_type=p_type,
			good=good,
			pay_url=res,
			remark=good.get_deliver() if good.deliver_type == '1' else '',
			user=request.user
		)
		order.save()
		return HttpResponse(res)
	else:
		goodid = request.GET.get('goodsId')
		if goodid is None:
			return redirect('/')
		elif isinstance(request.user, AnonymousUser):
			return redirect('/accounts/login/')
		good = Item.objects.get(id=goodid)
		date = datetime.datetime.now()
		pay_id = date.strftime("%Y%m%d")+str(int(time.time() % 100000 *1000))
		create_time = date.strftime("%Y-%m-%d %H:%M:%S")
		price = good.price
		content = good.title
		context = {
			"goodid": goodid,
			"pay_id": pay_id,
			"create_time": create_time,
			"price": price,
			"content": content if len(content)<15 else content[:15]+'...'
		}
		return render(request, 'store/pay.html', context=context)

@csrf_exempt
def CallbackView(request):
	if request.method == 'POST':
		pay_id = request.GET.get('payId')
		param = request.GET.get('param')
		p_type = request.GET.get('type')
		price = request.GET.get('price')
		reallyPrice = request.GET.get('reallyPrice')
		sign = request.GET.get('sign')
		print(pay_id, param, p_type, price, reallyPrice, sign)
		print(checkCallback(pay_id, param, p_type, price, reallyPrice, sign))
		if checkCallback(pay_id, param, p_type, price, reallyPrice, sign):
			order = Order.objects.get(uid=pay_id)
			order.realPrice = int(float(reallyPrice) * 100)
			order.is_confirmed = True
			order.remark = order.good.get_deliver()
			order.good.sales += 1
			# order.amount -= 1
			order.good.save()
			order.save()
			return HttpResponse("success")
		else:
			HttpResponse("Failed", 403)
	return HttpResponse("Failed", 403)

def DeliverView(request):
	orderid = request.GET.get('orderid')
	order = Order.objects.get(uid=orderid)
	good = order.good
	if good.deliver_type in ['1','2'] and order.is_confirmed:
		info = good.get_deliver()
		context = {
			"info" : info,
			"orderid" : orderid,
			"content" : good.title,
			"price" : "%.2f" % (good.price/100),
			"realPrice" : "%.2f" % (order.realPrice/100),
			"confirm_date" : order.confirm_date,
			"pay_type" : order.get_pay_type_display()
		}
		return render(request, 'store/deliver.html', context=context)
	elif not order.is_confirmed:
		info = good.get_deliver()
		context = {
			"info" : info,
			"orderid" : orderid,
			"content" : good.title,
			"price" : "%.2f" % (good.price/100),
			# "realPrice" : "%.2f" % (order.realPrice/100),
			# "confirm_date" : order.confirm_date,
			"pay_type" : order.get_pay_type_display()
		}
		return render(request, 'store/deliver.html')