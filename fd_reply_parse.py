from bs4 import BeautifulSoup
import html
import json
import os
import re
from urllib.parse import urlparse

from talon.signature.bruteforce import extract_signature

#'/home/ubuntu/workspace/2017_08'
def parse_month_folder(path):
    """
    Parse .raw.html files 
    """
    
    for f in [f for f in os.listdir(path) if (f.endswith('raw.html') and len(f) > 17)]: #ignore index file
        print(f)
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
    bodyhtml, bodytext = parse_reply_body(raw)
    #talon bruteforce technique to extract signature
    content, sig = extract_signature(bodytext)

    body_filename = filename.replace('.raw.html', '.reply.body.txt')
    with open(body_filename, 'w') as w:
        w.write(bodytext)
    
    title_body_filename = filename.replace('.raw.html', '.reply.title_body.txt')
    with open(title_body_filename, 'w') as w:
        w.write(title)
        w.write(bodytext)

    body_no_sig_filename = filename.replace('.raw.html', '.reply.body_no_signature.txt')
    with open(body_no_sig_filename, 'w') as w:
        w.write(content)
    
    title_body_no_sig_filename = filename.replace('.raw.html', '.reply.title_body_no_signature.txt')
    with open(title_body_no_sig_filename, 'w') as w:
        w.write(title)
        w.write(content)

    #parse tags
    tag_data = parse_reply_tags(bodyhtml)
    
    body_tags_filename = filename.replace('.raw.html', '.reply.body_tags.txt')
    with open(body_tags_filename, 'w') as w:
        w.write(json.dumps(tag_data))


def parse_reply_title(raw):
    """
    Read reply title.

    Args:
        raw: str, body contents of .raw.html file
    """
    
    soup = BeautifulSoup(raw, 'html5lib')
    subject = soup.find('meta', attrs={'name':'Subject'})
    title = subject['content']
    return html.unescape(title)


def parse_reply_body(raw):
    """
    Extract body content from reply, stripping away html tags.
    
    Args:
        raw: str, body contents of .raw.html file
        
    Returns:
        str, str: bodyhtml, body text (no html)
    """
    
    # Message body is contained between two comments; use basic indexing
    # <!--X-Body-of-Message-->
    # <!--X-Body-of-Message-End-->
    start = raw.index('<!--X-Body-of-Message-->') + 24
    end = raw.index('<!--X-Body-of-Message-End-->')
    body = raw[start:end]
    soup = BeautifulSoup(body)
    
    # default parser adds html basic tags, so search inside <body>
    bodyhtml = soup.find('body')
    bodytext = bodyhtml.text
    return bodyhtml, bodytext

def parse_reply_tags(bodyhtml):
    """
    Parse tag types and href domains from body html.
    
    Args:
        bodyhtml: html content of reply
    
    Returns:
        dict, {'tags': {}, 'sites': {} }
    """
    rx = re.compile('<([^\s>]+)(\s|/>)+')
    tags = {}
    for tag in rx.findall(str(bodyhtml)):
        tagtype = tag[0]
        if not tagtype.startswith('/'):
            if tagtype in tags:
                tags[tagtype] = tags[tagtype] + 1
            else:
                tags[tagtype] = 1    

    sites = {}
    atags = bodyhtml.find_all('a')
    hrefs = [link.get('href') for link in atags]
    
    for link in hrefs:
        parsedurl = urlparse(link)
        site = parsedurl.netloc
        if site in sites:
            sites[site] = sites[site] + 1
        else:
            sites[site] = 1
    
    return {'tags': tags, 'sites': sites}
