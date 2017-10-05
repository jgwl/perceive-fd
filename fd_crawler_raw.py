import calendar
import os
import pendulum
import random
import re
import requests
import time


def dl_range(year_start, month_start, year_end, month_end):
    """
    Download multiple months, using start & end year/months.
    See dl_month for contents.
    
    Args:
        year_start: int
        month_start: int (Jan = 1)
        year_end: int
        month_end: int (Jan = 1)
    """

    start = pendulum.date(year_start, month_start, 1)
    end = pendulum.date(year_end, month_end, 1)
    period = pendulum.period(start, end)
    for dt in period.range('months'):
        y, m = dt.year, dt.month
        dl_month(y, m)
    
def dl_month(year, month):
    """
    Download entire raw html contents of month.
    Contents will be written to subdir, e.g. ./2017_01
    
    Args: 
        year: int
        month: int (Jan = 1)
    """
    
    year_str = str(year)
    month_0x = str(month).zfill(2)
    month_str = calendar.month_abbr[month]
    
    output_path = './' + year_str + '_' + month_0x
    create_dir(output_path)
    
    index_file = dl_index(year_str, month_str, output_path)
    message_count = parse_index_num(index_file)

    for i in range(message_count):
        dl_message(year_str, month_str, str(i), output_path)
        #use random sleep to prevent banning
        time.sleep(20 * random.random())


def dl_index(year, month, path):
    """
    Download month's index file.
    
    Args:
        year: str, e.g. "2017"
        month: str, e.g., "Jan"
        path: str
    
    Returns:
        str: filename that contents were written into
    
    """
    
    #ex: http://seclists.org/fulldisclosure/2017/Jan/index.html
    url = 'http://seclists.org/fulldisclosure/' + year + '/' + month + '/index.html'
    print(url)
    r = requests.get(url)
    
    #save file, e.g.: 2017_Jan.raw.html
    filename = os.path.join(path, year + '_' + month + '.raw.html')
    with open(filename, 'w') as w:
        w.write(r.text)

    return filename


def parse_index_num(filename):
    """
    Determine how many messages the index file contains. 
    Parses the first line (e.g., <!-- SecLists-Message-Count: 108 -->)
    
    Args: 
        filename: str
    
    Returns:
        int
    
    """
    with open(filename, 'r') as f:
        first_line = f.readline()
    
    rx = re.compile('SecLists-Message-Count: ([\d]+)')
    m = rx.search(first_line)
    return int(m.group(1))


def dl_message(year, month, id, path):
    """
    Download individual message.
    
    Args: 
        year: str, e.g. "2017"
        month: str, e.g., "Jan"
        id: str, e.g., "0"
        path: str
    
    """
    
    #ex: http://seclists.org/fulldisclosure/2017/Jan/0
    url = 'http://seclists.org/fulldisclosure/' + year + '/' + month + '/' + id
    print(url)
    r = requests.get(url)
    
    #save file, ex: 2017_Jan_0.raw.html
    filename = os.path.join(path, year + '_' + month + '_' + id + '.raw.html')
    with open(filename, 'w') as w:
        w.write(r.text)


def create_dir(directory):
    """
    Create dir if not exists.
    """
    
    if not os.path.exists(directory):
        os.makedirs(directory)

