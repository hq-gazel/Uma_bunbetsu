#TODO 処理別にファイルを分ける
#TODO 星付き対処
#TODO 予め決められた場所をトリミングして検査
#TODO スクショ同じやつが2枚連続の場合


import cfgset

import os, shutil, glob, copy, subprocess
import cv2, pyocr, pyocr.builders
from PIL import Image
from time import sleep

import gspread
from oauth2client.service_account import ServiceAccountCredentials

cfgset.bunbetsu()
path_tesseract = cfgset.path_tesseract
filerng_low = cfgset.filerng_low
filerng_high = cfgset.filerng_high
graphic_comp_p = cfgset.graphic_comp_p
sheetname  = cfgset.sheetname


#VSCodeがうるさいから
akaID, SSRCounts, umaName, worksheet, rc = 0, 0, 0 ,0, 0
umaDict, uma_copy, umaDictBackup = {}, {}, {}
filesList = []


#ウマ娘リスト取得
def getter():
    global umaDictBackup, umaDict

    test1 = worksheet.row_values(1)
    test2 = worksheet.row_values(2)
    umaDict_get_umaName = copy.deepcopy(test1)
    umaDict_get_fileName = copy.deepcopy(test2)

    for i in test1:
        if i == '番号' or i == 'トレーナーID' or i ==  '開始時間' or i == '終了時間' or i ==  '作業者' or i ==  '進捗状況' or i == '所持ジュエル' or i ==  '合計':
            umaDict_get_umaName.remove(i)
        else:
            break

    for x in test2:
        if not x:
            umaDict_get_fileName.remove(x)
        else:
            break

    if len(umaDict_get_umaName) != len(umaDict_get_fileName):
        input('Google Sheetsを確認してください\nウマ娘名数とファイル名数が一致しません\nキーを入力して終了します')
        exit()

    for z in range(len(umaDict_get_umaName)):
        umaDictBackup.update({umaDict_get_fileName[z]:[umaDict_get_umaName[z],0]})

    umaDict = copy.deepcopy(umaDictBackup) #umaDictは実際に処理を使います



#GSheets書き出し
def GSheetCreate():
    Ext_List = []

    for y, z in enumerate(umaDict):
        Ext_List.append(umaDict[z][1])

    #ウマ娘シート修正
    last_col = worksheet.col_values(2)
    worksheet.update('B' + str(len(last_col)+1) + ':B' + str(len(last_col)+1), akaID)
    worksheet.update('I' + str(len(last_col)+1) + ':AO' + str(len(last_col)+1), [Ext_List])



#OCR機能
def convertOCR(OCRtarg):
    global akaID, akaID2

    testIMG = cv2.imread(OCRtarg ,1)
    temp_png = (motoDIR + '\\temp\\temp.png')

    x,y = 220,350
    w,h = 105,25
    bubun = testIMG[y:y+h, x:x+w]

    cv2.imwrite(temp_png, bubun)

    if path_tesseract not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + path_tesseract

    tools = pyocr.get_available_tools()
    tool = tools[0]

    img_org = Image.open(temp_png)
    img_rgb = img_org.convert('RGB')

    #OCR実行
    builder = pyocr.builders.TextBuilder()
    akaID = tool.image_to_string(img_rgb, lang='jpn', builder=builder)

    if akaID == type(str): #間違ったスクショをたまたまOCR出来てしまった時、空にする]
        akaID = None
    else: #スペース削除
        akaID = str(akaID.replace(' ', ''))



