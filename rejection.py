"""---------- Batchaya Noumeme Yacynte Divan ----------"""
"""---------- Bachelor's in Mechatronics Thesis ----------"""
"""---------- Development of Monocular Visual Odometry Algorithm, WS 23/24 ----------"""
"""---------- Technische Hochshule Wuerzburg-Schweinfurt ---------"""

import numpy as np
from ransac import estimate_foe

def inlier_static(q2,d,S,inlier_threshold):
    foe, inlie = estimate_foe(d, inlier_threshold )
 
    q2 = q2[inlie]
    d = d[inlie]
    a = np.sqrt(d[:,0]**2 + d[:,1]**2)
    dm = np.median(a, axis=0)
    dm = np.linalg.norm(dm)

    drr = np.where(a < 2*dm) 
    dr = d[drr]
    qr = q2[drr]

    return qr, dr, foe+np.array([S[1]/2,S[0]/2])

def inlier_dynamic(q2,d,S,inlier_threshold):
    n = 3
    S = np.array(S)
    u = np.zeros((S[0],S[1],2))
    u[np.reshape(q2[:,1],-1),np.reshape(q2[:,0],-1)] = d
    S = np.intp(S/n)
    foes = np.zeros((n*n,2))
    i3 = 0

    dd = [] 
    qd = [] 
    for j in range(0,n):
        for i in range(0,n):
            i3 += 1
            k = q2[np.where(np.all(np.array([i*S[1],j*S[0]]) <= q2,axis=1) & np.all(np.array([(i+1)*S[1],(j+1)*S[0]])>q2,axis=1)),:]
            k = k[0,:,:]
            d_rob = u[np.reshape(k[:,1],-1),np.reshape(k[:,0],-1)]
            if np.shape(d_rob)[0] <= 2:
                # print("break")
                continue
            
            foe, inliers = estimate_foe(d_rob, inlier_threshold)
            foes[i3-1,:] = np.array(foe) + np.array([(i+0.5)*S[1],(j+0.5)*S[0]])
            q_rob = k[inliers]
            d_rob = d_rob[inliers]
            if np.shape(d_rob)[0] <= 2:
                # print("break")
                continue
            a = np.sqrt(d_rob[:,0]**2 + d_rob[:,1]**2)
            dm = np.median(a)
            dm = np.linalg.norm(dm)
            # print(dm)
            drr = np.where(a < 2*dm) 
            dr = d_rob[drr]
            qr = q_rob[drr]
            for di, qi in zip(dr, qr):
                dd.append(di)
                qd.append(qi)

    return np.array(qd), np.array(dd), foes
    #return kd, ddr , foes, n

