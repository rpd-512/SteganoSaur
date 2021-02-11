from PIL import Image
import os
from os import path

sym = """
 ____  _                              ____
/ ___|| |_ ___  __ _  __ _ _ __   ___/ ___|  __ _ _   _ _ __
\___ \| __/ _ \/ _` |/ _` | '_ \ / _ \___ \ / _` | | | | '__|
 ___) | ||  __/ (_| | (_| | | | | (_) |__) | (_| | |_| | |
|____/ \__\___|\__, |\__,_|_| |_|\___/____/ \__,_|\__,_|_|
               |___/     By RPD-512 ( https://twitter.com/RhiddhiD )

Press ctrl+c or type 'bye' to exit
Type 'clear' to clear screen
               """
def getPath():
    while True:
        try:
            pth = input("Enter file path: ")
            img = Image.open(pth)
            if(img.mode != "RGB"):
                print("File mode "+img.mode+" Not supported")
                continue
            if(len(pth) == 0):
                raise "File doesn't exists"
            break
        except KeyboardInterrupt:
            print("\n| CANCELLED |")
            return
        except:
            print("\n!!! File doesn't exists (press ctrl+c to exit) !!!\n")
    pix = img.load()
    return pix,img,pth

def mainEncode(pix,img,pth):
    while True:
        txt = input("Enter your secret message: ")
        try:
            if(len(txt) != 0):
                break
            else:
                print("\n!!! Can't encrypt empty message (press ctrl+c to exit) !!!\n")
        except KeyboardInterrupt:
            print("\n| CANCELLED |")
            return
    encode(txt,pix,img,pth)

def decode(pix,img):
    binFound = ""
    message = ""
    isDone = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            #print(pix[x,y])
            for i in pix[x,y]:
                isDone += 1
                if(isDone == 9):
                    isDone = 0
                    message += (chr(int(binFound,2)))
                    binFound = ""

                    if(i%2 == 1):
                        return message
                binFound += str(i%2)

def encode(txt,pix,img,pth):
    encTxt = []
    for i in txt:
        encTxt.append(str(format(ord(i),'b')).zfill(8))
    x=0
    y=0
    p=[]
    numChr = 0
    for enc in encTxt:
        numChr += 1
        pos = 0
        x1 = x
        for en in range(len(enc)):
            if(len(p) == 3):
                p=[]
                x1 += 1
            e = int(enc[en])
            if(e == 1):
                if(pix[x1,y][pos] % 2 == 0):
                    p.append(pix[x1,y][pos]+1)
                else:
                    p.append(pix[x1,y][pos])
                pass
            else:
                if(pix[x1,y][pos] % 2 == 1):
                    p.append(pix[x1,y][pos]+1)
                else:
                    p.append(pix[x1,y][pos])
                pass
            pos += 1
            if(pos == 3):
                pos = 0
            if(en == 7):
                lstChr = pix[x,y][2]
                if(numChr == len(txt)):
                    if(lstChr % 2 == 0):
                        p.append(lstChr+1)
                    else:
                        p.append(lstChr)
                else:
                    if(lstChr % 2 == 1):
                        p.append(lstChr+1)
                    else:
                        p.append(lstChr)

            if(len(p) == 3):
                pix[x1,y] = (p[0],p[1],p[2])
                #print(pix[x1,y])
        x+=3
        p=[]
        if(x >= img.size[0]):
            y+=1
            x=0
    name = path.splitext(path.basename(pth))
    img.save(name[0]+"-enc.png")
    print("Done encoding!! Encoded image saved with filename: "+name[0]+"-enc.png")
def main():
    try:
        os.system("clear")
    except:
        os.system("cls")
    print(sym)
    while True:
        job = input("(E)ncrypt an image or (D)ecrypt an image: ")
        if(job.strip(" ").lower() == "bye"):
            print("\nBye!!")
            exit()
        elif(job.strip(" ")==""):
            continue
        elif(job.strip(" ").lower() == "clear"):
            try:
                os.system("clear")
            except:
                os.system("cls")
            continue
        try:
            if(job.lower() != "e" and job.lower() != "d"):
                print("Please select a valid option!!")
            else:
                pix,img,pth = getPath()
                if(job.lower() == "e"):
                    mainEncode(pix,img,pth)
                elif(job.lower() == "d"):
                    print(decode(pix,img))
        except:
            pass

try:
    main()
except KeyboardInterrupt:
    print("\nBye!!")
    exit()
