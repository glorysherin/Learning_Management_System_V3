from base.models import blog, Gallery, Draft_blog


def get_blog():
    images = blog.objects.filter(blog_type='Blog')
    cat = []
    temp = []
    items = []
    for i in images:
        cat.append(i.categories)
    for i in list(set(cat)):
        temp = []
        for j in images:
            if i == j.categories:
                temp.append(j)
        items.append(temp)
    for x, i in enumerate(items):
        items[x] = i[::-1]
    return items

def get_draft_blog(request):
    images = Draft_blog.objects.filter(userid=request.user.id,reviewed=False,Submitreview=False)
    cat = []
    temp = []
    items = []
    for i in images:
        cat.append(i.categories)
    for i in list(set(cat)):
        temp = []
        for j in images:
            if i == j.categories:
                temp.append(j)
        items.append(temp)
    for x, i in enumerate(items):
        items[x] = i[::-1]
    return items

def get_draft_blog_unreview(request):
    images = Draft_blog.objects.filter(userid=request.user.id,Submitreview=False)
    cat = []
    temp = []
    items = []
    for i in images:
        cat.append(i.categories)
    for i in list(set(cat)):
        temp = []
        for j in images:
            if i == j.categories:
                temp.append(j)
        items.append(temp)
    for x, i in enumerate(items):
        items[x] = i[::-1]
    return items


def get_blog_by_cat(cat):
    images = blog.objects.filter(categories=cat)
    cat = []
    temp = []
    items = []
    for i in images:
        cat.append(i.categories)
    for i in list(set(cat)):
        temp = []
        for j in images:
            if i == j.categories:
                temp.append(j)
        items.append(temp)
    for x, i in enumerate(items):
        items[x] = i[::-1]
    return items

def get_draft_blog_by_cat(cat,request):
    images = Draft_blog.objects.filter(categories=cat,userid=request.user.id)
    cat = []
    temp = []
    items = []
    for i in images:
        cat.append(i.categories)
    for i in list(set(cat)):
        temp = []
        for j in images:
            if i == j.categories:
                temp.append(j)
        items.append(temp)
    for x, i in enumerate(items):
        items[x] = i[::-1]
    return items

def get_draft_blog_by_cat_to_review(cat,request):
    images = Draft_blog.objects.filter(categories=cat,userid=request.user.id)
    cat = []
    temp = []
    items = []
    for i in images:
        cat.append(i.categories)
    for i in list(set(cat)):
        temp = []
        for j in images:
            if i == j.categories:
                temp.append(j)
        items.append(temp)
    for x, i in enumerate(items):
        items[x] = i[::-1]
    return items


def get_course():
    images = blog.objects.filter(blog_type='Course')
    cat = []
    temp = []
    items = []
    for i in images:
        cat.append(i.categories)
    for i in list(set(cat)):
        temp = []
        for j in images:
            if i == j.categories:
                temp.append(j)
        items.append(temp)
    for x, i in enumerate(items):
        items[x] = i[::-1]
    return items

def get_course_review(request):
    images = Draft_blog.objects.filter(userid=request.user.id,Submitreview=True)
    cat = []
    temp = []
    items = []
    for i in images:
        cat.append(i.categories)
    for i in list(set(cat)):
        temp = []
        for j in images:
            if i == j.categories:
                temp.append(j)
        items.append(temp)
    for x, i in enumerate(items):
        items[x] = i[::-1]
    return items


def get_images():
    images = Gallery.objects.all()
    cat = []
    temp = []
    items = []
    for i in images:
        cat.append(i.categories)
    for i in list(set(cat)):
        temp = []
        for j in images:
            if i == j.categories:
                temp.append(j)
        items.append(temp)
    return [items, images]
















