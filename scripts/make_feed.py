import json,html
from pathlib import Path
d=json.loads(Path('data/news.json').read_text())
host='https://aronpass12-debug.github.io/jewish-music-edit/'
items=''.join('<item><title>'+html.escape(x['title'])+'</title><link>'+html.escape(x['source_url'])+'</link><description>'+html.escape('Source: '+x['source'])+'</description></item>' for x in d[:30])
Path('feed.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>The Jewish Music Edit</title><link>'+host+'</link><description>Source-linked Jewish music news</description>'+items+'</channel></rss>')
