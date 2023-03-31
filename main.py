from lxml import html
from os.path import basename as base
from os import system as job
from os import listdir as Readl
import requests
import subprocess
url="https://gochiusa.com/af/"
job(f'wget -b -k -E -N -p {url}')
# Wgetでダウンロードしたファイルのパス
filename = 'gochiusa.com/af/index.html'

# ファイルを開く
with open(filename, 'r', encoding='utf-8') as f:
    # lxmlでパースする
    tree = html.fromstring(f.read())

    script_tags = tree.xpath('//script[@src]')
    
    # src属性の値を取得してリストに格納する
    src_list = [i.attrib['src'].replace('core_sys','gochiusa.com/bloom/core_sys') for i in script_tags if 'core_sys' in i.attrib['src']]
for i in src_list:
 if 'gochiusa.com/af/core_sys/other/js' in i:
  if 'gochiusa_af' in i:
   js=open(i,'r').read()
   for i in js.splitlines():
	if 'charaImgName = [' in i:
		charaImgName_L=[i.replace("'","") for i in (i.replace("const charaImgName = [", '').replace('];', '')).split(",")]
	if 'charaImg[i].src = ' in i:
		charaImg_root=(i.replace("	charaImg[i].src = '",'').replace("'+charaImgName[i];",''))
	if "const specialImgDir = '" in i:
		specialImgDir_root=i.replace("const specialImgDir = '", "").replace("';", "")
	if "const specialCharaName = ['" in i:
		specialCharaName_L=[i.replace("'", "") for i in i.replace("const specialCharaName = ['", "").replace("];", "").split(',')]
	if "const specialCharaImgType = ['" in i:
		specialCharaImgType_L=[i.replace("'", "")for i in i.replace("const specialCharaImgType = [", "").replace("]", "").split(",")]
for i in charaImgName_L:
	url=f'https://gochiusa.com/af/{charaImg_root}{i}'
	job(f'wget {url} -o {base(url)}')
for i in specialCharaName_L:
	url=f'https://gochiusa.com/af/{specialImgDir_root}{i}{specialCharaImgType_L[0]}'
	job(f'wget {url} -o {base(url)}')
	url=f'https://gochiusa.com/af/{specialImgDir_root}{i}{specialCharaImgType_L[1]}'
	job(f'wget {url} -o {base(url)}')

for i in Readl('/'):
 if i.endswith('.jpg') or i.endswith(".png"):
    open("README.md","w").write(f"![{i}]({i})")