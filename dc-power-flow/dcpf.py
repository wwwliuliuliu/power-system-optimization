import numpy as np
import pandas as pd
import sys
from getDataFrame import getDataFrame

class dcpf(object):
    def __init__(self, filePath, S_B):
        self.path = filePath  # casefile
        self.S_B = S_B  # rated capacity
        self.bus_df, self.gen_df, self.brch_df, self.gencost_df = getDataFrame(path=filePath)

    '''creat branch power flow power sensitivity matrix'''
    def makeBdc(self):
        nbrch = self.brch_df.shape[0]
        nbus = self.bus_df.shape[0]
        f = pd.DataFrame(self.brch_df, columns={'fbus'}).values  # DataFrame->>ndarray
        t = pd.DataFrame(self.brch_df, columns={'tbus'}).values  # DataFrame->>ndarray
        x = pd.DataFrame(self.brch_df, columns={'x'}).values  # DataFrame->>ndarray
        tap = pd.DataFrame(self.brch_df, columns={'ratio'}).values  # DataFrame->>ndarray
        tap[np.where(tap == 0.)] = 1.
        b = 1 / x
        b = b / tap
        Cft = np.zeros([nbrch, nbus])
        for ii in range(nbrch):
            Cft[ii, int(f[ii] - 1)] = 1
            Cft[ii, int(t[ii]) - 1] = -1
        Bf = np.zeros([nbrch, nbus])
        for ii in range(nbrch):
            Bf[ii, int(f[ii] - 1)] = b[ii]
            Bf[ii, int(t[ii]) - 1] = -b[ii]
        Bbus = Cft.T @ Bf
        return Bbus, Bf

    '''create BUS-GEN association matrix'''
    def getMbg(self):
        ngen = self.gen_df.shape[0]
        nbus = self.bus_df.shape[0]
        Mbg = np.zeros([nbus, ngen])
        iBus = pd.DataFrame(self.gen_df, columns={'GEN_BUS'}).values
        for ii in range(nbus):
            for jj in range(ngen):
                if ii == iBus[jj] - 1:
                    Mbg[ii, jj] = 1
        return Mbg

    '''calculate the DC power flow'''
    def run(self, write=0):
        B, Bf = self.makeBdc()
        Pd = pd.DataFrame(self.bus_df, columns={'Pd'}).values
        nbus = Pd.shape[0]
        BUS_TYPE = pd.DataFrame(self.bus_df, columns={'BUS_TYPE'}).values.reshape(nbus).astype(int)
        '''1=PQ bus 2=PV bus 3=slack bus'''
        PQ, PV, slk = 1, 2, 3
        ipq = np.array(np.where(BUS_TYPE == PQ)).flatten() # index
        ipv = np.array(np.where(BUS_TYPE == PV)).flatten()
        islk = np.array(np.where(BUS_TYPE == slk)).flatten()[0]
        BB = np.delete(B, islk, 0)
        BB = np.delete(BB, islk, 1)
        B_noslk_inv = np.linalg.inv(BB)
        nn = B_noslk_inv.shape[0]
        B_add = np.insert(B_noslk_inv, islk, np.zeros(nn), 0)
        B_add = np.insert(B_add, islk, np.zeros(nn + 1), 1)
        T = Bf @ B_add
        Pg = pd.DataFrame(self.gen_df, columns={'Pg'}).values
        Pd = pd.DataFrame(self.bus_df, columns={'Pd'}).values
        Mbg = self.getMbg()
        Pbus = (Mbg @ Pg - Pd) / self.S_B
        # Va is radian, now !
        Va = np.zeros((nbus, 1))
        Va[np.r_[ipv, ipq]] = np.linalg.solve(B[np.r_[ipv, ipq], :][:, np.r_[ipv, ipq]], Pbus[np.r_[ipv, ipq]])
        F = T @ Pbus # branch power flow
        f = pd.DataFrame(self.brch_df, columns={'fbus'}).values
        t = pd.DataFrame(self.brch_df, columns={'tbus'}).values
        nbrch = f.size
        # pretty output
        if write:
            from prettytable import PrettyTable
            xx1 = PrettyTable(['BUS_I', 'Vm/p.u.', 'Va/degrees'])
            xx2 = PrettyTable(['fbus', '->', 'tbus', 'branch power flow/MW'])
            for ii in range(nbus):
                xx1.add_row([ii+1, 1.0, np.around(Va[ii][0]*180/np.pi, decimals=4)]) # Va ->> degrees
            for jj in range(nbrch):
                xx2.add_row([f[jj][0], '->', t[jj][0], np.around(F[jj][0] * self.S_B, decimals=4)])
            print('Result of DC Power Flow')
            print(xx1)
            print(xx2)
        return f, t, F, Va

if __name__ == "__main__":
    # input you case file path
    dcpf = dcpf(filePath='X:/.../caseName/', S_B=100)
    f, t, F, Va = dcpf.run(write=1)