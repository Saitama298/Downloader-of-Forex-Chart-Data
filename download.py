import requests, os, sys

def verify_folder(folder):
    exists=False
    if os.path.isdir(folder):
        exists=True
    return exists

def create_folder(folder):
    if verify_folder(folder)==False:
        os.mkdir(folder)

def verify_file(file):
    exists=False
    if os.path.isfile(file):
        exists=True
    return exists

def download_file(path, symbol, year, month):
    def get_tk(url):
        r = requests.get(url)
        r = r.text.splitlines()

        tk = ""
        status=0
        index=0
        for i in  range(len(r)):
            result = r[i].find("tk")
            if result!=-1:
                status=1
                index = i
                break
        if status==1:
            tk = r[index]
            lixo, tk = tk.split(' id="tk" ')
            lixo, tk = tk.split('=')
            tk, lixo = tk.split(' ')
            tk = tk[1:-1]
        return tk, status
    
    base_url = 'https://www.histdata.com/download-free-forex-historical-data/?/excel/1-minute-bar-quotes/'
    base_url = base_url+symbol+"/"+year
    if month!="":
        temp = int(month)
        base_url = base_url+"/"+str(temp)
    url = base_url
    tk, status = get_tk(url)
    if status==1:
        url1 = "https://www.histdata.com/get.php"
        payload = {
            "tk": tk,
            "date": year,
            "datemonth": year+month,
            "platform": "XLSX",
            "timeframe": "M1",
            "fxpair": symbol
            }
        
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
            "Cache-Control": "max-age=0",
            "Coonection": "keep-alive",
            "Content-Lenght": "103",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "cookielawinfo-checkbox-non-necessary=yes; cookielawinfo-checkbox-necessary=yes",
            "dnt": "1",
            "Host": "www.histdata.com",
            "Origin": "https://www.histdata.com",
            "Referer": url,
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        }
        r = requests.post(url1, data=payload, headers=headers)
        filename = "HISTDATA_COM_XLSX_"+symbol+"_M1_"+year+month+".zip"
        if verify_file(path+"/"+filename)==False:
            open(path+"/"+filename, 'wb').write(r.content)
        else:
            print("ERROR: file already exists!")
    else:
        print("ERROR: tk not found!")

symbol = sys.argv[1]
os.system("Title "+symbol)
os.system("cls")
path = os.path.dirname(os.path.abspath(__file__))
path = path.replace("\Programs","")
path = path+"/"+symbol+" - files"
create_folder(path)

for i in range(2000,2023):
    try:
        if i==2022:
            for j in range(1,13):
                try:
                    month = "0"+str(j)
                    download_file(path, symbol, str(i), month)
                except:
                    pass
        else:
            download_file(path, symbol, str(i), "")
    except:
        print("There are no records of the year "+str(i)+"!")
