#### NAME : MANSI ARORA 
#### USER ID: marora33
#### GT ID: 903339702

import numpy as np
import random as rand

class QLearner(object):
    
    def author(self):
        return 'marora33'

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = True):

        self.verbose = verbose
        self.rar = rar
        self.radr = radr
        self.alpha = alpha
        self.gamma = gamma
        self.num_actions = num_actions
        self.num_states = num_states
        self.s = 0
        self.a = 0
        self.Q = np.zeros((num_states,num_actions), dtype=float)
        self.T = np.zeros((num_states, num_actions, num_states))
        #self.T[:,:,:] = 0.01
        self.R = np.zeros((num_states, num_actions))
        self.Tc = np.zeros((self.num_states, self.num_actions, self.num_states))
        self.Tc[:] = 0.0001
        self.dyna = dyna
        

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        if(rand.random() < self.rar):
            action = rand.randint(0, self.num_actions-1)
        else:
            #we have the experience tuple <self.s, self.a, s_prime, r>
            #use the Q table to take the next action
            action = np.argmax(self.Q[s])
             
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The reward you got in the previous state s when you took action a
        @returns: The selected action
        """
        if(rand.random() < self.rar):
            action = rand.randint(0, self.num_actions-1)
        else:
            #we have the experience tuple <self.s, self.a, s_prime, r>
            #use the Q table to take the next action
            #self.Q[self.s][self.a] = ((1-self.alpha)*self.Q[self.s][self.a]) + (self.alpha*(r + self.gamma*(self.Q[s_prime][np.argmax(self.Q[s_prime], axis = 0)])))
            self.Q[self.s,self.a] = (1-self.alpha)*self.Q[self.s,self.a] + self.alpha*(r + self.gamma*self.Q[s_prime, np.argmax(self.Q[s_prime])])
            action = np.argmax(self.Q[s_prime])
            
        self.rar = self.rar*self.radr
        
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        
        
        ############dyna#################
        
        
        self.Tc[self.s, self.a, s_prime]+=1
        self.T[self.s, self.a, s_prime] = self.Tc[self.s, self.a, s_prime]/self.Tc[self.s, self.a, :].sum()
        self.R[self.s, self.a] = ((1-self.alpha)*self.R[self.s, self.a]) + (self.alpha*r)
        
        for i in range(self.dyna):       
            rs = rand.randint(0,self.num_states-1)
            ra = rand.randint(0,self.num_actions-1)
            #rnum = rand.random()
            #cum=0
            #for j,i in enumerate(self.T[rs,ra,:]):
            #    cum+=i
            #    if cum > rnum:
            #        break
            #sp = j 
            
            #try:
            #    sp = min([i for i in (self.T[rs,ra,:].cumsum() > rnum).cumsum() if i!=0])
            #except:
            #    sp = self.num_states-1
            
            #try:
            #    sp=min(np.where(a)[0])
            #except:
            #    sp = self.num_states-1
            #sp = rand.randint(0,99)  
            
            sp = np.argmax(self.T[rs,ra])
            
            r = self.R[rs, ra]
            self.Q[rs,ra] = (1-self.alpha)*self.Q[rs,ra] + self.alpha*(r + self.gamma*self.Q[sp, np.argmax(self.Q[sp])])            
       
        self.a = action
        self.s = s_prime
        
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"

#num_states=100
#num_actions = 4
#alpha = 0.2
#gamma = 0.9
#rar = 0.5
#radr = 0.99
#dyna = 0
#verbose = False


