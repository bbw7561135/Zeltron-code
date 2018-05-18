#***********************************************************************!
#                       The Zeltron code project.                       !
#***********************************************************************!
# Copyright (C) 2012-2015. Authors: Benoit Cerutti & Greg Werner        !
#                                                                       !
# This program is free software: you can redistribute it and/or modify  !
# it under the terms of the GNU General Public License as published by  !
# the Free Software Foundation, either version 3 of the License, or     !
# (at your option) any later version.                                   !
#                                                                       !
# This program is distributed in the hope that it will be useful,       !
# but WITHOUT ANY WARRANTY; without even the implied warranty of        !
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         !
# GNU General Public License for more details.                          !
#                                                                       !
# You should have received a copy of the GNU General Public License     !
# along with this program. If not, see <http://www.gnu.org/licenses/>.  !
#***********************************************************************!
#
# This python script will draw any component of the total current density
# or the total charge density in 3D (isosurfaces) as function of x, y, z, 
# at a given time step it.
#
# To execute, type for instance:$ python plot3D_current.py 0 Jz &
# This command will draw the strength of Jz at time step 0.
#
# Notice: You need the Mayavi library to run this script
#***********************************************************************!

import numpy
import math
from mayavi.mlab import *
from mayavi import mlab
import sys

def plot3D_current(it,current):

    if it=='':
       it='0'

    if current=='':
       current='Jx'

    #===============================================================================
    # Parameters of the simulation

    params1=numpy.loadtxt(".././Zeltron3D/data/phys_params.dat",skiprows=1)
    params2=numpy.loadtxt(".././Zeltron3D/data/input_params.dat",skiprows=1)

    # Nominal cyclotron frequency
    rho=2.9979246e+10/params1[3]
    
    #===============================================================================
    # The grid
    x=numpy.loadtxt(".././Zeltron3D/data/xfield.dat")
    y=numpy.loadtxt(".././Zeltron3D/data/yfield.dat")
    z=numpy.loadtxt(".././Zeltron3D/data/zfield.dat")
   
    # The current
    rhoJe=numpy.loadtxt(".././Zeltron3D/data/currents/"+current+"_electrons"+it+".dat")
    rhoJi=numpy.loadtxt(".././Zeltron3D/data/currents/"+current+"_ions"+it+".dat")

    nx=len(x)
    ny=len(y)
    nz=len(z)

    dx,ptx=x[1]-x[0],nx*1j
    dy,pty=y[1]-y[0],ny*1j
    dz,ptz=z[1]-z[0],nz*1j

    x,y,z=numpy.ogrid[-dx:dx:ptx,-dy:dy:pty,-dz:dz:ptz]

    mapxyz=numpy.empty((nx,ny,nz))

    for ix in range(0,nx):
        for iy in range(0,ny):
            for iz in range(0,nz):   
                mapxyz[ix,iy,iz]=rhoJe[iy+iz*ny,ix]+rhoJi[iy+iz*ny,ix]
         
    contour3d(mapxyz,contours=10,transparent=True,opacity=0.9)
    mlab.outline()
    mlab.colorbar(title=current,orientation='vertical',nb_labels=10)
    mlab.axes()
    mlab.title("Time="+it+", "+current)
    
    #===============================================================================

    mlab.show()
    
    #===============================================================================

plot3D_current(sys.argv[1],sys.argv[2])
