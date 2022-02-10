import json
import re

from django.views import View
from users.models import User
from products.models import Product, ProductOption

from django.http import JsonResponse
