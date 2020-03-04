import requests
import csv

from bs4 import BeautifulSoup

url = 'https://first-avenue.com'
calendar_page = url + '/calendar'
page = requests.get(calendar_page)


if page.status_code != 200:
    print('this shit fuct')
    exit()

soup = BeautifulSoup(page.text, 'html.parser')
calendar = soup.body.div.contents[7].contents[3].contents[3]
view_content_tag = calendar.contents[3]
current_date = ''

with open('first_ave_march.csv', mode='w') as csv_file:
    fieldnames = ['event_date', 'event_time', 'event_name', 'event_url', 'event_img_thumbnail_link', 'performer_url',
                  'special_guest_names', 'event_price', 'door_price', 'event_status', 'ticket_url',
                  'venue_name', 'venue_url', 'event_age']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for child in view_content_tag.children:
        if child.name == 'h3':
            event_date = child.div.span.text
        if child.name == 'div':
            support_name = ''
            event_price = ''
            event_door_price = ''
            buy_ticket_url = ''
            venue_name = ''
            venue_url = ''
            event_time = ''
            event_age = ''

            article_tag = child.article
            event_name = article_tag.header.h2.a.text
            event_url = url + article_tag.header.h2.a['href']
            event_img_thumbnail_url = article_tag.div.div.div.a.img['src']
            event_details_tag = article_tag.contents[4]

            artist_tag_list = article_tag.find_all('div', class_='field-name-field-event-performer')
            artist_url = url + artist_tag_list[0].div.div.a['href']

            support_tag_list = article_tag.find_all('div', class_='field-name-field-event-special-guests')
            if len(support_tag_list) != 0:
                support_name = support_tag_list[0].div.div.text

            event_price_tag_list = article_tag.find_all('div', class_='field-name-field-event-price')
            if len(event_price_tag_list) != 0:
                event_price = event_price_tag_list[0].div.div.span.text

            event_door_price_tag_list = article_tag.find_all('div', class_='field-name-field-event-door-price')
            if len(event_door_price_tag_list) != 0:
                event_door_price = event_door_price_tag_list[0].div.div.span.text

            event_status_tag_list = article_tag.find_all('div', class_='field-name-field-event-status')
            if len(event_status_tag_list) != 0:
                if event_status_tag_list[0].div.div != None:
                    event_status = event_status_tag_list[0].div.div.a.text
                    if event_status == 'Buy Tickets':
                        buy_ticket_url = event_status_tag_list[0].div.div.a['href']

            event_venue_tag_list = article_tag.find_all('div', class_='group_calendar_room_age')
            if len(event_venue_tag_list) != 0:
                venue_name = event_venue_tag_list[0].div.div.div.a.text
                venue_url = url + event_venue_tag_list[0].div.div.div.a['href']

            event_time_tag_list = article_tag.find_all('div', class_='field-name-field-event-date')
            event_time = event_time_tag_list[0].div.div.div.span.text

            event_age_tag_list = article_tag.find_all('div', class_='field-name-field-event-age')
            event_age = event_age_tag_list[0].div.div.text

            event_details = {
                'event_date': event_date.encode("utf-8"),
                'event_time': event_time.encode("utf-8"),
                'event_name': event_name.encode("utf-8"),
                'event_url': event_url.encode("utf-8"),
                'event_img_thumbnail_link': event_img_thumbnail_url.encode("utf-8"),
                'performer_url': artist_url.encode("utf-8"),
                'special_guest_names': support_name.encode("utf-8"),
                'event_price': event_price.encode("utf-8"),
                'door_price': event_door_price.encode("utf-8"),
                'event_status': event_status.encode("utf-8"),
                'ticket_url': buy_ticket_url.encode("utf-8"),
                'venue_name': venue_name.encode("utf-8"),
                'venue_url': venue_url.encode("utf-8"),
                'event_age': event_age.encode("utf-8"),
                }

            print(event_details)

            writer.writerow(event_details)

