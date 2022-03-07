import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from faker import Faker
from random import randint as r

from links.models import Category, Link

class Command(BaseCommand):
    help = 'Creates a new fake user with fake data'

    def handle(self, *args, **options):
        f = Faker()

        # create user
        first    = 'Fake ' + f.first_name()
        last     = f.last_name()
        email    = f.email()
        password = f.password()
        user = None
        for i in range(1, 100):
            username = f'fakeuser{i:02d}'
            if len(User.objects.filter(username=username)) == 0:
                user = User.objects.create_user(username, email=email, password=password, first_name=first, last_name=last)
                break
        if user is None:
            raise RuntimeError("Too many fake users already exist!")

        # create data
        (cmin, cmax)   = (10, 12)       # number of categories
        (lmin, lmax)   = ( 2, 20)       # number of links per category
        (cnmin, cnmax) = ( 1,  7)       # number of words in a category name
        (lnmin, lnmax) = ( 0, 20)       # number of words in a link note
        (cn, ln)       = ( 0,  0)       # cat/link counters
        for i in range(r(cmin, cmax)):
            cname = ' '.join(f.words(r(cnmin, cnmax)))
            cat = Category(name=cname, user=user)
            cat.save()
            cn += 1

            for j in range(r(lmin, lmax)):
                url = fakeUrl(f)
                note = ' '.join(f.words(r(lnmin, lnmax)))
                date = timezone.make_aware(f.date_time_between(timezone.now() - datetime.timedelta(days=365*5), timezone.now()))
                link = Link(url=url, note=note, category=cat, user=user, created=date, updated=date)
                link.save()
                ln += 1

        # output
        self.stdout.write(self.style.SUCCESS(f"Successfully created fake user with {cn} categories and {ln} links:"))
        self.stdout.write("  username: {}".format(self.style.SUCCESS(username)))
        self.stdout.write("  password: {}".format(self.style.SUCCESS(password)))


# ---- utility ---------------------------------------------------------------------------------------

def fakeUrl(f, pnmin=2, pnmax=10):
    url = f.uri()
    # 50/50 chance of adding params
    if r(0, 1):
        url += '?'
        params = []
        for p in range(r(pnmin, pnmax)):
            params.append(f.word() + '=' + fakeParam(f))
        url += '&'.join(params)
    return url

def fakeParam(f):
    match r(1, 7):
        case 1: # word
            return f.word()
        case 2: # binary
            return str(r(0, 1))
        case 3: # small number
            return str(r(0, 100))
        case 4: # big number
            return str(r(0, 1e7))
        case 5: # md5
            return str(f.md5())
        case 6: # sha1
            return str(f.sha1())
        case 7: # bool
            return str(f.boolean())
