from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import ArticlePost
import markdown
from django.core.paginator import Paginator
from django.db.models import Q

def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')

    # 搜索逻辑
    if search:
        if order == 'total_views':
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()

    # 每页显示文章数
    paginator = Paginator(article_list,3)
    # 获取URL中的页码
    page = request.GET.get('page')
    # 将相应的页码内容返回给articles
    articles = paginator.get_page(page)

    context = {'articles': articles,'order': order,'search': search}
    return render(request,'article/list.html',context)

def article_detail(request,id):
    article = ArticlePost.objects.get(id=id)
    #markdown语法渲染html样式
    md = markdown.Markdown(
        extensions = [
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    # +浏览量
    article.total_views += 1
    article.save(update_fields=['total_views'])

    context = {'article': article,'toc': md.toc}

    return render(request,'article/detail.html',context)