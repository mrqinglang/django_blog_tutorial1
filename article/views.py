from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ArticlePost
from .models import ArticleColumn
from comment.models import Comment
from comment.forms import CommentForm
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import markdown


# Create your views here.
def article_list(request):
    # 取出所有博客文章# 修改变量名称（articles -> article_list）
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    article_list = ArticlePost.objects.all()
    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }

    return render(request, 'article/list.html', context)

# 文章详情

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # update_fields=[]指定了数据库只更新total_views字段，优化执行效率。
    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ])
    article.body = md.convert(article.body)
    # 新增了md.toc对象
    # 引入评论表单
    comment_form = CommentForm()
    context = {
        'article': article,
        'toc': md.toc,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'article/detail.html', context)

# 写文章的视图
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()
            # 完成后返回到文章列表
            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            return redirect("article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        # 新增及修改的代码
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'article/create.html', context)

def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect(article_list)

def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect('article_list')
    else:
        return HttpResponse('仅允许Post请求')

@login_required(login_url='/userprofile/login/')
def article_updata(request, id):
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    if request.method == 'POST':
        article_post_from = ArticlePostForm(data=request.POST)
        if article_post_from.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            # 新增的代码
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            return redirect("article_detail", id=id)
        else:
            return HttpResponse("表单传输有误")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
            'tags': ','.join([x for x in article.tags.names()])
        }
        return render(request, 'article/update.html', context)


