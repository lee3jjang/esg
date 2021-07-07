# 내부구조 상관없고 무조건 엑셀 매크로랑 똑같이 나오게 하면됨

import numpy as np
import logging
logging.basicConfig(format=None, level=logging.INFO)
logger = logging.getLogger()

class Ytm2Spot:
    def __init__(self, alpha: float, freq: int):
        self.alpha = alpha
        self.freq = freq

    def _ytm_price(self, tenor: float, ytm: float) -> float:
        dt = 1/self.freq
        P = 0
        T = tenor

        while T>0:
            if T==tenor:
                CF = 1+ytm/self.freq
            else:
                CF = ytm/self.freq

            if np.abs(T/dt - int(T/dt)) < 1e-7:
                DF = (1+ytm/self.freq)**(-T*self.freq)
            else:
                DF = 1/(1+ytm*T)
        
            P += CF*DF
            T -= dt

        return P



    def convert(self, tenor: np.ndarray, ytm: np.ndarray) -> np.ndarray:
        # 입력데이터 검사
        if len(tenor) != len(ytm):
            raise Exception('만기와 수익률 입력데이터 길이 불일치')
        
        self.ltfr = np.log(1+ytm[np.argmax(tenor)])
        n = len(tenor)

        # 1. C 행렬 만들기
        # 1.1 C 행렬의 Column 개수 결정
        k = 0
        for i in range(n):
            k = k + int(np.ceil(tenor[i]*self.freq))

        # 1.2 U 행렬 (S.W에서 W 행렬을 만들기 위한 시점 정보) 생성
        C_col_candidate = np.zeros(k)
        C_col_candidate2 = np.zeros(k)

        k = 0
        for i in range(n):
            for j in range(int(np.ceil(tenor[i]*self.freq))):
                C_col_candidate[k] = tenor[i] - j*(1/self.freq)
                k += 1
        
        N2 = 0
        for i in range(len(C_col_candidate)):
            tmp = np.min(C_col_candidate)
            if tmp == 99999:
                break
            C_col_candidate2[N2] = tmp
            N2 += 1
            for j in range(len(C_col_candidate)):
                if C_col_candidate[j] == tmp:
                    C_col_candidate[j] = 99999
        
        T = np.zeros(N2)
        for i in range(N2):
            T[i] = C_col_candidate2[i]

        # 1.3 C행렬 만들기
        # TODO: 수정
        c = np.zeros([n, N2])
        for i in range(n):
            tmp = tenor[i]
            for j in range(N2):
                if T[j] > tmp:
                    c[i, j] = 0
                elif tmp == T[j]:
                    c[i, j] = 1+ytm[i]/self.freq
                elif 12*(tmp-T[j])%(12/self.freq) == 0:
                    c[i, j] = ytm[i]/self.freq
                else:
                    c[i, j] = 0

        # 2. m, u 벡터 만들기
        m = np.zeros(n)
        u = np.zeros(N2)
        for i in range(n):
            m[i] = self._ytm_price(tenor[i], ytm[i])
        for i in range(N2):
            u[i] = np.exp(-self.ltfr*T[i])

        # 3. W 행렬 만들기
        W = np.zeros([N2, N2])
        for i in range(N2):
            for j in range(i, N2):
                W[i, j] = np.exp(-self.ltfr*(T[i]+T[j]))*(self.alpha*min(T[i], T[j])-0.5*np.exp(-self.alpha*max(T[i], T[j]))*(np.exp(self.alpha*min(T[i], T[j]))-np.exp(-self.alpha*min(T[i], T[j]))))
                if i != j:
                    W[j, i] = W[i, j]

        # 4. ZETA 계산  (CWC')^-1 * (m-Cu) & ZETA conversion
        m_Cu = np.zeros(n)
        m_Cu = c@(u.T)
        for i in range(n):
            m_Cu[i] = m[i] - m_Cu[i]
        zeta = np.linalg.inv(c@W@(c.T))@m_Cu
        zeta2 = (c.T)@zeta

        # 5. tt : output 시점 계산
        tt = tenor.copy()

        # 6. 금리 계산
        result = np.zeros(n)
        for i in range(n):
            tmp = np.exp(-self.ltfr*tt[i])
            for j in range(N2):
                tmp += zeta2[j]*(np.exp(-self.ltfr*(tt[i]+T[j]))*(self.alpha*min(tt[i], T[j])-0.5*np.exp(-self.alpha*max(tt[i], T[j]))*(np.exp(self.alpha*min(tt[i], T[j]))-np.exp(-self.alpha*min(tt[i], T[j])))))
            result[i] = -np.log(tmp)/tt[i]
        
        return result

if __name__ == '__main__':
    
    tenor = np.array([0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 5, 7, 10, 15, 20, 30, 50])
    ytm = np.array([0.00416, 0.00527, 0.00595, 0.00656, 0.008, 0.00886, 0.00974, 0.0097, 0.01168, 0.01335, 0.01528, 0.01722, 0.01802, 0.01832, 0.01832, 0.01827])

    converter = Ytm2Spot(alpha=0.1, freq=2)
    spot = converter.convert(tenor, ytm)
    spot_vba = np.array([0.00415783829864592, 0.00526306894787356, 0.00593853665922484, 0.00655137510958086, 0.00799151072094341, 0.0088523545948423, 0.00973544200019318, 0.00969190242215475, 0.0116966438585723, 0.0133973144270576, 0.0153740875695134, 0.01739076420042, 0.018182727715511, 0.0184685440160738, 0.0183856061026744, 0.0182609649942996])
    
    error = max(np.abs(spot-spot_vba))
    print(f'최대오차 : {error}')
