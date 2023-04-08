from base.models import blog
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .Tool.blogTool import get_blog, get_course, get_blog_by_cat
from .Tool.Tools import student_detials


# ...............Blog........................................
@login_required(login_url='/FourNotFout')
def blog_edit(request):
    return render(request, "blog/blog_edit.html", student_detials(request, 'Create Blog'))


def save_blog(request):
    ids = ['#title', '#description', '#content', '#Category', '#Thumbnail']
    title = request.POST.get(ids[0])
    description = request.POST.get(ids[1])
    content = request.POST.get(ids[2])
    Category = request.POST.get(ids[3])
    Thumbnail = request.POST.get(ids[4])
    blog_type = request.POST.get('#type_')

    obj = blog(title=title, blog_type=blog_type, description=description, content=content,
               categories=Category, blog_profile_img=Thumbnail)
    obj.save()
    ob = blog.objects.all()
    for i in ob:
        print(i.blog_profile_img, i.title, i.content)

    return render(request, "blog/blog_edit.html")


def save_edit_blog(request, pk):
    ids = ['#title', '#description', '#content', '#Category', '#Thumbnail']
    title = request.POST.get(ids[0])
    description = request.POST.get(ids[1])
    content = request.POST.get(ids[2])
    Category = request.POST.get(ids[3])
    Thumbnail = request.POST.get(ids[4])

    obj = blog.objects.get(id=pk)
    obj.content = content
    obj.title = title
    obj.description = description
    obj.categories = Category
    obj.blog_profile_img = Thumbnail
    obj.save()

    print("Saved...........")

    return render(request, "blog/blog_edit.html")


def student_list_blog(request):
    items = get_blog()
    return render(request, "blog/studentblog.html", student_detials(request, 'Blog', {'blogs': items}))


def student_list_blog_course(request):
    items = get_course()
    return render(request, "blog/studentblog.html", student_detials(request, 'Blog', {'blogs': items}))


def view_blog(request, pk):
    page = blog.objects.get(id=pk)
    items = get_blog_by_cat(page.categories).remove(page) if page in get_blog_by_cat(
        page.categories) else get_blog_by_cat(page.categories)
    return render(request, "blog/view_blog.html", {'blog': page, 'item': items})


def delete_blog(request):
    bl_id = request.GET.get("id")
    page = blog.objects.get(id=bl_id)
    page.delete()
    return render(request, "blog/view_blog.html", {'blog': page})


@login_required(login_url='/FourNotFout')
def list_edit_blog(request):
    items = get_blog()
    return render(request, "blog/edit_blog_list.html", {'blogs': items})


def edit_blog(request, pk):
    obj = blog.objects.get(id=pk)
    return render(request, "blog/blog_re_edit.html", {'obj': obj})


def teacher_list_blog(request):
    items = get_blog()
    return render(request, "blog/teacherblog.html", {'blogs': items})
