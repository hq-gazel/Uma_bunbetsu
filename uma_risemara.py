#TODO ウマ娘アップデート時の対処
#TODO タップ位置

#from oauth2client.service_account import ServiceAccountCredentials
#import gspread
import datetime, inquirer, cfgset, os
from aapo_kai import AapoManager as am
from time import sleep

cfgset.prechun()
adbpath: str = cfgset.adbpath
sleeptime: int = cfgset.sleeptime
worker: str = cfgset.worker
in_password: str = cfgset.in_password
distpath: str = cfgset.distpath

aapo: str = am.AapoManager(adbpath)

folderName: str = None
stackCount: int = 0

# # Google Sheetsアクセス権限取得
# SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# c = ServiceAccountCredentials.from_json_keyfile_name('.src/prechun-GSheet.json', SCOPES)
# gs = gspread.authorize(c)
# SPREADSHEET_KEY = '1kPY8V_MozF9mgfVrU_9BAMsq3rX-kQ5Pu_dPgVH08x0'
# worksheet = gs.open_by_key(SPREADSHEET_KEY).worksheet('TEST')


# マルチインスタンス選択画面
def multiinstance():
    devicesselect = [inquirer.List("device", message="デバイスを選択して下さい。", choices=aapo.adbl.devices)]
    selected = inquirer.prompt(devicesselect)
    aapo.setdevice(selected['device'])


# アプリ起動
def start():
    aapo.start('jp.co.cygames.umamusume/jp.co.cygames.umamusume_activity.UmamusumeActivity')
    sleep(sleeptime*10)
    return


# アプリ停止
def reset():
    aapo.end('jp.co.cygames.umamusume')
    sleep(sleeptime*5)
    return


motoDIR = os.getcwd()


