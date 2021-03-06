import numpy as np
from typing import List
from scipy.integrate import quad
from scipy.optimize import minimize_scalar, minimize
from scipy.stats import norm, multivariate_normal

{'Updates' : '2020-04-09', 'Version': '1.2.1'}
# Dynamics 수정(1st order approx. → exact form)
# (2020.04.09) 일단 1st order approx.로 가고 나중에 exact form으로 수정하겠음
# (2020.04.09) 금리시나리오 생성 시 자산쪽 상승(Level2) 충격 줄 때 α 계산 이후로 엑셀이랑 안 맞음

def sample():
    dt = 1/12
    maturity = np.array([1,3,5,10,20])
    data = np.array([
        [0.01995,0.02039,0.02158,0.02415,0.02603],
        [0.01981,0.02024,0.02116,0.02346,0.02518],
        [0.01838,0.01865,0.01969,0.02276,0.02466],
        [0.01703,0.01739,0.01857,0.02177,0.02373],
        [0.01746,0.01875,0.0211,0.0249,0.0271],
        [0.0163,0.01773,0.0204,0.02468,0.02679],
        [0.01597,0.01777,0.02048,0.0245,0.02658],
        [0.01582,0.01735,0.01946,0.02308,0.02498],
        [0.01553,0.01651,0.01846,0.02216,0.02388],
        [0.01546,0.01627,0.01784,0.02088,0.02222],
        [0.01631,0.01752,0.01945,0.02254,0.02366],
        [0.01635,0.01719,0.01902,0.02181,0.02278],
        [0.01587,0.01628,0.01772,0.02025,0.02121],
        [0.01469,0.01474,0.01586,0.01826,0.01919],
        [0.01507,0.01498,0.01611,0.01854,0.01918],
        [0.01493,0.01468,0.01569,0.0181,0.01892],
        [0.0148,0.01455,0.01551,0.01787,0.01886],
        [0.01361,0.01334,0.01406,0.01617,0.01712],
        [0.0126,0.01218,0.01246,0.01401,0.01482],
        [0.01265,0.01238,0.01264,0.01417,0.01489],
        [0.01322,0.01312,0.01353,0.01512,0.01545],
        [0.01369,0.01361,0.01412,0.01596,0.01641],
        [0.01511,0.01609,0.01739,0.01965,0.0204],
        [0.01576,0.01692,0.01873,0.02159,0.02186],
        [0.01496,0.01643,0.01821,0.02111,0.02168],
        [0.01465,0.01665,0.01861,0.02163,0.02214],
        [0.01485,0.01709,0.01909,0.02221,0.02302],
        [0.01467,0.01678,0.01859,0.02182,0.02302],
        [0.01464,0.0169,0.01906,0.02257,0.02388],
        [0.01461,0.01673,0.01864,0.02165,0.02266],
        [0.01464,0.0174,0.01942,0.02252,0.02317],
        [0.01471,0.0178,0.01987,0.02287,0.02364],
        [0.01481,0.01785,0.01989,0.02286,0.02318],
        [0.01654,0.02026,0.02247,0.02455,0.02411],
        [0.01787,0.0215,0.02355,0.0254,0.02518],
        [0.01833,0.021,0.02298,0.02472,0.02439],
        [0.01839,0.0219,0.02444,0.02626,0.02571],
        [0.01851,0.02277,0.02537,0.0277,0.02738],
        [0.01875,0.02271,0.02501,0.02708,0.02704],
        [0.01873,0.02192,0.02436,0.02655,0.02671],
        [0.01887,0.0225,0.02532,0.02757,0.02754],
        [0.01851,0.02175,0.02442,0.02656,0.02649],
        [0.01842,0.02097,0.02338,0.02549,0.02547],
        [0.0183,0.02019,0.02242,0.02458,0.02429],
        [0.0179,0.01953,0.02128,0.02315,0.02265],
        [0.01853,0.0201,0.02164,0.02338,0.02284],
        [0.01844,0.0194,0.02048,0.02209,0.02159],
        [0.01776,0.01825,0.01893,0.01992,0.01969],
        [0.01733,0.01807,0.01879,0.01991,0.02023],
        [0.0176,0.01802,0.01869,0.01988,0.0205],
        [0.01769,0.01789,0.01838,0.01953,0.01995],
        [0.01751,0.01736,0.01771,0.01889,0.01913],
        [0.01711,0.01679,0.01716,0.01828,0.01865],
        [0.0156,0.01496,0.0153,0.01618,0.0166],
        [0.01478,0.01382,0.01421,0.01506,0.0152],
        [0.01186,0.01164,0.01201,0.01254,0.01251],
        [0.01228,0.01287,0.01353,0.0142,0.01386],
        [0.01298,0.01357,0.01442,0.01577,0.01568],
        [0.01386,0.01492,0.01593,0.0175,0.01709],
        [0.0135,0.0139,0.01481,0.01653,0.01628]
    ])
    return dt, maturity, data





