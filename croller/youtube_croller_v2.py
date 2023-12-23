import json
import os
import string

import pytube
from pytube.exceptions import VideoPrivate, LiveStreamError, AgeRestrictedError,VideoUnavailable
from pytube.cli import on_progress
from pytube import YouTube
import csv

#파일 없을 시 만들어주는 함수
def makedirs(path):
  try:
    os.makedirs(path)
  except OSError:
    if not os.path.isdir(path):
      raise

## MovieNet DataSet Json 파싱
def jsonParsing (filePath):
    with open(filePath) as json_file: # json 파일 오픈
        jsonData = json.load(json_file) # json load
        imdb_id_list = []        
        youtube_id_list = []
        for val in jsonData: # youtube_id_list에 json 파일 속 
            imdb_id_list.append(val['imdb_id'])
            youtube_id_list.append(val['youtube_id']) # 'youtube_id'의 값을 저장
    return imdb_id_list, youtube_id_list

## Youtube link Download
def youtube_download(youtube_id, imdb_id, path) :
    DOWNLOAD_FOLDER = path
    #가져올 링크 넣기
    url = "https://www.youtube.com/watch?v="+youtube_id
    yt = pytube.YouTube(url, on_progress_callback=on_progress)
    #print(yt.streams)
    print("title : ",yt.title)
    print("length : ",yt.length)
    print("publish_date : ", yt.publish_date)
    #print("views : ", yt.views)
    #print("keywords : ", yt.keywords)
    #print("description : ", yt.description)
    #print("thumbnail_url : ", yt.thumbnail_url)
    try :
        yt.streams.filter(progressive=True, file_extension='mp4')\
                    .order_by("resolution")\
                    .desc()\
                    .first()\
                    .download(output_path=DOWNLOAD_FOLDER, filename= imdb_id)
    except VideoPrivate:  # 비공개 영상일 경우 예외처리
        pass
    except AgeRestrictedError:# 연령 제한 영상일 경우 예외처리
        pass
    except LiveStreamError:  # 라이브 영상일 경우 예외처리
        pass
    except VideoUnavailable: # 이용 불가 영상일 경우 예외처리
        pass

# youtube 영상을 저장할 path 지정
# vid_save_path = '/home/gpuadmin/data/mv_trailer'
vid_save_path = 'E:\\NRF_2022\\vid_dataset' + '\\mv_trailer'

makedirs(vid_save_path)

youtube_id=[]
imdb_id=[]
# json_path='/home/gpuadmin/dev/multi-label-classification/dataset/filtered_trailer_url_s1.json' # 1200개
json_path='../dataset/filtered_trailer_url_s1.json'
imdb_id=jsonParsing(json_path)[0]
youtube_id=jsonParsing(json_path)[1]
print(youtube_id[0])
print(imdb_id)
print(len(youtube_id))



# printable한 문자로만 처리 (ex ASCII CODE)
# 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
# !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c
f = open('vid_dataset.csv','w', newline='')
wr = csv.writer(f)
i=0
j=0

# youtube_id 개수만큼 다운로드
# while i<=len(youtube_id):
while i<20:
    try :
        print(f"youtube_id:{youtube_id[i]}")
        printable = set(string.printable)
        ' '.join(filter(lambda x: x in printable, youtube_id[i]))
        youtube_download(youtube_id[i], imdb_id[i], vid_save_path)
        path_imdb_id = vid_save_path + '\\' + imdb_id[i]
        wr.writerow([path_imdb_id]) # 실제 다운로드된 트레일러 영상의 imdb_id를 csv 파일에 행 단위로 기록
        i += 1
        j += 1
        print(f"progress:{i}")
        print(f"extract:{j}")
    except VideoPrivate: # 비공개 영상일 경우 예외처리
        i += 1
        print(f"progress:{i}")
        continue
    except AgeRestrictedError:# 연령 제한 영상일 경우 예외처리
        i += 1
        print(f"progress:{i}")
        continue
    except LiveStreamError:  # 라이브 영상일 경우 예외처리
        i += 1
        print(f"progress:{i}")
        continue
    except VideoUnavailable:  # 이용불가 영상일 경우 예외처리
        i += 1
        print(f"progress:{i}")
        continue
    except :
        i += 1
        print(f"progress:{i}")        
        print('etc...\n')
        continue
print(f"총 비디오 갯수:{i}")
print(f"추출된 비디오 갯수:{j}")