##メイン部分
def main():
    global stackCount, folderName
    aapo.screencap()

    # 早送りボタンは常にタップ
    if aapo.touchImg(motoDIR + '\\.src\\risemara\\hayaokuri.png', 475, 895):
        sleep(sleeptime)

    # 日付が変わりましたをタップ
    if aapo.touchImg(motoDIR + '.\\.src\\risemara\\hizuke.png', 220, 520):
        sleep(sleeptime)

    # 通信エラーリトライをタップ
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\tuusinera-.png', 320, 520):
        aapo.touchPos(320, 520)
        sleep(sleeptime)

    # Google Playダイアログが出たら、キャンセルの位置をタップ
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\google-play.png', 135, 540):
        aapo.touchPos(135, 540)
        sleep(sleeptime)

    # アカウント連携ダイアログが出たら、後でするの位置をタップ
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\account.png' ,135 ,540):
        aapo.touchPos(135, 540)
        sleep(sleeptime)

    # チュートリアルダイアログが出たら、スキップの位置をタップ
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\tutorial.png' ,320 ,540):
        aapo.touchPos(320, 540)
        sleep(sleeptime)

    # トレーナー登録ダイアログが出たら、
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\trainer.png' ,400 ,360):

        # トレーナー名入力の位置をタップ
        aapo.touchPos(400, 360)
        sleep(sleeptime)

        # abc と入力
        aapo.inputtext('abc')
        sleep(sleeptime)

        # トレーナー名入力の位置をタップ
        aapo.touchPos(220, 550)
        sleep(sleeptime)

        # 登録ボタンの位置をタップ1
        aapo.touchPos(220, 550)
        sleep(sleeptime)

        # 登録ボタンの位置をタップ2
        aapo.touchPos(220, 550)
        sleep(sleeptime)

        # OKボタンの位置をタップ
        aapo.touchPos(320, 550)
        sleep(sleeptime)

    # データダウンロードダイアログが出たら、OKの位置をタップ
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\datadownload.png', 320, 550):
        aapo.touchPos(320, 550)
        sleep(sleeptime*30)

    # お知らせダイアログが出たら、閉じるの位置をタップ
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\osirase.png' ,220 ,760):
        aapo.touchPos(220, 760)
        sleep(sleeptime)

    # メインストーリー開放ダイアログが出たら、閉じるの位置をタップ
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\main-story.png', 220, 550):
        aapo.touchPos(220, 550)
        sleep(sleeptime)

    # ウマ娘ストーリー開放ダイアログが出たら、閉じるの位置をタップ
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\umamusume-story.png' ,220 ,760):
        aapo.touchPos(220, 760)
        sleep(sleeptime)

    # ウマ娘詳細ダイアログが出たら、閉じるの位置をタップ
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\umamusume-syosai.png', 270 ,680):
        aapo.touchPos(270, 680)
        sleeptime*2

    # ガチャボタンを見つけたら、ロビーと判断
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\roby.png', 450, 880):

        # フォルダ名がカラの場合セット
        if not folderName:
            folderName = datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f')

        # プレゼントの位置をタップ
        aapo.touchPos(400, 590)
        sleep(sleeptime)

        # 一括受取の位置をタップ
        aapo.touchPos(300, 730)
        sleep(sleeptime)

        # 閉じるの位置をタップ1
        aapo.touchPos(130, 730)
        sleep(sleeptime)

        # 閉じるの位置をタップ2
        aapo.touchPos(130, 730)
        sleep(sleeptime)

        # 実績ログが終わるまで10秒ほど待機（メニューボタンが隠れて押せないから）
        sleep(sleeptime*10)

        # メニューボタンの位置をタップ
        aapo.touchPos(438, 44)
        sleep(sleeptime)

        # データ連携の位置をタップ1
        aapo.touchPos(330, 530)
        sleep(sleeptime)

        # データ連携の位置をタップ2
        aapo.touchPos(380, 520)
        sleep(sleeptime)

        # 連携パスワードの位置をタップ
        aapo.touchPos(380, 460)
        sleep(sleeptime)

        # 設定の位置をタップ
        aapo.touchPos(300, 510)
        sleep(sleeptime)

        # 連携パスワード入力の位置をタップ
        aapo.touchPos(120, 345)
        sleep(sleeptime)

        # パスワードを入力
        aapo.inputtext(in_password)
        sleep(sleeptime)

        # 確認入力の位置をタップ1
        aapo.touchPos(120, 430)
        sleep(sleeptime)

        # 確認入力の位置をタップ2
        aapo.touchPos(120, 430)
        sleep(sleeptime)

        # パスワードを入力
        aapo.inputtext(in_password)
        sleep(sleeptime)

        # プライバシーポリシーの位置をタップ1
        aapo.touchPos(115, 520)
        sleep(sleeptime)

        # プライバシーポリシーの位置をタップ2
        aapo.touchPos(115, 520)
        sleep(sleeptime)

        # OKの位置をタップ
        aapo.touchPos(320, 570)
        sleep(sleeptime)

        # 画面キャプチャ
        aapo.screencap()

        # スクショを保存
        aapo.imgSave(distpath + folderName + '\\screenshot_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.png')
        sleep(sleeptime)

        # 閉じるの位置をタップ
        aapo.touchPos(220, 520)
        sleep(sleeptime*3)

        # ガチャボタンの位置をタップ
        aapo.touchPos(400, 770)
        sleep(sleeptime*2)

        # サポートカードの位置をタップ
        aapo.touchPos(420, 490)
        sleep(sleeptime)

    #TODO 位置
    # 10回引く！
    if aapo.touchImg(motoDIR + '.\\.src\\risemara\\10-kaihiku.png', 445, 805):
        sleep(sleeptime)

    #TODO 位置
    # ガチャを引く！
    if aapo.touchImg(motoDIR + '.\\.src\\risemara\\gatyahiku.png', 380 , 645):
        sleep(sleeptime)

    # ガチャ結果
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\gatya-kekka.png'):
        # フォルダ名がカラの場合セット
        if not folderName:
            folderName = datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f')

        # スクショを保存
        aapo.imgSave(distpath + folderName + '\\screenshot_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.png')
        sleep(sleeptime)

        # もう1回引くの位置をタップ
        aapo.touchPos(300, 780)
        sleep(sleeptime)

    # 購入するボタンが出たら、ガチャ終了
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\konyusuru.png'):
        reset()
        start()
        folderName = 0

    # ハンバーガーメニューボタンをタップ
    if aapo.touchImg(motoDIR + '.\\.src\\risemara\\hanba-ga-menu.png', 450, 880):
        sleep(sleeptime)

        # ユーザーデータ削除の位置をタップ1
        aapo.touchPos(90, 650)
        sleep(sleeptime)

        # ユーザーデータ削除の位置をタップ2
        aapo.touchPos(330, 540)
        sleep(sleeptime)

        # ユーザーデータ削除の位置をタップ3
        aapo.touchPos(330, 540)
        sleep(sleeptime)

        # 閉じるの位置をタップ
        aapo.touchPos(220, 550)
        sleep(sleeptime)

        # ロゴをタップ
        if aapo.touchImg(motoDIR + '.\\.src\\risemara\\logo.png'):
            sleep(sleeptime)

        # 同意をタップ
        if aapo.touchImg(motoDIR + '.\\.src\\risemara\\doui.png'):
            sleep(sleeptime)


    # スタック対策
    if aapo.chkImg(motoDIR + '.\\.src\\risemara\\stack.png'):
        sleep(sleeptime)
        stackCount += 1

        if stackCount >= 5:
            reset()
            start()
            stackCount,folderName = 0,0
    main()

if __name__ == '__main__':
    multiinstance()
    start()
    main()