class SmithWilson:
    
    """
        Example
        -------
            >>> data = np.array([
                    [1, 0.01301],
                    [3, 0.01325],
                    [5, 0.01415],
                    [10, 0.01600],
                    [20, 0.01625],
                    [30, 0.01604]
                ])

            >>> X_train = data[:, 0]
            >>> y_train = data[:, 1]
            >>> ltfr = 0.045
            >>> terminal = 60

            >>> sw = SmithWilson(np.log(1+ltfr), terminal)
            >>> sw.train(X_train, y_train)

            >>> maturity = np.linspace(0, 100, 1201)
            >>> spot_rate = sw.spot(maturity)
            >>> bond_price = sw.bond(maturity)
            >>> forward_rate = sw.forward(maturity)
    """
    
    def __init__(self, ltfr, cp, tol=1e-4):
        self.ltfr = ltfr
        self.cp = cp
        self.tol = tol
    
    def train(self, X, y):
        m = 1/(1+y)**X
        mu = np.exp(-self.ltfr*X)
        n = len(X)
        
        def obj_fun(alpha):
            W = self._wilson(X[:, None], X, alpha)
            zeta = (m-mu)@np.linalg.inv(W)
            W_T = self._wilson(self.cp, X, alpha)
            derivW_T = self._wilson(self.cp, X, alpha, order=1)
            bond0_T = np.exp(-self.ltfr*self.cp) + W_T@zeta
            bond1_T = -self.ltfr*np.exp(-self.ltfr*self.cp)+derivW_T@zeta
            forward_T = -bond1_T/bond0_T
            error = abs(self.ltfr-self.tol-forward_T)
            return error
        
        res = minimize_scalar(obj_fun, method='bounded', bounds=(1e-4,1), options={'disp':False})
        self._alpha = res.x
        W = self._wilson(X[:, None], X, self._alpha)
        self._zeta = np.linalg.inv(W)@(m-mu)
        self._u = X.copy()
        
    def bond(self, t, order=0):
        if type(t) != np.ndarray:
            t = np.array([t])
            bond = (-self.ltfr)**order*np.exp(-self.ltfr*t)+self._wilson(t[:, None], self._u, self._alpha, order)@self._zeta
            return bond[0]
        else:
            bond = (-self.ltfr)**order*np.exp(-self.ltfr*t)+self._wilson(t[:, None], self._u, self._alpha, order)@self._zeta
            return bond
        
    def spot(self, t: float, compounding: str='annually'):
        if type(t) != np.ndarray:
            t = np.fmax(np.array([t]), 1e-6)
            P = np.exp(-self.ltfr*t)+self._wilson(t[:, None], self._u, self._alpha)@self._zeta
            sp = ((1/P)**(1/t) - 1)[0]
        else:
            t = np.fmax(t, 1e-6)
            P = np.exp(-self.ltfr*t)+self._wilson(t[:, None], self._u, self._alpha)@self._zeta
            sp = (1/P)**(1/t) - 1
        
        if compounding=="continuously":
            return np.log(1+sp)
        elif compounding=="annually":
            return sp
        else:
            raise Exception("compounding 입력 오류")
    
    def forward(self, t: float, order: int=0, x: int=0, compounding: str='continuously'):
        if x==0:
            if type(t) != np.ndarray:
                t = np.array([t])
                if order==0:
                    fwd = -self.bond(t, 1)/self.bond(t, 0)
                elif order==1:
                    fwd = -1/self.bond(t, 0)*(-self.bond(t, 1)**2/self.bond(t, 0)+self.bond(t, 2))
                else:
                    raise Exception('order 입력 오류')
            else:
                if order==0:
                    fwd = -self.bond(t, 1)/self.bond(t, 0)
                elif order==1:
                    fwd = -1/self.bond(t, 0)*(-self.bond(t, 1)**2/self.bond(t, 0)+self.bond(t, 2))
                else:
                    raise Exception('order 입력 오류')

            if compounding=="continuously":
                return fwd
            elif compounding=="annually":
                return np.exp(fwd)-1
            else:
                raise Exception("compounding 입력 오류")
        elif x in range(1, 13):
            fwd = (self.bond(t)/self.bond(t+x/12))**(12/x)-1

            if compounding=="continuously":
                return np.log(1+fwd)
            elif compounding=="annually":
                return fwd
            else:
                raise Exception("compounding 입력 오류")
        else:
            raise Exception('x 입력 오류')
    
    def _wilson(self, t, u, alpha, order=0):
        if order == 0:
            W = np.exp(-self.ltfr*(t+u))*(alpha*np.fmin(t,u) - np.exp(-alpha*np.fmax(t,u))*np.sinh(alpha*np.fmin(t,u)))
        elif order == 1:
            W = np.where(t < u, np.exp(-self.ltfr*t-(alpha+self.ltfr)*u)*(self.ltfr*np.sinh(alpha*t)-alpha*np.cosh(alpha*t)-alpha*(self.ltfr*t-1)*np.exp(alpha*u)), \
                    np.exp(-self.ltfr*u-(alpha+self.ltfr)*t)*((alpha+self.ltfr)*np.sinh(alpha*u)-alpha*self.ltfr*u*np.exp(alpha*t)))
        elif order == 2:
            W = np.where(t < u, np.exp(-self.ltfr*t-(alpha+self.ltfr)*u)*(-(alpha**2+self.ltfr**2)*np.sinh(alpha*t)+2*alpha*self.ltfr*np.cosh(alpha*t)+alpha*self.ltfr*(self.ltfr*t-2)*np.exp(alpha*u)), \
                    np.exp(-self.ltfr*u-(alpha+self.ltfr)*t)*(alpha*self.ltfr**2*u*np.exp(alpha*t)-(alpha+self.ltfr)**2*np.sinh(alpha*u)))
        else:
            raise Exception('order 입력 오류')
        return W
    

