#!/usr/bin/python

#IPv4 to 32bit 
def convert(ip):
    list=ip.split(".")
    list=map(int,list)
    list=map(bin,list)
    list=map(str,list)
    list=map(cut,list)
    list=map(binpro,list)
    return "".join(list)

def cut(str):
    return str[2:]

def binpro(bin):
    bin=str(bin)
    if len(bin) >= 8:
        return bin
    else:
        bin='0%s'%(bin)
        return binpro(bin)
    

def getmask(b1,b2):
    if len(b1)!=len(b2): return ''
    mask=0
    for i in range(len(b1)):
        yu=int(b1[i:])
        if yu !=0:
            mask=mask+1
       
    return mask


p=open("./p.txt",'r')
line=p.readline()
while line:
    line=line.strip()
    l=line.split("-")
    ip1=l[0].strip()
    ip2=l[1].strip()
    mask=getmask(convert(ip1),convert(ip2))
    print '%s/%s'%(ip1,mask)
    line=p.readline()
p.close()

