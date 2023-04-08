from base.models import blog, Gallery


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