class NelsonSiegel:
    
    """
        Example
        -------
            >>> data = np.array([
                    [1, 0.01301],
                    [3, 0.01325],
                    [5, 0.01415],
                    [10, 0.01600],
                    [20, 0.01625],
                    [30, 0.01604]
                ])

            >>> X_train = data[:, 0]
            >>> y_train = data[:, 1]

            >>> ns = NelsonSiegel()
            >>> ns.train(X_train, y_train)

            >>> maturity = np.linspace(0, 100, 1201)
            >>> spot_rate = ns.spot(maturity)
            >>> bond_price = ns.bond(maturity)
            >>> forward_rate = ns.forward(maturity)
    """
    
    def train(self, X, y):
        def obj_fun(lambda_):
            design_matrix = np.c_[np.ones_like(X), (1-np.exp(-lambda_*X))/(lambda_*X), (1-np.exp(-lambda_*X))/(lambda_*X)-np.exp(-lambda_*X)]
            beta = np.linalg.inv(design_matrix.T@design_matrix)@design_matrix.T@y
            error = np.sum((y-design_matrix@beta)**2)
            return error
        res = minimize_scalar(obj_fun, method='bounded', bounds=(1e-2,1), options={'disp':False})
        self.lambda_ = res.x
        design_matrix = np.c_[np.ones_like(X), (1-np.exp(-self.lambda_*X))/(self.lambda_*X), (1-np.exp(-self.lambda_*X))/(self.lambda_*X)-np.exp(-self.lambda_*X)]
        self.beta = np.linalg.inv(design_matrix.T@design_matrix)@design_matrix.T@y
    
    def spot(self, t):
        t = np.fmax(t, 1e-6)
        design_matrix = np.c_[np.ones_like(t), (1-np.exp(-self.lambda_*t))/(self.lambda_*t), (1-np.exp(-self.lambda_*t))/(self.lambda_*t)-np.exp(-self.lambda_*t)]
        return design_matrix@self.beta
    
    def bond(self, t):
        return (1+self.spot(t))**(-t)
    
    def forward(self, t):
        t = np.fmax(t, 1e-6)
        design_matrix = np.c_[np.ones_like(t), np.exp(-self.lambda_*t), self.lambda_*t*np.exp(-self.lambda_*t)]
        return design_matrix@self.beta
    
    
