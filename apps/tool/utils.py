# -*- coding: utf-8 -*-
IMAGE_LIST = [
    'busybox', 'centos', 'docker', 'fedora', 'golang', 'httpd', 'java',
    'jenkins/jenkins', 'jenkinsci/blueocean', 'memcached', 'mongo', 'mysql',
    'nginx', 'node', 'php', 'postgres', 'python', 'rabbitmq', 'redis',
    'registry', 'ruby', 'tomcat', 'ubuntu', 'wordpress'
]

QTECHCODE_TOOLS = {
    'office': {
        'tag':
        '办公工具',
        'tools': [{
            'name': 'Markdown编辑器',
            'url': 'tool:markdown_editor',
            'img': 'editor/images/logos/editormd-logo-96x96.png',
            'desc': '基于开源项目 Editor.md 的在线 markdown 编辑器，拥有强大的编辑能力和全面的语法支持'
        }, {
            'name': '词云图',
            'url': 'tool:word_cloud',
            'img': 'blog/img/word-cloud.png',
            'desc': '支持中英文分词并统计词频生成词云图的工具，支持全屏预览和导出成图片及其他格式'
        }, {
            'name': '二维码',
            'url': 'tool:qr_code',
            'img': 'blog/img/qrcode.png',
            'desc': '支持添加logo和背景图片的二维码生成工具，支持导出成图片及其他格式'
        }, {
            'name': '水印',
            'url': 'tool:watermarker',
            'img': 'blog/img/watermarker.png',
            'desc': '图片在线添加全图半透明水印工具，支持jpg和png图片格式'
        }]
    },
    'develop': {
        'tag':
        '开发工具',
        'tools': [{
            'name': 'Docker镜像查询',
            'url': 'tool:docker_search',
            'img': 'blog/img/docker.png',
            'desc': '查询官方镜像仓库中指定镜像的版本信息，帮助开发人员更准确的选择合适的镜像'
        }, {
            'name': 'User-Agent生成器',
            'url': 'tool:useragent',
            'img': 'blog/img/chrome.png',
            'desc': '网页请求头在线生成器，自动生成各种平台和浏览器的请求头User-Agent'
        }, {
            'name': 'HTML特殊字符',
            'url': 'tool:html_characters',
            'img': 'blog/img/html.png',
            'desc': 'HTML常用字符查询表，HTML特殊字符对照表'
        }, {
            'name': '在线正则表达式',
            'url': 'tool:regex',
            'img': 'blog/img/regex.png',
            'desc': '正则表达式在线工具，使用正则表达式的规则提取信息，所有语言规则通用'
        }]
    },
    'web': {
        'tag':
        '站长工具',
        'tools': [{
            'name': '百度主动推送',
            'url': 'tool:baidu_push',
            'img': 'blog/img/baidu-2.png',
            'desc': '调用百度站长提供的主动推送接口批量提交链接，提升网站收录效率，老站必备'
        }, {
            'name': 'Sitemap主动推送',
            'url': 'tool:baidu_push_site',
            'img': 'blog/img/map.png',
            'desc': '抓取Sitemap页面所有链接，调用百度主动推送接口，主动批量提交网站链接，新站必备'
        }]
    },
}

if __name__ == '__main__':
    print(sorted(IMAGE_LIST))
