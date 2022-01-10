from time import time
from Tools.IPlatform import Debug
import ver_laya

if __name__ == "__main__":

    try:
        time_start = time()
        #获取项目位置
        projpath = input('Drag the project root directory into the window\n')
        projpath = projpath.replace('\\', '/')
   
        #对指定项目处理
        Debug.Log('Project path: %s' % projpath)    
        ver_laya.depend(projpath,2)

        Debug.Log(f"Done! Time cost: {time() - time_start}s")
    except Exception as e:
        Debug.LogExcept()
    finally:
        #输出日志
        Debug.Export()