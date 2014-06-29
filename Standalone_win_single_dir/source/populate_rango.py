import os

def populate():
    python_cat = add_cat('Python', likes=64, views=128)

    add_page(cat=python_cat,
             title="Official Python Tutorial",
             url="http://docs.python.org/2/tutorial/")

    add_page(cat=python_cat,
             title="How to Think like a Computer Scientist",
             url="http://www.greenteapress.com/thinkpython/")

    django_cat = add_cat("Django", likes=32, views=64)

    add_page(cat=django_cat,
        title="Official Django Tutorial",
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(cat=django_cat,
        title="Django Rocks",
        url="http://www.djangorocks.com/")

    add_page(cat=django_cat,
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/")


    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    return p

def add_cat(name, likes=0, views=0):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    return c


if __name__=='__main__':
    print "Starting Rango population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_project.settings')
    from rango.models import Category, Page
    populate()


