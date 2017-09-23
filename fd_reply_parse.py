from bs4 import BeautifulSoup
import html
import os
import re

#'/home/ubuntu/workspace/2017_08'
def parse_month_folder(path):
    for f in [f for f in os.listdir(path) if len(f) > 17]: #ignore index file
        parse_reply(os.path.join(path, f))


def parse_reply(filename):
    """
    Extract body contents from reply, stripping away html tags.
    
    Args:
        filename: str, full path of .raw.html file
    """

    with open(filename, 'r') as f:
        raw = f.read()
    
    title = parse_reply_title(raw)
    body = parse_reply_body(raw)

    body_filename = filename.replace('.raw.html', '.reply.body.txt')
    with open(body_filename, 'w') as w:
        w.write(body)
    
    title_body_filename = filename.replace('.raw.html', '.reply.title_body.txt')
    with open(title_body_filename, 'w') as w:
        w.write(title)
        w.write(body)


def parse_reply_title(contents):
    """
    Read reply title.

    Args:
        contents: str, body contents of .raw.html file
    """
    
    soup = BeautifulSoup(contents)
    subject = soup.find('meta', attrs={'name':'Subject'})
    title = subject['content']
    return html.unescape(title)


def parse_reply_body(contents):
    """
    Extract body contents from reply, stripping away html tags.
    
    Args:
        contents: str, body contents of .raw.html file
        
    Returns:
        str: body contents
    """
    
    # Message body is contained between two comments; use basic indexing
    # <!--X-Body-of-Message-->
    # <!--X-Body-of-Message-End-->
    start = contents.index('<!--X-Body-of-Message-->') + 24
    end = contents.index('<!--X-Body-of-Message-End-->')
    body = contents[start:end]
    soup = BeautifulSoup(body)
    
    # default parser adds html basic tags, so search inside <body>
    text = soup.find('body').text
    return text


