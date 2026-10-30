"""Refresh source-linked Jewish music headlines from public RSS feeds. No full articles copied."""
import json,urllib.request,xml.etree.ElementTree as ET,datetime,email.utils,re
from pathlib import Path
feeds=[("Jewish Insights","https://www.thejewishinsights.com/wp/feed/"),("Der Muzikant","https://www.dermuzikant.com/feeds/posts/default?alt=rss")]
p=Path("data/news.json"); old=json.loads(p.read_text()) if p.exists() else []
seen={x.get("source_url") for x in old}; gathered=[]
for name,url in feeds:
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; JewishMusicEdit/1.0; news digest)"})
  raw=urllib.request.urlopen(req,timeout=15).read(2000000)
  root=ET.fromstring(raw)
  entries=root.findall(".//channel/item")
  if not entries: entries=root.findall(".//{http://www.w3.org/2005/Atom}entry")
  for e in entries:
   title=e.findtext("title") or e.findtext("{http://www.w3.org/2005/Atom}title") or ""
   link=e.findtext("link") or ""
   if not link:
    for l in e.findall("{http://www.w3.org/2005/Atom}link"):
     if l.get("rel","alternate")=="alternate":link=l.get("href","");break
   date=e.findtext("pubDate") or e.findtext("{http://www.w3.org/2005/Atom}published") or ""
   try: date=email.utils.parsedate_to_datetime(date).date().isoformat()
   except Exception:
    try:date=date[:10] if re.match(r"^\\d{4}-\\d{2}-\\d{2}",date) else ""
    except Exception:date=""
   title=re.sub(r"<[^>]+>","",title).strip()
   if name=="Der Muzikant" and not any(t in title.lower() for t in ["song","music","single","album","singer","release","video","concert","nigun","shabbos","choir","melody"]):continue
   if link.startswith("https://") and title and link not in seen:
    gathered.append({"title":title[:180],"source_url":link,"source":name,"date":date});seen.add(link)
  print(name,len(entries))
 except Exception as ex: print("Feed unavailable:",name,ex)
items=sorted(old+gathered,key=lambda x:x.get("date",""),reverse=True)[:48]
p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(items,indent=2,ensure_ascii=False)+"\n")
print("News items:",len(items))
