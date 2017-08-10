import re

fow = open("test-backup.txt", "w")
pa = re.compile(u"[\u4e00-\u9fa5]{1,2}")  # 中文
with open("test.txt", "r+") as fo:
    for i in range(100):
        lines = pa.findall(fo.readline())
        # line = fo.readline()
        print(i)
        if(i != '依零'):
            fow.write("依零"+lines+"\n")

fow.close()
