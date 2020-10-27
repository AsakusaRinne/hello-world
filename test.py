def readHdr(fileName):
    fileinfo = {}
    with open(fileName, 'rb') as fd:
        tline = fd.readline().strip()
        if len(tline) < 3 or tline[:2] != b'#?':
            print('invalid header')
            return
        fileinfo['identifier'] = tline[2:]

        # while(tline[:1]==b'#'):
        tline=fd.readline().strip()

        if(tline[:1]==b'#'):
            tline = fd.readline().strip()
        while tline:
            n = tline.find(b'=')
            if n > 0:
                fileinfo[tline[:n].strip()] = tline[n + 1:].strip()
            tline = fd.readline().strip()

        tline = fd.readline().strip().split(b' ')
        fileinfo['Ysign'] = tline[0][0]
        fileinfo['height'] = int(tline[1])
        fileinfo['Xsign'] = tline[2][0]
        fileinfo['width'] = int(tline[3])

        data = [d for d in fd.read()]
        height, width = fileinfo['height'], fileinfo['width']
        if width < 8 or width > 32767:
            data.resize((height, width, 4))
            print("error")
            return rgbe2float(data)

        img = np.zeros((height, width, 4))
        dp = 0
        # c=0
        for h in range(height):
            if data[dp] != 2 or data[dp + 1] != 2:
                print('this file is not run length encoded')
                print(data[dp:dp + 4])
                return
            if data[dp + 2] * 256 + data[dp + 3] != width:
                print('wrong scanline width')
                return
            dp += 4
            for i in range(4):
                ptr = 0
                while (ptr < width):
                    if data[dp] > 128:
                        count = data[dp] - 128
                        if count == 0 or count > width - ptr:
                            print('bad scanline data')
                        img[h, ptr:ptr + count, i] = data[dp + 1]
                        ptr += count
                        dp += 2
                    else:
                        # if(data[dp]==127):
                            # c=c+1
                        count = data[dp]
                        dp += 1
                        if count == 0 or count > width - ptr:
                            print('bad scanline data')
                        img[h, ptr:ptr + count, i] = data[dp: dp + count]
                        ptr += count
                        dp += count
        # return rgbe2float(img)
        # return img,c
        return img