class DynamicNelsonSiegel:
    
    """
    Example
        -------
            >>> dt, maturity, data = dbesg.sample()
            >>> dns = DynamicNelsonSiegel(dt, maturity)
            >>> dns.train(data, disp=True)
            >>> time, num = 1, 200
            >>> scenarios = dns.sample(time, num)
            >>> mean_reversion, level1, level2, twist1, twist2 = dns.shock(time)
    """
    
    def __init__(self, dt, maturity):
        self.maturity = maturity
        self.dt = dt
        self.params = None
        self.x0 = None
        self.A = None
        self.B = None
        self.Q = None
        self.H = None
        self.R = None
    
    def train(self, X, lr=5e-7, tol=1.5e1, disp=False):
        if type(self.params) == type(None):
            self.params = self._initial_value(X)
        
        while(True):
            params_grad = self._gradient(self.params, X)
            self.params += lr*params_grad
            self.A, self.B, self.Q, self.H, self.R = self._system(self.params)
            self.x0 = self._filtering(self.params, X)[0]
            norm = np.sqrt(sum(params_grad**2))   
            if disp:
                loglik = self._filtering(self.params, X)[2]
#                 print('Norm of Gradient: {:.6f}, Loglikelihood: {:.6f}'.format(norm, loglik))
                print('|∇logL(Ψ)|: {:.6f}, logL(Ψ): {:.6f}'.format(norm, loglik))
            if norm < tol:
                break
    
    def _system(self, params):
        lambda_, eps, kappa11, kappa22, kappa33, theta1, theta2, theta3, sigma11, sigma21, sigma22, sigma31, sigma32, sigma33 = params
        expKdt = np.array([[np.exp(-kappa11*self.dt), 0, 0],
                          [0, np.exp(-kappa22*self.dt), 0],
                          [0, 0, np.exp(-kappa33*self.dt)]])
        A = expKdt
        B = (np.identity(3)-expKdt)@np.array([theta1, theta2, theta3])
        L = np.array([[sigma11, 0, 0],
                      [sigma21, sigma22, 0],
                      [sigma31, sigma32, sigma33]])
        kappa = np.array([kappa11, kappa22, kappa33])
        Q = (L@L.T)*1/(kappa[:, None]+kappa)*(1-np.exp(-(kappa[:, None]+kappa)*self.dt))
        H = np.c_[np.ones_like(self.maturity), (1-np.exp(-lambda_*self.maturity))/(lambda_*self.maturity), (1-np.exp(-lambda_*self.maturity))/(lambda_*self.maturity)-np.exp(-lambda_*self.maturity)]
        R = np.identity(len(self.maturity))*eps**2
        return A, B, Q, H, R
    
    def _initial_value(self, X):
        def obj_fun(lambda_):
            design_matrix = np.c_[np.ones_like(self.maturity), (1-np.exp(-lambda_*self.maturity))/(lambda_*self.maturity), (1-np.exp(-lambda_*self.maturity))/(lambda_*self.maturity)-np.exp(-lambda_*self.maturity)]
            beta = np.linalg.inv(design_matrix.T@design_matrix)@design_matrix.T@X.T
            rmse = np.sqrt(np.mean((X.T-design_matrix@beta)**2))
            return rmse
        res = minimize_scalar(obj_fun, method='bounded', bounds=(1e-2,1), options={'disp':False})
        lambda_ = res.x
        eps = obj_fun(lambda_)
        design_matrix = np.c_[np.ones_like(self.maturity), (1-np.exp(-lambda_*self.maturity))/(lambda_*self.maturity), (1-np.exp(-lambda_*self.maturity))/(lambda_*self.maturity)-np.exp(-lambda_*self.maturity)]
        beta = (np.linalg.inv(design_matrix.T@design_matrix)@design_matrix.T@X.T).T
        
        x, y = beta[:-1], beta[1:]
        beta1 = (np.mean(x**2, axis=0)*np.mean(y, axis=0)-np.mean(x, axis=0)*np.mean(x*y, axis=0))/(np.mean(x**2, axis=0)-np.mean(x, axis=0)**2)
        beta2 = (np.mean(x*y, axis=0)-np.mean(x, axis=0)*np.mean(y, axis=0))/(np.mean(x**2, axis=0)-np.mean(x, axis=0)**2)
        kappa = (1-beta2)/self.dt
        theta = beta1/kappa/self.dt
        e = y-(beta1+x*beta2)
        sigma = np.linalg.cholesky(e.T@e/(len(x)-3))/np.sqrt(self.dt)
        params_init = np.array([lambda_, eps, kappa[0], kappa[1], kappa[2], theta[0], theta[1], theta[2], sigma[0][0], sigma[1][0], sigma[1][1], sigma[2][0], sigma[2][1], sigma[2][2]])
        return params_init
    
    def _filtering(self, params, X):
        A, B, Q, H, R = self._system(params)
        
        x_update = np.array([0., 0.,  0.])
        P_update = np.identity(3)
        
        logL = 0
        for i in range(len(X)):
            # Predict
            x_pred = A@x_update+B
            P_pred = A@P_update@A.T+Q

            # Measurement
            z_meas = X[i]

            # Update
            z_pred = H@x_pred
            v = z_meas-z_pred
            F = H@P_pred@H.T+R
            F_inv = np.linalg.inv(F)
            detF = np.fmax(np.linalg.det(F), 1e-60)
            K = P_pred@H.T@F_inv
            x_update = x_pred+K@v
            P_update = P_pred-K@H@P_pred
            logL += -0.5*np.log(2*np.pi)-0.5*np.log(detF)-0.5*v.T@F_inv@v
            
        return x_update, P_update, logL
    
    def _init_delta(self):
        dA = np.zeros(shape=(3,3))
        dB = np.zeros(3)
        dQ = np.zeros(shape=(3,3))
        dR = np.zeros(shape=(len(self.maturity), len(self.maturity)))
        dH = np.zeros(shape=(len(self.maturity), 3))
        return dA, dB, dQ, dR, dH
    
    def _partial_deriv(self, params, deltas, X):
        A, B, Q, H, R = self._system(params)
        dA, dB, dQ, dH, dR = deltas
        
        x_update = np.zeros(3)
        P_update = np.identity(3)
        dx_update = np.zeros(3)
        dP_update = np.zeros(shape=(3,3))
        
