from bs4 import BeautifulSoup
import os
import re

#'/home/ubuntu/workspace/2017_08'
def parse_month(path):
    for f in [f for f in os.listdir(path) if len(f) > 17]: #ignore index file
        parse_message_content(os.path.join(path, f))

#'/home/ubuntu/workspace/2017_08/2017_Aug_0.raw.html'
def parse_message_content(filename):
    with open(filename, 'r') as f:
        raw = f.read()

    # Message body is contained between two comments; use basic indexing
    # <!--X-Body-of-Message-->
    # <!--X-Body-of-Message-End-->
    start = raw.index('<!--X-Body-of-Message-->') + 24
    end = raw.index('<!--X-Body-of-Message-End-->')
    body = raw[start:end]
    soup = BeautifulSoup(body)
    
    # default parser adds html basic tags, so search inside <body>
    text = soup.find('body').text
    
    fileout = filename.replace('.raw.html', '.content.txt')
    
    with open(fileout, 'w') as w:
        w.write(text)