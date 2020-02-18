from bs4 import BeautifulSoup as soup
import requests
import csv
import pandas as pd
from datetime import date


def func_html_parser(parse_url):
    url_request = requests.get(parse_url)
    page_soup = soup(url_request.content, 'html5lib')
    return page_soup

#def func_write_to_csv():
#    'hi'

def main():
    today = date.today()
    file = today.strftime("%d%b%Y")
    output_file = file +'_today_uci.csv'        
    data_to_file = open(output_file, 'w', newline='')
    csv_writer = csv.writer(data_to_file, delimiter=",")
    csv_writer.writerow(["Home Url","Event Name", "Event Url", "Description", "Event Date", "Event Timing", "Event Type", "Event Type Url",
                         "Website", "Aduience", "Department", "Department Url", "Hash Tag", "Hash Tag Url", "Event Sponser's",
                        "Event Contact Email", "Event Contact Phone No.", "Event Address", "Event Address Url"])

    event_date = today.strftime("%Y/%m/%d")

    url = 'https://today.uci.edu/calendar/day/'
    main_url = url + event_date
    page_soup_content = func_html_parser(main_url)

    try:
        event_list = page_soup_content.findAll('div', attrs={'class': 'item_content_medium'})

        for item in event_list:
            event_url = item.find('a')['href']

            event_page_soup_content = func_html_parser(event_url)

            try:
                info = event_page_soup_content.find('div', attrs={'class': 'box_content vevent grid_8'})
                title = info.find('h1').text.strip()
                description = info.find('div', attrs={'class': 'description'}).text.strip()
                try:
                    s_timing = info.find('abbr', attrs={'class': 'dtstart'}).text.strip().split()[-1]
                    e_time = info.find('abbr', attrs={'class': 'dtend'}).text.strip()
                    event_timing = s_timing + ' - ' + e_time
                except Exception:
                    event_timing = 'N/A'
                    pass

                details = event_page_soup_content.find('div', attrs={'class': 'extra_details clearfix'})
                try:
                    event_type = details.find('dd', attrs={'class': 'filter-event_types'}).text.strip()
                    event_type_url = details.find('dd', attrs={'class': 'filter-event_types'}).find('a')['href']
                except Exception:
                    event_type = 'N/A'
                    event_type_url = 'N/A'
                    pass
                try:
                    Aduience = details.find('dd', attrs={'class': 'filter-event_audience'}).text.strip()
                except Exception:
                    Aduience = 'N/A'
                    pass
                website = details.find('dd', attrs={'class': 'event-website'}).find('a')['href']
                try:
                    Department = details.find('dd', attrs={'class': 'event-group'}).find('a').text.strip()
                    Department_url = details.find('dd', attrs={'class': 'event-group'}).find('a')['href']
                except Exception:
                    Department = 'N/A'
                    Department_url = 'N/A'
                    pass

                try:
                    HashTag = details.find('dd', attrs={'class': 'event-hashtag'}).find('a').text.strip()
                    HashTag_url = details.find('dd', attrs={'class': 'event-hashtag'}).find('a')['href']
                except Exception:
                    HashTag = 'N/A'
                    HashTag_url = 'N/A'
                    pass

                try:
                    event_sponser = details.find('dd', attrs={'class': 'custom-field-event_sponsor'}).find('p').text.strip()
                except Exception:
                    event_sponser = 'N/A'
                    pass

                try:
                    event_contact_email = details.find('dd', attrs={'class': 'custom-field-event_contact_email'}).find('a').text.strip()
                except Exception:
                    event_contact_email = 'N/A'
                    pass

                try:
                    event_contact_phone = details.find('dd', attrs={'class': 'custom-field-event_contact_phone'}).find('p').text.strip()
                except Exception:
                    event_contact_phone = 'N/A'
                    pass

                try:
                    addr = info.find('p', attrs={'class': 'location'})
                    addr1 = addr.find('a').text.strip()
                    addr2 = addr.find('span').text.strip()
                    address = addr1 + ', ' + addr2
                    try:
                        address_url = addr.find('a')['href']
                    except Exception:
                        address_url = 'N/A'
                        pass
                except Exception:
                    address = 'N/A'
                    pass

                csv_writer.writerow([url , title, event_url, description, event_date, event_timing, event_type, event_type_url,
                                     website, Aduience, Department, Department_url, HashTag, HashTag_url, event_sponser,
                                     event_contact_email, event_contact_phone, address, address_url])
                
                print('Event Name :  '+title)

               # Addmission_opening_timing = ''

               # func_write_to_csv({'title': title, })


            except Exception:
                pass
    except Exception:
        pass

if __name__ == '__main__':
    main()