#         logL = 0
        dlogL = 0
        for z_meas in X:
            ################ logL 연산 ###################
            x_prev = x_update
            P_prev = P_update

            # Predict
            x_pred = A@x_prev+B
            P_pred = A@P_prev@A.T+Q

            # Update
            z_pred = H@x_pred
            v = z_meas-z_pred
            F = H@P_pred@H.T+R
            F_inv = np.linalg.inv(F)
#             detF = np.linalg.det(F)

            K = P_pred@H.T@F_inv
            x_update = x_pred+K@v
            P_update = P_pred-K@H@P_pred
#             logL += -0.5*np.log(2*np.pi)-0.5*np.log(detF)-0.5*v.T@F_inv@v
            
            

            ################ dlogL 연산 ###################
            dx_prev = dx_update
            dP_prev = dP_update

            # Predict
            dx_pred = dA@x_prev + A@dx_prev + dB
            dP_pred = dA@P_prev@A.T + A@dP_prev@A.T + A@P_prev@dA.T + dQ

            # Update
            dz_pred = dH@x_pred + H@dx_pred
            dv = -dz_pred
            dF = dH@P_pred@H.T + H@dP_pred@H.T + H@P_pred@dH.T + dR
            dK = dP_pred@H.T@F_inv + P_pred@dH.T@F_inv - P_pred@H.T@(F_inv@dF@F_inv)
            dx_update = dx_pred + dK@v + K@dv
            dP_update = dP_pred - (dK@H@P_pred + K@dH@P_pred + K@H@dP_pred)
            dlogL += -0.5*np.trace(F_inv@dF)-0.5*(dv.T@F_inv@v - v.T@(F_inv@dF@F_inv)@v + v.T@F_inv@dv)
        
        return dlogL
    
    def _gradient(self, params, X):
        lambda_, eps, kappa11, kappa22, kappa33, theta1, theta2, theta3, sigma11, sigma21, sigma22, sigma31, sigma32, sigma33 = params
        A, B, Q, H, R = self._system(params)
        grad = np.zeros(14)
        
        # λ
        dA, dB, dQ, dR, dH = self._init_delta()
        dH = np.array([[0, np.exp(-lambda_*t)/lambda_-t*(1-np.exp(-lambda_*t))/(lambda_*t)**2, np.exp(-lambda_*t)/lambda_-t*(1-np.exp(-lambda_*t))/(lambda_*t)**2+t*np.exp(-lambda_*t)] for t in self.maturity])
        deltas = [dA, dB, dQ, dH, dR]
        grad[0] = self._partial_deriv(params, deltas, X)
        
        # ε
        dA, dB, dQ, dR, dH = self._init_delta()
        dR = 2*eps*np.identity(len(self.maturity))
        deltas = [dA, dB, dQ, dH, dR]
        grad[1] = self._partial_deriv(params, deltas, X)

        # κ11
        dA, dB, dQ, dR, dH = self._init_delta()
        dA[0][0] = -self.dt
        dB = theta1*self.dt*np.array([1, 0, 0])
        deltas = [dA, dB, dQ, dH, dR]
        grad[2] = self._partial_deriv(params, deltas, X)

        # κ22
        dA, dB, dQ, dR, dH = self._init_delta()
        dA[1][1] = -self.dt
        dB = theta2*self.dt*np.array([0, 1, 0])
        deltas = [dA, dB, dQ, dH, dR]
        grad[3] = self._partial_deriv(params, deltas, X)
        
        # κ33
        dA, dB, dQ, dR, dH = self._init_delta()
        dA[2][2] = -self.dt
        dB = theta3*self.dt*np.array([0, 0, 1])
        deltas = [dA, dB, dQ, dH, dR]
        grad[4] = self._partial_deriv(params, deltas, X)

        # θ1
        dA, dB, dQ, dR, dH = self._init_delta()
        dB = kappa11*self.dt*np.array([1, 0, 0])
        deltas = [dA, dB, dQ, dH, dR]
        grad[5] = self._partial_deriv(params, deltas, X)

        # θ2
        dA, dB, dQ, dR, dH = self._init_delta()
        dB = kappa22*self.dt*np.array([0, 1, 0])
        deltas = [dA, dB, dQ, dH, dR]
        grad[6] = self._partial_deriv(params, deltas, X)

        # θ3
        dA, dB, dQ, dR, dH = self._init_delta()
        dB = kappa33*self.dt*np.array([0, 0, 1])
        deltas = [dA, dB, dQ, dH, dR]
        grad[7] = self._partial_deriv(params, deltas, X)

        # σ11
        dA, dB, dQ, dR, dH = self._init_delta()
        dQ = np.array([
            [2*sigma11, sigma21, sigma31],
            [sigma21, 0, 0],
            [sigma31, 0, 0]
        ])
        deltas = [dA, dB, dQ, dH, dR]
        grad[8] = self._partial_deriv(params, deltas, X)
        
        # σ21
        dA, dB, dQ, dR, dH = self._init_delta()
        dQ = np.zeros(shape=(3,3))
        dQ = np.array([
            [0, sigma11, 0],
            [sigma11, 2*sigma21, sigma31],
            [0, sigma31, 0]
        ])
        deltas = [dA, dB, dQ, dH, dR]
        grad[9] = self._partial_deriv(params, deltas, X)

        # σ22
        dA, dB, dQ, dR, dH = self._init_delta()
        dQ = np.zeros(shape=(3,3))
        dQ = np.array([
            [0, 0, 0],
            [0, 2*sigma22, sigma32],
            [0, sigma32, 0]
        ])
        deltas = [dA, dB, dQ, dH, dR]
        grad[10] = self._partial_deriv(params, deltas, X)
        
        # σ31
        dA, dB, dQ, dR, dH = self._init_delta()
        dQ = np.zeros(shape=(3,3))
        dQ = np.array([
            [0, 0, sigma11],
            [0, 0, sigma21],
            [sigma11, sigma21, 2*sigma31]
        ])
        deltas = [dA, dB, dQ, dH, dR]
        grad[11] = self._partial_deriv(params, deltas, X)
        
        # σ32
        dA, dB, dQ, dR, dH = self._init_delta()
        dQ = np.zeros(shape=(3,3))
        dQ = np.array([
            [0, 0, 0],
            [0, 0, sigma22],
            [0, sigma22, 2*sigma32]
        ])
        deltas = [dA, dB, dQ, dH, dR]
        grad[12] = self._partial_deriv(params, deltas, X)

        # σ33
        dA, dB, dQ, dR, dH = self._init_delta()
        dQ = np.zeros(shape=(3,3))
        dQ = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 2*sigma33]
        ])
        deltas = [dA, dB, dQ, dH, dR]
        grad[13] = self._partial_deriv(params, deltas, X)
        
        return grad
    
    def predict(self, time):
        lambda_, eps, kappa11, kappa22, kappa33, theta1, theta2, theta3, sigma11, sigma21, sigma22, sigma31, sigma32, sigma33 = self.params
        H = np.c_[np.ones_like(self.maturity), (1-np.exp(-lambda_*self.maturity))/(lambda_*self.maturity), (1-np.exp(-lambda_*self.maturity))/(lambda_*self.maturity)-np.exp(-lambda_*self.maturity)]
        x_mean = (np.identity(3)-np.diag(np.exp(-np.array([kappa11, kappa22, kappa33])*time)))@(np.array([theta1, theta2, theta3]) - self.x0)
        z_mean = x_mean@H.T
        return x_mean, z_mean
    
    def sample(self, time, num, measurement_noise=False, random_seed=None):
        # dns.sample(1, 1, random_seed=0) bug 있음
        # (2020.04.13) measurement_noise = True 쓰지 말것 (오류여부 재확인 중)
        np.random.seed(random_seed)
        lambda_, eps, kappa11, kappa22, kappa33, theta1, theta2, theta3, sigma11, sigma21, sigma22, sigma31, sigma32, sigma33 = self.params
        L = np.array([[sigma11, 0, 0],
                      [sigma21, sigma22, 0],
                      [sigma31, sigma32, sigma33]])
        H = np.c_[np.ones_like(self.maturity), (1-np.exp(-lambda_*self.maturity))/(lambda_*self.maturity), (1-np.exp(-lambda_*self.maturity))/(lambda_*self.maturity)-np.exp(-lambda_*self.maturity)]
        R = np.identity(len(self.maturity))*eps**2
        x_mean, _ = self.predict(time)
        kappa = np.array([kappa11, kappa22, kappa33])
        x_cov = (L@L.T)*1/(kappa[:, None]+kappa)*(1-np.exp(-(kappa[:, None]+kappa)*time))
        x_rand = multivariate_normal.rvs(mean=x_mean, cov=x_cov, size=num)
        z_mean = x_rand@H.T
        if measurement_noise:
            z_rand = np.r_[[multivariate_normal.rvs(mean=z_mean[i], cov=R) for i in range(num)]]
        else:
            z_rand = np.r_[[multivariate_normal.rvs(mean=z_mean[i], cov=np.zeros_like(R)) for i in range(num)]]
        return z_rand
    
    def shock(self, time, significance=0.995):
        lambda_, eps, kappa11, kappa22, kappa33, theta1, theta2, theta3, sigma11, sigma21, sigma22, sigma31, sigma32, sigma33 = self.params
        L = np.array([[sigma11, 0, 0],
                      [sigma21, sigma22, 0],
                      [sigma31, sigma32, sigma33]])
        
        # 평균회귀 충격시나리오
        _, mean_reversion = self.predict(time)

        # M
        kappa = np.array([kappa11, kappa22, kappa33])
        M = np.linalg.cholesky((L@L.T)*1/(kappa[:, None]+kappa)*(1-np.exp(-(kappa[:, None]+kappa)*time)))

        # W
        LOT = 20
        a = sum([(1-np.exp(-lambda_*t))/(lambda_*t) for t in range(1, LOT+1)])
        b = sum([(1-np.exp(-lambda_*t))/(lambda_*t)-np.exp(-lambda_*t) for t in range(1, LOT+1)])
        W = np.diag([LOT, a, b])

        # N
        N = W@M
        V = N@N.T
        # Issue; eigenvector가 eigenvalue 크기 순으로 정렬되어 있는지 확인 필요
        (lambda3, lambda2, lambda1), e = np.linalg.eigh(V)
        e3, e2, e1 = e.T

        # 수준/기울기 충격시나리오
        H = np.c_[np.ones_like(self.maturity), (1-np.exp(-lambda_*self.maturity))/(lambda_*self.maturity), (1-np.exp(-lambda_*self.maturity))/(lambda_*self.maturity)-np.exp(-lambda_*self.maturity)]
        Hp = np.array([[1, (1-np.exp(-lambda_*t))/(lambda_*t), (1-np.exp(-lambda_*t))/(lambda_*t)-np.exp(-lambda_*t)] for t in range(1,LOT+1)])
        S1 = sum(Hp@M@e1)
        S2 = sum(Hp@M@e2)
        angle = np.arctan(S2/S1)
        level1 = H@(norm.ppf(significance)*(np.cos(angle)*M@e1 + np.sin(angle)*M@e2))
        level2 = H@(-norm.ppf(significance)*(np.cos(angle)*M@e1 + np.sin(angle)*M@e2))
        twist1 = H@(norm.ppf(significance)*(np.cos(angle)*M@e2 - np.sin(angle)*M@e1))
        twist2 = H@(-norm.ppf(significance)*(np.cos(angle)*M@e2 - np.sin(angle)*M@e1))
        
        return mean_reversion, level1, level2, twist1, twist2

    
