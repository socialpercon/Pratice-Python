import re
import urllib
fileNo = 0
racingGirlUrl = 'http://gall.dcinside.com/list.php?id=racinggirl&no='

for no in range(170710, 170720):
    url = racingGirlUrl + str(no)
    f = urllib.urlopen(url)
    html = f.read()
    imageUrlList = re.findall("http://image.dcinside.com/download.php[^']+", html)
    print imageUrlList
    for url in imageUrlList:
        print fileNo
        contents = urllib.urlopen(url).read()
        file(str(fileNo)+'.jpg', 'wb').write(contents)
        fileNo = fileNo + 1
