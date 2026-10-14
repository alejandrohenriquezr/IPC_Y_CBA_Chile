import unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag in ('script','link','a','iframe'):
   for key in ('src','href'):
    if d.get(key):self.links.append(d[key])
class NavigationTest(unittest.TestCase):
 def test_pages_and_assets(self):
  paths=[ROOT/'site/index.html',*sorted((ROOT/'site/documentacion').glob('*.html'))]
  self.assertEqual(len(paths),6)
  for path in paths:
   p=Links();p.feed(path.read_text(encoding='utf-8'))
   for link in p.links:
    if link.startswith(('http:','https:','mailto:','#','data:')):continue
    self.assertTrue((path.parent/link.split('#')[0]).exists(),f'{path.name}: {link}')
 def test_generator_retains_navigation(self):
  for path in ('site/plantilla.html','site/index.html'):
   s=(ROOT/path).read_text(encoding='utf-8')
   self.assertIn('site-menu-toggle',s)
   self.assertIn('assets/navegacion.css',s)
   self.assertIn('assets/navegacion.js',s)
 def test_docs_not_empty(self):
  for f in (ROOT/'site/documentacion').glob('*.html'):
   self.assertGreater(f.stat().st_size,1000)
