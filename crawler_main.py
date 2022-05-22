import requests
import urllib.request as req
import os, time, random
import bs4
import crawler_conf as arg

# url = base_url
def getdata(url):
    # 附加 Request 物件，附加Request Headers 的資訊
    request = req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    # print(data)
    return data

#TODO 抓 imh image
# data = getdata(base_url) # 引用getdata
def getimgurl_imh(data):
    root = bs4.BeautifulSoup(data, "html.parser")
    img_url = root.find("a",class_="next_img").img.get("data-src") # 找 data-src
    return img_url
# print(getimgurl_imh(data))

# 抓 nh 
# data = getdata(base_url) # 引用getdata
# print(data)
def getimgurl_nh(data):
    root = bs4.BeautifulSoup(data, "html.parser")
    img_url = root.find("section",id="image-container").a.img # 找image-container
    img_url = img_url.get("src")
    return img_url


# nh 的 img total
# data = getdata(base_url) # 引用getdata
def getimgtotal_nh(data):
    root = bs4.BeautifulSoup(data, "html.parser")
    img_url = root.find_all("div",class_="thumb-container") # 找image-container
    total_img = len(img_url)
    return total_img
# print(getimgtotal_nh(data))

# imh 的 img total
# data = getdata(base_url) # 引用getdata
def getimgtotal_imh(data):
    root = bs4.BeautifulSoup(data, "html.parser")
    img_total_str = root.find("ul",class_="galleries_info").find("li",class_="pages").string # 找image-container
    _, img_total = img_total_str.split("Pages: ")
    img_total = int(img_total)
    return img_total
# print(getimgtotal_imh(data))

# 確認有無圖片資料夾與建一個
def imgfolder(folder_,foldername):
    if os.path.exists(os.path.join(folder_,foldername)) == False:
        folder_mkdir = os.mkdir(os.path.join(folder_,foldername))
        folder_save = os.path.join(folder_,foldername)
        print("This is mkdir: ",folder_save)
    else:
        folder_save = os.path.join(folder_,foldername)
        print('had folder: ',folder_save)
    return folder_save


if __name__ == "__main__":

    base_url = arg.BASE_URL
    startnumber = arg.STARTNUMBER
    folder_ = arg.FOLDER
    foldername = arg.FOLDERNAME

    data = getdata(base_url)

    # 不同網站 img total 
    if "nhentai.net" in base_url:
        endnumber = getimgtotal_nh(data)

    elif "imhentai.xxx" in base_url:
        endnumber = getimgtotal_imh(data)

    print("img_total:",endnumber)

    # 確認有無圖片資料夾與建一個
    folder_save = imgfolder(folder_,foldername)

    for i in range(startnumber,endnumber+1):

        # 確認有超連結字尾
        if base_url[-1] != "/":
            base_url = base_url +"/"
        # print("page_url:",base_url)

        # 判斷 從哪一個網站拿 img
        if "nhentai.net" in base_url:
            page_url = base_url + "{}".format(i)
            Data = getdata(page_url) # 引用getdata
            imgURL = getimgurl_nh(Data)

        elif "imhentai.xxx" in base_url:
            view_url = base_url.replace("gallery","view")
            page_url = view_url + "{}".format(i)
            
            Data = getdata(page_url) # 引用getdata
            imgURL = getimgurl_imh(Data)

        print("page_url:",page_url)
        print("imgURL:",imgURL)

        # 提取 img 的副檔名格式
        imgformat = lambda url_str: url_str[-3:]
        imgFormat_split = imgformat(imgURL)
        print("img format:",imgFormat_split)

        # Save the image to 
        with open(os.path.join(folder_save,'{}.{}'.format(i,imgFormat_split)),'wb') as file:
            img_data = requests.get(imgURL)
            file.write(img_data.content)
            file.flush()

        file.close()

        # sleep and output info
        print("第 {} 張".format(i))
        sleeptime = random.randint(1, 5)
        print("sleep time:", sleeptime)
        time.sleep(sleeptime)

        if i == endnumber:
            print("crawler end, total:{} page.".format(i))

