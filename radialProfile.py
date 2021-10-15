import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from math import sqrt, atan2, pi as PI
from skimage.measure import moments,moments_central,inertia_tensor,inertia_tensor_eigvals,regionprops
from skimage.filters import threshold_otsu
import os

def radialMean(im,x0,y0,h,w,rs):
    yy,xx=np.mgrid[0:h,0:w]
    rr= np.sqrt((xx-x0)**2+(yy-y0)**2)
    #rs = range(rmax)
    means = []
    maxs = []
    mins = []

    #plt.figure()
    #plt.imshow(rr)
    #plt.show()

    for r in range(len(rs)):
        mask = (np.uint32(rr)==r)
        a=im[mask]
        means.append(a.mean())
        maxs.append(a.max())
        mins.append(a.min())
    #rs = np.array(rs) * 0.065
    return means,maxs,mins

def orientation(inertia_tensor):
    a, b, b, c = inertia_tensor.flat
    if a - c == 0:
        if b < 0:
            return -PI / 4.
        else:
            return PI / 4.
    else:
        return 0.5 * atan2(-2 * b, c - a)

def covImg(im):
    M = moments(im)
    cx,cy = (M[1, 0] / M[0, 0], M[0, 1] / M[0, 0])
    mu = moments_central(im,[cx,cy])
    cov = inertia_tensor(im,mu)
    eigvals,w = np.linalg.eigh(cov)
    l1,l2 = np.clip(eigvals, 0, None, out=eigvals)
    #lmin = min(l1,l2)
    #lmax = max(l1,l2)
    ec = np.sqrt(1 - l1 /l2)
    ori = orientation(cov)
    return cx,cy,cov,l1,l2,w,ec,ori

def runOneCell(position, maskFileName, folder, rs):
    #positions = [[position[0],position[1]]]
    #maskFileNames = [maskFileName]

    imgName = folder+'/stackGFP.tif'
    print('imgName',imgName)
    img = mpimg.imread(imgName)
    #maxR = 1100

    #print('dtype',img.dtype,'max',img.max())
    h,w=img.shape
    #print('w',w,'h',h)

    f,[[axA,axB,axC],[axD,axE,axF]]=plt.subplots(2,3)
    imgplot = axA.imshow(img, cmap="gray")
    
    thresh = threshold_otsu(img)
    binary = img > thresh
    img = img*binary
    imgplot = axB.imshow(img, cmap="gray")

    #names = []
    #eccs = []
    #sols = []
    #profiles = []
    #smProfiles = [] 

    #for cid,(maskName,pos, rmax) in enumerate(zip(maskFileNames,positions,maxR)):
    #names.append(maskFileName[:-4])
    name = maskFileName[:-4] 
    #cellIds.append(cid)
    #print('mask path',folder+"/"+maskFileName)
    mask = mpimg.imread(folder+"/"+maskFileName)
    #plt.figure()
    #plt.imshow(mask)

    celli = img * (mask>0)
    #plt.figure()
    axC.set_title(maskFileName[:-4])
    imgplot = axC.imshow(celli, cmap="gray")

    x0, y0 = position
    means,maxs,mins = radialMean(celli,x0,y0,h,w,rs)
    cy,cx,cov,l1,l2,w,ec,ori = covImg(celli)
    props = regionprops(np.uint(celli>0),celli)
    f,[ax1,ax2,ax3]=plt.subplots(1,3,sharex=True,sharey=True)
    ax1.set_title(maskFileName[:-4])
    ax2.imshow(props[0].image)
    ax1.imshow(props[0].intensity_image)
    ax3.imshow(props[0].convex_image)
    sol=np.sum(props[0].image)/np.sum(props[0].convex_image)
    #print('props sum intensity',props[0].mean_intensity*props[0].area,np.sum(celli))
    #print('props',props[0].weighted_centroid)
    #print('props',props[0].inertia_tensor)
    #print('cov',cov)
    #print('eiv',l1,l2,w)
    print('ec',ec)
    print('cy,cx',cy,cx)
    print('y0,x0',y0,x0)
    print('sol',np.sum(props[0].image),np.sum(props[0].convex_image),sol)
    #eccs.append(ec)
    #sols.append(sol)
    #profiles.append(maxs)
    #smProfiles.append(maxs)

    maxRad, minRad, meanRad = rs[maxs.index(max(maxs))], rs[mins.index(max(mins))], rs[means.index(max(means))]

    # Here you choose the value of the averaging in um
    averageOver=0.5

    div,tmp,thres,precRad=0.,0.,0.,0
    tabAvgMax, tabRsAvgMax=[],[]
    for i in range(len(maxs)):
        if rs[i]>=precRad+averageOver:
            precRad+=averageOver
            tabRsAvgMax.append(precRad)
            tabAvgMax.append(tmp/(div+1e-10))
            tmp,div=0.,0.
        tmp+=maxs[i]
        div+=1

    #Questa parte adesso non serve più?#############
    txt="Radius (um)\tIntensity\n"
    for i in range(len(tabAvgMax)):
        a=round(tabRsAvgMax[i] * 2) / 2
        b=round(tabAvgMax[i] * 2) / 2
        txt+=str(a)+"\t"+str(b)+"\n"
    with open(folder+"/AvgInt_"+imgName.replace(folder+"/", "") + "_" + maskFileName.replace(".tif", "")+".xls", "w+") as f:
        f.write(txt)
    #################################################

    print("The radius with maximum intensity is:", maxRad, "microns (" +str(maxRad/0.065)+"pixels)")

    fig, ax = plt.subplots()
    ax.set_title(' '.join(imgName.split('/')[:2])+' ' +maskFileName)
    ax.plot(np.array(rs),maxs,label='max',linewidth=1)
    ax.plot(maxRad, maxs[maxs.index(max(maxs))], "or", label="(d=%.2f $\mu m$ ; I=%.2f)" %(maxRad,max(maxs)), markersize=6)
    ax.plot(tabRsAvgMax, tabAvgMax, linewidth=2)
    #plt.plot(np.array(rs),means,label='mean',linewidth=0.7)
    #rs_mins = rs
    ## If you want to consider only the mins>0 and not =0, add this code:
    #mins, rs_mins = [x for x in mins if x>0], [rs[i] for i in range(len(mins)) if mins[i]>0]
    #plt.plot(np.array(rs_mins),mins,label='mins', linewidth=0.7)
    ax.legend()
    ax.set_xlabel(r"Radius ($\mu m$)")
    ax.set_ylabel("Fluorescence Intensity (a.u.)")
    plt.savefig(folder+"/Graph_" + imgName.replace(folder+"/", "") + "_" + maskFileName.replace(".tif", "") + ".pdf", dpi=600)

    fig, ax = plt.subplots()
    #plt.title("")
    imgplot = axD.imshow(celli, cmap="gray")
    imgplot = ax.imshow(celli, cmap="gray")
    ax.set_yticks([])
    ax.set_xticks([])

    print('max pixel ',maskFileName ,celli.max())
    print('min pixel ',maskFileName ,celli[mask>0].min())
    print('mean int',maskFileName,celli[mask>0].mean())

    for rc in range(0,1100,77):
        cir = plt.Circle((x0, y0), rc, fill=False, color='b')
        ax.add_artist(cir)

    cir = plt.Circle((x0, y0), maxRad/0.065, fill=False, color='r')
    ax.add_artist(cir)

    x1 = cx + np.cos(ori-PI / 2.) * 2 * np.sqrt(l2)
    y1 = cy - np.sin(ori-PI / 2.) * 2 * np.sqrt(l2)
    x2 = cx - np.sin(ori-PI / 2.) * 2 * np.sqrt(l1)
    y2 = cy - np.cos(ori-PI / 2.) * 2 * np.sqrt(l1)
    ax.plot((cx, x1), (cy, y1), '-r', linewidth=2.5)
    ax.plot((cx, x2), (cy, y2), '-r', linewidth=2.5)
    ax.plot(cx, cy, '.g', markersize=15)

    plt.savefig(folder+"/Circ_"+imgName.replace(folder+"/", "").replace("GFP.tif", "")+"_"+maskFileName.replace(".tif", "")+".pdf", dpi=600)
    #plt.show()
    #plt.close()
    plt.close('all')

    return name, ec, sol,maxs, tabAvgMax, tabRsAvgMax


