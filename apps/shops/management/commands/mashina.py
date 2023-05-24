from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

import requests
from bs4 import BeautifulSoup

from apps.shops.models import Category, Product, ProductImage, Specification


class Command(BaseCommand):
    help = _('Parse data from external source')
    base_url = 'https://www.mashina.kg/commercialsearch/all/'

    # def add_arguments(self, parser):
    #     parser.add_argument('--date', type=str, help=_('Date in format: YYYY-mm-dd'))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(_('Parsing starting!')))
        self.parse()
        self.stdout.write(self.style.SUCCESS(_('Parsing finished!')))

    def get_html(self, url):
        response = requests.get(url)
        return response.content

    def get_soup(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        return soup

    def parse(self):
        response = self.get_html(f"{self.base_url}")

        soup = self.get_soup(response)
        all_items = soup.find('div', {'class': 'table-view-list'})

        for item in all_items.find_all('div', {'class': 'list-item'}):
            category, _ = Category.objects.get_or_create(name='Коммерческие авто')
            product = Product.objects.create(category=category)

            image = item.find_all('img', {'class': 'lazy-image'})
            for img in image:
                imagine_dragon = ProductImage.objects.create(product=product)

                imagine_dragon.image = img.get('data-src')
                imagine_dragon.save()

            detail_item = item.find('a').get('href')
            detail_response = self.get_html(f'https://www.mashina.kg{detail_item}')
            detail_soup = self.get_soup(detail_response)

            name = detail_soup.find('h1').text.strip().replace('Продажа ', '')
            product.name = name

            price = detail_soup.find('div', {'class': 'price-dollar'}).text.strip().replace('$ ', '')
            product.price = price.replace(' ', '')

            description = detail_soup.find('h2', {'class': 'comment'}).text.strip()
            product.description = description

            specification_key = detail_soup.find_all('div', {'class': 'field-label'})
            specification_value = detail_soup.find_all('div', {'class': 'field-value'})

            for spec_key, spec_value in zip(specification_key, specification_value):
                special = Specification.objects.create(product=product)

                special.name = spec_key.text.strip()
                special.value = spec_value.text.strip().replace(' ', '')
                special.save()

            product.save()
