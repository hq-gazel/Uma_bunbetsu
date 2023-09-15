import configparser, os

def  bunbetsu():
    global path_tesseract, filerng_low, filerng_high, graphic_comp_p, sheetname
    if not os.path.exists('config.ini'): 
        f = open('config.ini', 'w', encoding='SHIFT-JIS')
        textlist = ['[PATH]\n','Tesseract = C:\\Program Files\\Tesseract-OCR\n\n\n',
                        '[SETTINGS]\n'
                        'filerng_low = 7\n', 'filerng_high = 10\n', '#何枚以下か判別lowが最低枚数、highが最大枚数\n\n',
                        'graphic_comp_p = 95\n', '#NORM_HAMMINGは95、NORM_L2SQRは250000\n','#しきい値設定、0に近いほど比較一致率が高い\n',
                        'sheetname = TEST\n#Google Sheets名を指定']
        f.writelines(textlist)
        f.close()


    inifile = configparser.ConfigParser()
    inifile.read('config.ini', 'SHIFT-JIS')

    path_tesseract = inifile.get('PATH', 'Tesseract')
    filerng_low = inifile.get('SETTINGS', 'filerng_low')
    filerng_high = inifile.get('SETTINGS', 'filerng_high')
    graphic_comp_p = inifile.get('SETTINGS', 'graphic_comp_p')
    sheetname = inifile.get('SETTINGS', 'sheetname')

    filerng_low = int(filerng_low)
    filerng_high = int(filerng_high)
    graphic_comp_p = int(graphic_comp_p)

    if not path_tesseract or not filerng_low or not filerng_high or not graphic_comp_p:
        input('config.iniを確認してください\nキーを押して終了します')
        exit()