import requests
import urllib.request as req
import os, time, random
import bs4
import crawler_conf as arg

# TODO 取得該台電腦的 Cookie 和 User Agent 
# TODO [V] 爬取 e-hentai 的圖片
# TODO e-hentai整合到 nlang_crawler
# https://e-hentai.org/tag/artist:aroma+sensei
# https://e-hentai.org/g/2119341/7064769124/

def getdata(url):
    # 附加 Request 物件，附加Request Headers 的資訊 這個要看網站的狀況沒有辦法制式化
    request = req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Accept-Language": "zh-TW;q=0.7",
        # "Cache-Control": "max-age=0",
        "Cookie": "cf_clearance=F0fUeQPjzqETdCw.4F3CfdhrYWstntRR9JuJCKcp_AE-1661272157-0-150; csrftoken=GElTSfwxVI7hJwtrDoNCPT2vUNMmbQurQEVc2W4u0G22NHZcCST1VJq8gzRwwuq1; sessionid=vnp97orlcfus3m647zosjfab39kfsqay"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    return data

def get_pageurl_all_eh(data):
    root = bs4.BeautifulSoup(data, "html.parser")
    img_url = root.find_all("div",class_="gdtm")
    return img_url

def get_imgurl_eh(pageurldata):
    root = bs4.BeautifulSoup(pageurldata, "html.parser")
    img_url = root.find("div",id="i3").a.img.get("src")
    return img_url

def imgfolder(folder_,foldername):
    if os.path.exists(os.path.join(folder_,foldername)) == False:
        os.mkdir(os.path.join(folder_,foldername))
        folder_save = os.path.join(folder_,foldername)
        print("This is mkdir: ",folder_save)
    else:
        folder_save = os.path.join(folder_,foldername)
        print('had folder: ',folder_save)
    return folder_save

if __name__ == "__main__":

    # url = r"https://e-hentai.org/g/2119341/7064769124/"
    # folder_save = r"D:\1_29\hentai_cg\cawler_test"

    base_url = arg.BASE_URL
    folder_ = arg.FOLDER
    foldername = arg.FOLDERNAME

    data = getdata(base_url)

    folder_save = imgfolder(folder_,foldername)

    noclean_pageurl_all = get_pageurl_all_eh(data)
    clean_pageurl_all = [pageurl.select_one("a").get("href") for pageurl in noclean_pageurl_all]

    for idx,pageurl in enumerate(clean_pageurl_all):
        pageurldata = getdata(pageurl)

        imgurl = get_imgurl_eh(pageurldata)
        # 提取 img 的副檔名格式
        imgformat = lambda url_str: url_str[-3:]
        imgFormat_split = imgformat(imgurl)
        print("img format:",imgFormat_split)
        # index
        idx +=1
        idx = str(idx)
        print("idx:",idx)

        with open(os.path.join(folder_save,'{}.{}'.format(idx,imgFormat_split)),'wb') as file:
            img_data = requests.get(imgurl)
            file.write(img_data.content)
            file.flush()

        file.close()

        # sleep and output info
        print("第 {} 張".format(idx))
        sleeptime = random.randint(1, 5)
        print("sleep time:", sleeptime)
        time.sleep(sleeptime)

        if int(idx) == len(clean_pageurl_all):
            print("crawler end, total:{} page.".format(idx))