class HullWhite:
    
    def __init__(self, curve: SmithWilson, alpha: List[float], sigma: List[float]):
        self.curve = curve
        self.ALPHA1, self.ALPHA2 = alpha
        self.SIGMA1, self.SIGMA2, self.SIGMA3, self.SIGMA4, self.SIGMA5, self.SIGMA6, self.SIGMA7 = sigma

    def alpha(self, t: float) -> float:
        if t<0: raise Exception("t 입력 오류")
        elif t<=20: value = self.ALPHA1
        else: value = self.ALPHA2
        return value

    def sigma(self, t: float) -> float:
        if t<0: raise Exception("t 입력 오류")
        elif t<=1: value = self.SIGMA1
        elif t<=2: value = self.SIGMA2
        elif t<=3: value = self.SIGMA3
        elif t<=5: value = self.SIGMA4
        elif t<=7: value = self.SIGMA5
        elif t<=10: value = self.SIGMA6
        else: value = self.SIGMA7
        return value
#         return 0

    def E(self, t: float) -> float:
        if t<0: raise Exception("t 입력 오류")
        elif t<=20: integral = self.ALPHA1*t 
        else: integral = self.ALPHA1*20+self.ALPHA2*(t-20)
        value = np.exp(integral)
        return value

    def B(self, t: float, T: float) -> float:
        if t<0 or T<t:
            raise Exception('(t, T) 입력 오류')
        elif t<=20 and T<=20:
            value = 1/self.ALPHA1*(1-np.exp(-self.ALPHA1*(T-t)))
        elif t<=20 and T>20:
            value = 1/self.ALPHA1*(1-np.exp(-self.ALPHA1*(20-t)))+1/self.ALPHA2*(np.exp(-self.ALPHA2*20)-np.exp(-self.ALPHA2*T))*np.exp(self.ALPHA1*t)
        elif t>20 and T>20:
            value = 1/self.ALPHA2*(1-np.exp(-self.ALPHA2*(T-t)))
        return value

    def theta(self, t: float) -> float:
        value = self.curve.forward(t, 1)+self.alpha(t)*self.curve.forward(t)+0.5*(self.deriv_V_0t(t, 2)+self.alpha(t)*self.deriv_V_0t(t, 1))
        # value = self.curve.forward(t, 1)+self.alpha(t)*self.curve.forward(t) # for test (사용 X)
        return value
    
    def deriv_V_0t(self, t: float, order: int) -> float:
        if order == 1:
            return 2/self.E(t)*quad(lambda u: self.sigma(u)**2*self.E(u)*self.B(u, t), 0, t, limit=200)[0]
        elif order == 2:
            return quad(lambda u: self.sigma(u)**2*self.E(u)/self.E(t)*(-self.alpha(t)*self.B(u, t)+self.E(u)/self.E(t)), 0, t, limit=200)[0]
        else:
            raise Exception("order 입력 오류")

    def generate_scenario(self, t: float, n: int, dt: float = 1/12):
        m = int(t/dt)
        r = np.zeros([m+1, n])
        r[0] = self.curve.forward(0)
        dW = np.random.normal(0, np.sqrt(dt), size=(m, n))
        t = np.arange(0, t+dt, dt)
        for i in range(m):
            r[i+1] = r[i] + (self.theta(t[i])-self.alpha(t[i])*r[i])*dt + self.sigma(t[i])*dW[i]
        return r