if __name__ == "__main__":

    with open("eccSols.txt", "w") as f:
        f.write('day \t folder \t num \t eccentricity \t solidity \n')

    rmax = 1100
    rs = np.arange(rmax+1) * 0.065
    with open("profiles.txt", "w") as f:
        f.write('day \t folder \t num')
        for r in rs:
            f.write('\t' + '{0:.3f}'.format(r))
        f.write('\n')

    rsSmooth = np.arange(0.5,(rmax + 1)*0.065,0.5)
    with open("profilesSmooth.txt", "w") as f:
        f.write('day \t folder \t num')
        for r in rsSmooth:
            f.write('\t' + '{0:.3f}'.format(r))
        f.write('\n')
 
    days = [day for day in os.listdir() if os.path.isdir(day) and not ('.' in day) ]
    print('days',days)

    for day in days:
        print('day',day)
        dicPos={}
        with open(day+"/coordinates.txt", "r") as f:
            for l in f:
                (folder, name, posx, posy) = l.replace("\n", "").split("\t")
                posx, posy = float(posx), float(posy)
                try:
                    dicPos[folder][name]=[posx, posy]
                except:
                    dicPos[folder]={}
                    dicPos[folder][name]=[posx, posy]


        print('dicPos',dicPos.keys())
        #print('dicPos[M0_2]',dicPos['M0_2'].keys())
        #print('dicPos[M0_2][cell1]',dicPos['M0_2']['cell1'])

        folders = [name for name in os.listdir(day)]
        print('folders',folders)
        for folder in folders:
            if folder not in dicPos:
                continue

            files = [name for name in os.listdir(day+'/'+folder)]

            for file in files:
                if "cell" not in file or ".tif" not in file or "xls" in file:
                    continue
                file = file.replace(".tif", "")
                if file not in dicPos[folder]:
                    continue

                #print('path to get stuff', folder, file)
                name,ecc,sol, maxs, profilesSmooth, profilesSmoothRs = runOneCell(dicPos[folder][file], file+".tif", day+'/'+folder, rs)

                #print('rsSmooth')
                #print(rsSmooth)
                #print(profilesSmoothRs)
                with open("eccSols.txt", "a") as f:
                    #print(day,name,ecc,sol)
                    f.write(day+'\t'+folder+'\t'+str(name)+'\t'+str(ecc)+'\t'+str(sol)+'\n')

                with open("profiles.txt", "a") as f:
                    #print(name)
                    f.write( day +'\t'+ folder + '\t' + str(name))
                    for m in maxs:
                        f.write('\t' + str(m))
                    f.write('\n')


                with open("profilesSmooth.txt", "a") as f:
                    #print(name)
                    f.write( day +'\t'+ folder + '\t' + str(name))
                    for m in profilesSmooth:
                        f.write('\t' + str(m))
                    f.write('\n')
