from bing_image_downloader import downloader
import time

def Download_Image(inputString,path,n):
    downloader.download(inputString, limit=n, output_dir=path, adult_filter_off=False, force_replace=False, timeout=3, verbose=True)



def remove_directory(path):
    import shutil
    shutil.rmtree(path)


#remove_directory("pythonDownload")
#Download_Image("bikini instagram girl", "pythonDownload", 50)




