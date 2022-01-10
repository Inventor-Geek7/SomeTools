import os
import Tools.IUtils as IUtils
from Tools.IPlatform import Debug
from Tools.consoleColorFont import printGreen
import webbrowser

#版本
dirnames = ["1.x","2.0_2.1","2.2+"]
#lib文件
libfiles = ["fairygui.js","rawinflate.min.js"]
#声明文件
dfiles = ["fairygui.d.ts"]

def depend( proj_path,ver=2 ):

    #检测项目路径
    if not IUtils.hasPath(f"{proj_path}/laya") or not IUtils.hasPath(f"{proj_path}/libs"):
        printGreen("不是一个laya项目根目录")
        Debug.Log("不是一个laya项目根目录")
        return

    #获取项目位置 和 FGUI版本
    Debug.Log("正在将FGUI库植入Laya项目中...")
    if ver < 0 or ver > len(dirnames):
        Debug.Log(f"Error: lib version number is out of range, please check the version number :{ver}")
        return
    lib_path = dirnames[ver]
    Debug.Log(f"fgui version: {lib_path}")

    #目标库文件目录
    destDir = f"{proj_path}/bin/libs"
    Debug.Log(f"目标库文件目录: {destDir}")
    if not os.path.exists(destDir):
        os.makedirs(destDir)

    #导入fgui库
    Debug.Log("正在导入fgui库...")
    rootDir = os.getcwd()
    for file in libfiles:
        fullpath = f"{destDir}/{file}"
        if not os.path.exists(fullpath):
            Debug.Log(f"正在导入{file}...")
            IUtils.CopyFile(f"{rootDir}/FGUI/{lib_path}/{file}",fullpath)

    #导入声明文件
    Debug.Log("正在导入fgui声明文件...")
    destDir = f"{proj_path}/libs"
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    for file in dfiles:
        fullpath = f"{destDir}/{file}"
        if not os.path.exists(fullpath):
            Debug.Log(f"正在导入{file}...")
            IUtils.CopyFile(f"{rootDir}/FGUI/{lib_path}/{file}",fullpath)

    #更新项目配置文件
    #2.x
    Debug.Log("laya工程添加引用fgui...")
    jspath = f"{proj_path}/bin/index.js"
    indexJsContent = IUtils.fromFile(jspath)
    if indexJsContent.find("fgui") == -1:
        Debug.Log("正在添加fgui引用...")
        importContent = """//-----libs-end-------
loadLib("libs/fairygui/rawinflate.min.js");
loadLib("libs/fairygui/fairygui.js");
"""
        indexJsContent = indexJsContent.replace("//-----libs-end-------",importContent)
        Debug.Log("正在更新index.js...")
        IUtils.writeInFile(jspath,indexJsContent)
        webbrowser.open(f"{os.getcwd()}/FGUI/index.html", new=0, autoraise=True) 
        

    elif indexJsContent.find('loadLib("libs/fairygui/fairygui.js");') == -1:
        Debug.Log(f"存在不正确的fgui引用或工具检测有误，请人工检查 {jspath}文件...")
        IUtils.openExplorer(f"{proj_path}/bin")
    else:
        Debug.Log("fgui引用已存在...")