#画像比較
def SSRchk(imgname, distpath):
    global SSRCounts, umaDict

    detector = cv2.AKAZE.create()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    targ_img = cv2.imread(imgname, cv2.COLOR_RGB2BGR)
    kp1, targ_des = detector.detectAndCompute(targ_img, None)

    for fl in faceList:
        try:
            for i in range(filerng_high + 1): #最大10匹検出用にrangeは11
                comp_img = cv2.imread(faceDIR + fl, cv2.COLOR_RGB2BGR)
                kp2, comp_des = detector.detectAndCompute(comp_img, None)

                w, h = comp_img.shape[1],comp_img.shape[0]
                matches = bf.match(targ_des, comp_des)

                dist = [m.distance for m in matches]
                ret = sum(dist) / len(dist)

                #print(imgname + 'は、' + fl + 'との誤差:' + str(ret))

                if ret <= graphic_comp_p:
                    umaName = os.path.splitext(os.path.basename(fl))[0]
                    umaDict[umaName][1] += 1
                    SSRCounts += 1
                    print(umaDict[umaName][0] + 'を1枚検出')

                    #マスクの作成
                    resIMG = cv2.matchTemplate(targ_img, comp_img, cv2.TM_CCOEFF_NORMED)

                    #黒く塗りつぶす
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resIMG)
                    top_left = max_loc
                    bottom_right = (top_left[0] + w, top_left[1] + h)
                    cv2.rectangle(targ_img, top_left, bottom_right, (0,0,0), thickness=-1)
                    cv2.imwrite(motoDIR + '\\temp\\res.png', targ_img)

                    #次のループの為に情報書き換え
                    targ_img = cv2.imread(motoDIR + '\\temp\\res.png', cv2.COLOR_RGB2BGR)
                    kp1, targ_des = detector.detectAndCompute(targ_img, None)
                    continue

                else:
                    break


        except cv2.error:
            input('OpenCV2 Errorが発生したので画像とプログラムを確認してください\n.Errorフォルダに移動しました\n\n強制終了します')
            f_stage(distpath)
            convert7z(akaID, motoDIR + '\\gatya\\.Error\\')
            exit()



#画像変換
def convertIMG():
    convertIMG_files = glob.glob('*.png', recursive=True) + glob.glob('*.bmp', recursive=True)

    if convertIMG_files:
        for ci in convertIMG_files:
            img = Image.open(ci).convert('RGB') # RGBA(png)→RGB(jpg)へ変換
            img.save(os.path.splitext(os.path.basename(ci))[0] + '.jpg', quality=100) #品質設定
            os.remove(ci)



#7zip圧縮
def convert7z(ZIPtarg, toZIP):
    #フォルダ設定
    exe_7z = py_DIR + '\\.src\\7z\\7za.exe'
    dst_file = (toZIP + ZIPtarg + '.7z') #圧縮後のファイル名
    src_dir = f'{ZIPtarg}\\*'  # 最上位フォルダ無し

    # コマンドラインの引数リストを作る
    args = ( exe_7z, 'a', dst_file, src_dir, 
                '-mx=9', # 0,1,3,5,7,9 数字が高いほど圧縮率が高い
                '-mmt=on', # マルチスレッディング on,off,整数,{N}が使える
)

    # 圧縮を実行
    cp = subprocess.run(args, stdout=subprocess.DEVNULL)

    # デバッグ出力
    if cp.returncode != 0:
        print(f'7zip Error:{ZIPtarg} + {cp.returncode}')

    shutil.rmtree(motoDIR + '\\.working\\' + ZIPtarg)




#多重配列内の空要素削除, 集計結果表示
def dict_edit():
    global umaDict, uma_copy
    uma_copy = copy.deepcopy(umaDict) #分解用にバックアップ、この処理終わったらumaDictは用済み

    print('\n\n----------合計結果----------')
    for i, x in enumerate(uma_copy):
        if uma_copy[x][1] == 0:
            umaDict.pop(x)

        else:
            print(umaDict[x][0] + 'は合計: ' + str(umaDict[x][1]) + '枚')
    print('\nSSR総数: ' + str(SSRCounts) + '枚')



#何回も同じ事書いてあったからまとめた
def f_stage(f_stage_dir):
    convertIMG()
    os.chdir(motoDIR + '\\.working\\')
    if akaID:
        os.rename(f_stage_dir, akaID)



