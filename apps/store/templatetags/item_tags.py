from django import template


register = template.Library()

@register.inclusion_tag('store/tags/item_list.html')
def load_item_summary(items):
    '''返回文章列表模板'''
    return {'items': items}

@register.inclusion_tag('blog/tags/pagecut.html', takes_context=True)
def load_pages(context):
    '''分页标签模板，不需要传递参数，直接继承参数'''
    return context

@register.simple_tag
def keywords_to_str(item):
    '''将文章关键词变成字符串'''
    keys = item.keywords.all()
    return ','.join([key.name for key in keys])

@register.filter
def div( value, arg ):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = int( value )
        arg = int( arg )
        if arg: return value / arg
    except: pass
    return ''