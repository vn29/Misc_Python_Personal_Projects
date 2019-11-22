import numpy as np
from scipy import linalg
import math
import pandas as pd

inch = 1.
lb = 1.
kip = 1000.*lb
ft = inch*12.
ksi = kip/(inch**2)
psi = lb/(inch**2)
klf = kip/(ft)
plf = lb/(ft)

class StructModel(object):
  def __init__(self):
    self.node_df = pd.DataFrame( columns = ['x','y','z','Fx','Fy','Mz','Rx','Ry','Rz'])
    self.line_df = pd.DataFrame( columns = ['i','j','ux','uy','uz','rx','ry','rz','MatProp','SecProp','Alpha','Length','E','A','I'])
    self.matprop_df = pd.DataFrame(columns = ['name','fpc','fy','fu','E','selfWeightPerVol'])
    self.secprop_df = pd.DataFrame(columns = ['matprop','Area','rx','ry','Ix','Iy','Sx','Sy','Zx','Zy'])
    
  def AddNode(self,node_index,coord_xyz):
    if node_index not in self.node_df.index:
        self.node_df.loc[node_index,['x','y','z',
                                   'Fx','Fy','Mz',
                                   'Rx','Ry','Rz']] = [coord_xyz[0],coord_xyz[1],coord_xyz[2],
                                                                 0.,0.,0.,
                                                                 0,0,0]
    else:
        print("duplicate node exists for node:"+str(node_index))
    
  def AddForce(self,node_index,force_xyz):
    if node_index in self.node_df.index:
      self.node_df.loc[node_index,['Fx','Fy','Mz']] = [force_xyz[0],force_xyz[1],force_xyz[2]]
    else:
      print("node" + str(node_index) + "does not exist")
  
  def AddBoundary(self,node_index,bound_xyz):
    if node_index in self.node_df.index:
      self.node_df.loc[node_index,['Rx','Ry','Rz']] = [bound_xyz[0],bound_xyz[1],bound_xyz[2]]
    else:
      print("node" + str(node_index) + "does not exist")
  
  def AddLine(self,line_index,ij_tup):
    if line_index not in self.line_df.index:
      self.line_df.loc[line_index,['i','j']] = [ij_tup[0],ij_tup[1]]
      i_tup = self.node_df.loc[ij_tup[0],['x','y','z']]
      j_tup = self.node_df.loc[ij_tup[1],['x','y','z']]
      dx = -i_tup[0]+j_tup[0]
      dy = -i_tup[1]+j_tup[1]
      self.line_df.loc[line_index,'Length'] = ((dx)**(2)+(dy)**(2))**(0.5)
      self.line_df.loc[line_index,'Alpha'] = math.atan(dy/(dx+0.00000000001*self.line_df.loc[line_index,'Length']))
      self.line_df.loc[line_index,['ux','uy','uz','rx','ry','rz']] = [1,1,1,1,1,1]
    else:
      print("duplicate line exists for line:"+str(line_index))
   
  
  def SetEAI(self,line_index,E,A,I):
    if line_index in self.line_df.index:
      self.line_df.loc[line_index,['E','A','I']] = [E,A,I]
      
    else:
      print("line"+str(line_index)+"does not exist")
      
    
    
  def DelNode(self,node_index):
    if node_index in self.node_df.index:
      self.node_df = self.node_df.drop([node_index])
    else:
      "no node exists. "+str(node_index)+" has not been dropped"
  def DelLine(self,line_index):
    if line_index in self.line_df.index:
      self.line_df = self.line_df.drop([line_index])
    else:
      "no line exists. "+str(line_index)+" has not been dropped"
  def ldl_decomp(self,A):
    #A = np.matrix(A)
    if not (A.H == A).all():
      print("A must be Hermitian!")
      return None, None
    else:
        S = np.diag(np.diag(A))
        Sinv = np.diag(1/np.diag(A))
        D = np.matrix(S.dot(S))
        Lch = np.linalg.cholesky(A)
        L = np.matrix(Lch.dot(Sinv))
    return L, D

  def solver(self,k):
    F = self.GenFvec()
    Low,D =self.ldl_decomp(k)
    y = Low**(-1)*F
    j = D*Low.T
    d=j**(-1)*y
    return d

  def rotater(self,theta,k):
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.matrix([[c ,-s ,0.,0.,0. ,0.],
                   [s ,c  ,0.,0.,0. ,0.],
                   [0.,0. ,1.,0.,0. ,0.],
                   [0.,0. ,0.,c ,-s ,0.],
                   [0.,0. ,0.,s ,c  ,0.],
                   [0.,0. ,0.,0.,0. ,1.]])
    k_rotated = R.T*k*R
    return k_rotated

  def mkboundary(self,k_matrix,DOF_list):
    for e in DOF_list:
      col = e
      row = e
      m = k_matrix.shape[0]
      k_matrix[:,col]=np.zeros((m,1))
      k_matrix[row,:]=np.zeros((1,m))
      k_matrix[row,col]=1.
    return k_matrix
     
    
  def GenEK(self,E,A,I,L):
    k_list = [[E*A/L ,0.         ,0.         ,-E*A/L,0.          ,0.         ],
              [0.    ,12*E*I/L**3,-6*E*I/L**2,0.    ,-12*E*I/L**3,-6*E*I/L**2],
              [0.    ,-6*E*I/L**2,4*E*I/L    ,0.    ,6*E*I/L**2  ,2*E*I/L    ],
              [-E*A/L,0.         ,0.         ,E*A/L ,0.          ,0.         ],
              [0.,-12*E*I/L**3   ,6*E*I/L**2 ,0.    ,12*E*I/L**3 ,6*E*I/L**2 ],
              [0.,-6*E*I/L**2    ,2*E*I/L    ,0.    ,6*E*I/L**2  ,4*E*I/L    ]]
    k_matrix_elem = np.matrix(k_list)
    return k_matrix_elem
    
  
  def GlobalStiff(self): #will assign as k_matrix_eme(e) at for loop which will then look up the correct properties from the dataframe
    
    NodesCount = self.node_df.shape[0]
    LinesCount = self.line_df.shape[0]
    K = np.matrix(np.zeros((NodesCount*3,NodesCount*3)))
    
    for e in range(LinesCount):
      i = self.line_df['i'].iloc[e]
      j = self.line_df['j'].iloc[e]
      theta = self.line_df['Alpha'].iloc[e]
      
      E = self.line_df['E'].iloc[e]
      A = self.line_df['A'].iloc[e]
      I = self.line_df['I'].iloc[e]
      L = self.line_df['Length'].iloc[e]
      k_matrix_elem = self.GenEK(E,A,I,L)
      #here is where I plan to add the element stiffness matrix generation so that properties can vary from member to member
      k_matrix = self.rotater(theta, k_matrix_elem)
    
      k_matrix_part = [
          k_matrix[:3,:3],
          k_matrix[:3,3:],
          k_matrix[3:,:3],
          k_matrix[3:,3:]
          ] 
      
      K[3*i:3*i+3,3*i:3*i+3] = K[3*i:3*i+3,3*i:3*i+3] + k_matrix_part[0]
      K[3*i:3*i+3,3*j:3*j+3] = K[3*i:3*i+3,3*j:3*j+3] + k_matrix_part[1]
      K[3*j:3*j+3,3*i:3*i+3] = K[3*j:3*j+3,3*i:3*i+3] + k_matrix_part[2]
      K[3*j:3*j+3,3*j:3*j+3] = K[3*j:3*j+3,3*j:3*j+3] + k_matrix_part[3]
    return K
  
  def GenFvec(self):
    return np.matrix(self.node_df.loc[:,['Fx','Fy','Mz']].stack()).reshape((self.node_df.shape[0]*3,1))
  #this is a courtesy function for now
  
  def getbound(self):
    bndlist = []
    for e in self.node_df.index:
      if self.node_df.loc[e,'Rx'] == 1:
        bndlist.append(3*e*self.node_df.loc[e,'Rx'])
      if self.node_df.loc[e,'Ry'] == 1:
        bndlist.append(3*e*self.node_df.loc[e,'Ry']+1)
      if self.node_df.loc[e,'Rz'] == 1:
        bndlist.append(3*e*self.node_df.loc[e,'Rz']+2)
    return bndlist
  
  def recoverReactions(self,d):
    #get the stiffness matrix and assign an index and column index to it
    m_size = self.GlobalStiff().shape[0]
    unbnd_nodes = set(range(m_size)) - set(om.getbound())
    K_gl = pd.DataFrame(self.GlobalStiff(), index=range(m_size) , columns =range(m_size))
    K_bb = K_gl.loc[self.getbound(),self.getbound()]
    K_aa = K_gl.loc[list(unbnd_nodes),list(unbnd_nodes)]
    K_ba = K_gl.loc[list(bnd_nodes),list(unbnd_nodes)]
    #mathematical operation to recover the reactions vector
    Rr = K_ba.values*d[list(unbnd_nodes)]+K_bb.values*d[list(bnd_nodes)]
    
    return Rr,list(bnd_nodes)
    
   

  
#generate object model dataframe
om = StructModel()
#add nodes
om.AddNode(0,(0.,0.,0.))
om.AddNode(1,(0.,10.,0.))
om.AddNode(2,(10.,10.,0.))
om.AddNode(3,(10.,0.,0.))

#add frame members
om.AddLine(0,(0,1))
om.AddLine(1,(1,2))
om.AddLine(2,(2,3))
om.SetEAI(0,29000.*ksi,100.*inch**2,I = 20.*inch**4)
om.SetEAI(1,29000.*ksi,10.*inch**2,I = 10.*inch**4)
om.SetEAI(2,29000.*ksi,10.*inch**2,I = 20.*inch**4)

#add forces
om.AddForce(1,(1.*kip,0.*kip,0.*kip*ft))
om.AddForce(2,(1.*kip,0.*kip,0.*kip*ft))
#add boundary conditions (x res, y res, rotational res)
om.AddBoundary(0,(1,1,1))
om.AddBoundary(3,(1,1,1))
#generate the global stiffness matrix
K = om.mkboundary(om.GlobalStiff(),om.getbound())
#solve for displacements
d= om.solver(K)
#solve for reactions
om.recoverReactions(d)