#####メイン部分#####
if __name__ == '__main__':
    os.chdir('..\\')
    motoDIR = os.getcwd()
    py_DIR = os.path.dirname(__file__)
    faceDIR = (py_DIR +  '\\.src\\face\\')

    os.makedirs('temp\\', exist_ok=True)
    os.makedirs('.working\\', exist_ok=True)


    os.chdir(faceDIR)
    faceList = glob.glob('*.png', recursive=True)

    os.chdir(motoDIR + '\\.working\\')

    SHORImaeDIR_1 = os.listdir('.\\')
    SHORImaeDIR_2 = [f for f in SHORImaeDIR_1 if os.path.isdir(os.path.join('.\\', f))]
    #フォルダじゃない奴を除去


    #Google Sheets アクセス権限取得
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    # Google Sheets JSONを渡す
    c = ServiceAccountCredentials.from_json_keyfile_name(py_DIR + '', SCOPES)
    gs = gspread.authorize(c)
    SPREADSHEET_KEY = ''
    worksheet = gs.open_by_key(SPREADSHEET_KEY).worksheet(sheetname)


    getter()
    #辞書とGSheetアクセス権限をセットします


    if not SHORImaeDIR_2:
        input('処理するフォルダが存在しないので強制終了します\n\n./.working/に処理するフォルダを追加してください\n')
        subprocess.run('PAUSE', shell=True)
        shutil.rmtree(motoDIR + '\\temp\\')
        exit()

    #フォルダ数分、フォルダリストを作成してSSR枚数を確認
    for i in SHORImaeDIR_2:
        os.chdir(motoDIR + '\\.working\\' + i)

        #初期化
        filesList.clear()
        uma_copy.clear()
        umaDict.clear()
        umaDict = copy.deepcopy(umaDictBackup)
        SSRCounts, akaID = 0, 0
        filesList = glob.glob('*.png', recursive=True) + glob.glob('*.jpg', recursive=True) + glob.glob('*.jpeg', recursive=True) + glob.glob('*.bmp', recursive=True)

        if not filesList: #もし間違ったフォルダを入れてしまった時の対応
            print(i + 'は画像が存在しないので、.Errorに移動されました')
            os.chdir(motoDIR + '\\.working\\')
            shutil.move(i, motoDIR + '\\gatya\\.Error\\')
            continue

        filesList.sort() #大文字を前に持ってくる為、降順でソート

        for x in filesList:
            if x == filesList[0]:
                convertOCR(x) #最初の1枚だけOCR

                if not akaID: #取得できなかった場合
                    print(i + 'はアカウントIDが読み込めなかったので、.Errorに移動されました')
                    f_stage(i)
                    convert7z(i, motoDIR + '\\gatya\\.Error\\')
                    break

                else: #取得出来た場合、2枚目もアカウントIDないか調べる
                    akaID2 = str(akaID)
                    akaID = None
                    convertOCR(x)

                    if akaID2 != type(int) and not akaID:
                        print(i + 'は2回目のOCRが成功してしまった為、.Errorに移動されました')
                        f_stage(i)
                        convert7z(i, motoDIR + '\\gatya\\.Error\\')
                        break

                    else:
                        #2回目の取得が出来ないがakaIDがある場合
                        akaID = str(akaID2)
                        continue


            elif len(filesList) < filerng_low:
                f_stage(i)
                convert7z(i, motoDIR + '\\gatya\\.Error\\')
                print(akaID + 'は' + str(filerng_low) + '枚未満なので.Errorフォルダに移動されました ')
                continue

            elif len(filesList) > filerng_high:
                f_stage(i)
                convert7z(i, motoDIR + '\\gatya\\.Error\\')
                filerng_high += 1
                print(akaID + 'は' + str(filerng_high) + '枚以上なので.Errorフォルダに移動されました ')
                filerng_high -= 1
                continue


            elif len(filesList) >= filerng_low and len(filesList) <= filerng_high:
                SSRchk(x, i)
                continue




        if SSRCounts == 4:
            for p, w in enumerate(umaDict): #ループを抜けたらリーチを検索
                if umaDict[w][1] == 4:
                    f_stage(i)
                    convert7z(akaID, motoDIR + '\\gatya\\.Reach\\')
                    dict_edit()
                    print(akaID + 'は凸4のカードが存在するので.Reachフォルダに移動されました\n----------------------------\n')
                    break


        elif SSRCounts < 5:
            f_stage(i)
            convert7z(akaID, motoDIR + '\\gatya\\.GOMIBAKO\\')
            dict_edit()
            print(akaID + 'はSSR 5枚未満なので.GOMIBAKOに移動されました\n----------------------------\n')
            continue


        elif SSRCounts >= 5:
            GSheetCreate()
            f_stage(i)
            convert7z(akaID, motoDIR + '\\gatya\\.SSR' + str(SSRCounts) + '\\')
            dict_edit()
            print(akaID + 'はSSR ' + str(SSRCounts) + 'フォルダに移動されました\n----------------------------\n')

            rc += 1
            if rc >= 50: #50回目に3秒間休憩
                sleep(3)
                rc = 0
            continue


    shutil.rmtree(motoDIR + '\\temp\\')
    input('処理が完了しました...キーを入力して終了できます')
