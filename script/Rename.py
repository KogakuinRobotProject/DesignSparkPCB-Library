
"""
DesignSparkPCBのガーバー出力をFusionPCBに発注できるようにリネームしてくれるスクリプト。
pythonが入っていることが前提なのと
globがインストールされていることが前提です。
$ pip install glob
を実行してインストールしてください。
"""
import glob
import os
from argparse import ArgumentParser as Parser
import zipfile

rename_list={
"*Bottom Copper (Resist).gbr":"{name}.GBS",
"*Bottom Copper.gbr":"{name}.GBL",
"*Bottom Silkscreen.gbr":"{name}.GBO",
"*Drill Data *.drl":"{name}.TXT",
"*Plot 1.gbr":"{name}.GML",
"*Top Copper (Resist).gbr":"{name}.GTS",
"*Top Copper.gbr":"{name}.GTL",
"*Top Silkscreen.gbr":"{name}.GTO",
}

parser = Parser(description='designSparkPCBのガーバーをfusionPCB用にリネームしてくれるスクリプト')
parser.add_argument("wdir",type=str,help='ガーバーが出力されているフォルダを指定')
parser.add_argument("name",type=str,help='ファイルの名前を指定してください。')
args = parser.parse_args()
os.chdir(args.wdir)
print("now direct"+os.getcwd())
for key in rename_list.keys():
    get = glob.glob(key)
    print(get)
    if(len(get) == 0):
        continue
    if(len(get)>1):
        raise RuntimeError("なんで同一のガーバーがあるの？")
    if get is not None:
        os.replace(get[0],rename_list[key].format(name=args.name))



compFile=zipfile.ZipFile(args.name+".zip",'w',zipfile.ZIP_STORED)
try:
    for name in rename_list.values():
        if not os.path.exists(name.format(name=args.name)):
            raise RuntimeError("リネームされたガーバーがない")
        compFile.write(name.format(name=args.name))
except RuntimeError as e:
    pass
finally:
    compFile.close()

for path in glob.glob("*Plot Report?.txt"):#for を使うことでファイル検索代入と条件分岐を同時に行う
    os.remove(path)
