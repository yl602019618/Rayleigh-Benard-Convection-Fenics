import gym
from gym import spaces
from gym.utils import seeding
from gym import error, utils
import numpy as np
from os import path
import math

import torch
import random
import math
import torch.nn as nn

from rbc_adjoint_tools import *
import time

class RBC():
    def __init__(self, params=None):

        self.set_params(params)
        self.geometry = MyGeometry(min_x = self.params['min_x'], max_x =self.params['max_x'] , min_y = self.params['min_y'],max_y = self.params['max_y'])
        # default is [0,3,0,1]
        self.function_space = MyFunctionSpace(self.geometry, )
        self.solver = MySolver(self.geometry, self.function_space, params={'T': self.params['T'] ,'dt': self.params['dt'],'dimx':self.params['dimx'],'dimy':self.params['dimy'],'Ra' :self.params['Ra'] })
        self.geometry.generate()
        self.function_space.generate()
        self.solver.generate_variable()
        # self.solver.generate_bc()
        # self.solver.generate_solver()
        self.solver.generate_grid()
        # self.solver.solve()


        self.current_t = self.solver.time 
        
    def set_params(self, params =None):
        if params is not None:
            self.params = params
        else:
            self.params = {'dt':  0.125,
                            'T':  0.125*130,
                            'dimx': 32*2+1,
                            'dimy': 33,
                            'min_x' : 0, 
                            'max_x' : 2.0, 
                            'min_y' : 0.0, 
                            'max_y' : 1.0 ,'Ra':2E6
                                    }
        
    def reset(self):
        self.solver.init_solve()
        print('init now')
        print('init now')
        print('init now')
        print('init now')
        print('init now')
        print('init now')
        print('init now')
        print('init now')
        print('init now')
        print('init now')
        print('init now')
        print('init now')
        print('init now')
        print('init now')

    def step(self):        
        temp , velo , p ,a1 , b1= self.solver.step_forward()
        #self.solver.plot_all()
        episode_over = self._get_done()
        
        return temp , velo , p , episode_over, a1 , b1
    
    def adjoint_forward(self,w_tn, w_tnp1,a1,b1):
        grad_wn,grad_wnp1,J=self.solver.RBC_step(w_tn, w_tnp1,a1,b1)
        return grad_wn,grad_wnp1,J

    def forward(self,w_tn,w_tnp1,a1,b1):
        return self.solver.forward(w_tn,w_tnp1,a1,b1)
    def backward(self,w_tn,w_tnp1,a1,b1):
        return self.solver.backward(w_tn,w_tnp1,a1,b1)

        
 
    def _get_done(self):
        return self.solver.time > self.solver.T
        # return self.env.getDown()
    def _close(self):
        return None

    def get_value(self):
        obs = self.solver.get_value()
        return obs 
