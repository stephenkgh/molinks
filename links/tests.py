from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from .models import Category, Link


class CategoryModelTests(TestCase):

    def test_restrict_by_user(self):
        """
        Category Model should only return entries that are owned by the logged in user
        """

        (az, bub) = build_users()
        (ac1, ac2, bc1, bc2) = build_categories(az, bub)

        acats = Category.objects.all(az).order_by('name')
        bcats = Category.objects.all(bub).order_by('name')

        self.assertQuerysetEqual(acats, [ac1, ac2])
        self.assertQuerysetEqual(bcats, [bc2, bc1])

    def test_require_user(self):
        """
        Category Model should only create entries if a user is given
        """

        ac1 = Category(name='Death')
        self.assertRaisesMessage(IntegrityError, "null value", ac1.save)


class LinkModelTests(TestCase):

    def test_restrict_by_user(self):
        """
        Link Model should only return entries that are owned by the logged in user
        """

        (az, bub) = build_users()
        (ac1, ac2, bc1, bc2) = build_categories(az, bub)

        # build links
        al1 = Link(url='https://void.null/death/blog', note='my scrapbooking site', category=ac1, user=az)  ; al1.save()
        al2 = Link(url='https://facebook.com', note='next on my list',              category=ac1, user=az)  ; al2.save()
        al3 = Link(url='https://kittenwar.com', note='not sure where to put this',  category=ac2, user=az)  ; al3.save()
        bl1 = Link(url='https://hell.com', note='home sweet home',                  category=bc1, user=bub) ; bl1.save()
        bl2 = Link(url='https://irs.gov', note='',                                  category=bc2, user=bub) ; bl2.save()

        alinks = Link.objects.all(az).order_by('created')
        blinks = Link.objects.all(bub).order_by('created')

        self.assertQuerysetEqual(alinks, [al1, al2, al3])
        self.assertQuerysetEqual(blinks, [bl1, bl2])

    def test_link_ordering(self):
        """
        Link Model default ordering is by category, then reverse date modified
        """

        (az, bub) = build_users()
        (ac1, ac2, _, _) = build_categories(az, bub)

        # build links
        al1 = Link(url='https://void.null/death/blog', note='my scrapbooking site', category=ac1, user=az)  ; al1.save()
        al2 = Link(url='https://facebook.com', note='next on my list',              category=ac1, user=az)  ; al2.save()
        al3 = Link(url='https://kittenwar.com', note='not sure where to put this',  category=ac2, user=az)  ; al3.save()
        al4 = Link(url='https://reddit.com/u/death', note='my reddit user',         category=ac1, user=az)  ; al4.save()

        # use default ordering
        alinks = Link.objects.all(az)

        self.assertQuerysetEqual(alinks, [al4, al2, al1, al3])

    def test_require_user(self):
        """
        Link Model should only create entries if a user is given
        """

        from django.db.utils import IntegrityError

        (az, bub) = build_users()
        ac1 = Category(name='Death', user=az)   ; ac1.save()
        al1 = Link(url='https://void.null/death/blog', note='my scrapbooking site', category=ac1)
        self.assertRaisesMessage(IntegrityError, "null value", al1.save)

    def test_link_category_users_must_match(self):
        """
        Link object cannot be created with a Category from a different user
        """
        (az, bub) = build_users()
        ac1 = Category(name='Death', user=az)   ; ac1.save()
        bl1 = Link(url='https://void.null/death/blog', note='my scrapbooking site', category=ac1, user=bub)
        #bl1.save()
        self.assertRaisesMessage(IntegrityError, "user", bl1.save)
        """

        print('az categories:\n', Category.objects.all(az))
        print('az links:\n', Link.objects.all(az))
        print('bub categories:\n', Category.objects.all(bub))
        print('bub links:\n', Link.objects.all(bub))

        print('link user:', bl1.user)
        print('cat user:', bl1.category.user)

        assert False, "HERE"
        """


# ---- utility ---------------------------------------------------------------------------------------

def build_users():
    az = User.objects.create_user('azrael', 'az@void.null', '********')
    bub = User.objects.create_user('beelzebub', 'bub@hell.com', '********')
    return (az, bub)
    
def build_categories(a, b):
    ac1 = Category(name='Death',            user=a)  ; ac1.save()
    ac2 = Category(name='Taxes',            user=a)  ; ac2.save()
    bc1 = Category(name='zHellish things',  user=b)  ; bc1.save()
    bc2 = Category(name='Taxes',            user=b)  ; bc2.save()
    return (ac1, ac2, bc1, bc2)
