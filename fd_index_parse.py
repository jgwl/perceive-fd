from bs4 import BeautifulSoup
import re

#'/home/ubuntu/workspace/2017_08/2017_Aug.raw.html'
def parse(filename, idroot):
    with open(filename, 'r') as f:
        raw = f.read()

    #body contains unclosed anchor tag; add the closing tag to make parsing easier.
    raw = raw.replace('<a name="begin">', '<a name="begin"></a>')
    soup = BeautifulSoup(raw)
    f.close()
    
    begin = soup.find(attrs={'name':'begin'}) #beginning of msg links
    items = begin.find_next('ul').find_all('li')
    
    messages = []
    read_messages(items, messages, idroot, None)
    print(messages)
    #write_csv(idroot, messages)
    #insert_sqlite3(idroot, messages, db)

def read_messages(items, messages, idroot, parent):
    for li in items:
        msg = li.find('a')
        id = idroot + msg['href']
        title = msg.text
        
        whowhen = li.find('em').text
        rx = re.compile('(.+) \((.+)\)')
        m = rx.search(whowhen)
        who = m.group(1)
        when = m.group(2)

        messages.append({
            'id': id,
            'title': title,
            'parent': parent,
            'author': who,
            'date': when
        })
        
        replies = li.find('ul')
        if replies != None:
            read_messages(replies.find_all('li'), messages, idroot, id)

    return messages

def write_csv(idroot, messages):
    pass

def insert_sqlite3(idroot, messages, db):
    pass