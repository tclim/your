"""
This module contains utility functions:
    1) Transformation functions
    2) Useful geometry functions e.g. Intersections
"""

import Rhino.Geometry as rg
import math

# ----- Coordinate System conversions -----

def matrix_to_axis_angle(m):
    """
    Function that transforms a 4x4 matrix to axis-angle format
    referenced from Martin Baker's www.euclideanspace.com
    
    Args:
        m: Rhino.Geometry Transform structure  - 4x4 matrix
    
    Returns:
        axis: Rhino.Geometry Vector3d object - axis-angle notation
    """
    
    epsilon = 0.01
    epsilon2 = 0.01
    
    if (math.fabs(m.M01 - m.M10) < epsilon) & (math.fabs(m.M02 - m.M20) < epsilon) & (math.fabs(m.M12 - m.M21) < epsilon):
    #singularity found
    #first check for identity matrix which must have +1 for all terms
    #in leading diagonal and zero in other terms
        if (math.fabs(m.M01 + m.M10) < epsilon2) & (math.fabs(m.M02 + m.M20) < epsilon2) & (math.fabs(m.M12 + m.M21) < epsilon2) & (math.fabs(m.M00 + m.M11 + m.M22 - 3) < epsilon2):
            #this singularity is identity matrix so angle = 0   make zero angle, arbitrary axis
            angle = 0
            x = 1
            y = z = 0
        else:
            # otherwise this singularity is angle = 180
            angle = math.pi;
            xx = (m.M00 + 1) / 2
            yy = (m.M11 + 1) / 2
            zz = (m.M22 + 1) / 2
            xy = (m.M01 + m.M10) / 4
            xz = (m.M02 + m.M20) / 4
            yz = (m.M12 + m.M21) / 4
            if ((xx > yy) & (xx > zz)):
                # m.M00 is the largest diagonal term
                if (xx < epsilon):
                    x = 0
                    y = z = 0.7071
                else:
                    x = math.sqrt(xx)
                    y = xy / x
                    z = xz / x
            elif (yy > zz): 
                # m.M11 is the largest diagonal term
                if (yy < epsilon):
                    x = z = 0.7071
                    y = 0
                else: 
                    y = math.sqrt(yy)
                    x = xy / y
                    z = yz / y
            else: 
                # m.M22 is the largest diagonal term so base result on this
                if (zz < epsilon):
                    x = y = 0.7071
                    z = 0
                else:
                    z = math.sqrt(zz)
                    x = xz / z
                    y = yz / z
    else:
        s = math.sqrt((m.M21 - m.M12) * (m.M21 - m.M12)+ (m.M02 - m.M20) * (m.M02 - m.M20)+ (m.M10 - m.M01) * (m.M10 - m.M01)); # used to normalise
        if (math.fabs(s) < 0.001):
            #prevent divide by zero, should not happen if matrix is orthogonal and should be
            s = 1
        angle = math.acos((m.M00 + m.M11 + m.M22 - 1) / 2)
        x = (m.M21 - m.M12) / s
        y = (m.M02 - m.M20) / s
        z = (m.M10 - m.M01) / s
    angleRad = angle
    axis = rg.Vector3d(x,y,z)
    axis = axis*angleRad
    
    return axis

def matrix_to_euler(m):
    """Returns Euler rotation angles from a transformation matrix
    
    Based on Gregory Slabaugh method
    Args:
        m = Transform object
    Returns:
        tuple of euler angles in radians
    """
    
    if (abs(m.M20) != 1): 
        # Non-degenerate case
        # Find rotation Y
        rY1 = -math.asin(m.M20)
        rY2 = math.pi - rY1
        
        # Find rotation X
        rX1 = math.atan2(m.M21/math.cos(rY1), m.M22/math.cos(rY1))
        rX2 = math.atan2(m.M21/math.cos(rY2), m.M22/math.cos(rY2))
        
        # Find rotation Z
        rZ1 = math.atan2(m.M10/math.cos(rY1), m.M00/math.cos(rY1))
        rZ2 = math.atan2(m.M10/math.cos(rY2), m.M00/math.cos(rY2))
        return ((rX1, rY1, rZ1), (rX2, rY2, rZ2))
    else:
        #Degenerate case
        rotZ = 0 #arbitrary
        if (m.M20 < 0):
            rotY = math.pi/2
            rotX = rotZ + math.atan2(m.M01, m.M02)
        else:
            rotY = -math.pi/2
            rotX = -rotZ + math.atan2(-m.M01, -m.M02)
        return (rotX, rotY, rotZ)

# ----- Matrix related helper functions

def concatenate_matrices(matrices):
    """
    This function creates a concatenated matrix from a list of matrices
    
    Arguments:
        matrices: A list of tranformation matrices
    
    Returns:
        _transform: Concatenated matrix
    """
    _transform = matrices[0]
    for i in range(1,len(matrices)):
        _transform *= matrices[i]
    return _transform

# ----- Miscellaneous geometry helper functions

def signed_angle(v1,v2,v_normal):
    """
    This function gets the angle between 2 vectors -pi < theta< pi
    
    Arguments:
        v1: Vector3d. First unitized vector
        v2: Vector3d. Second unitized vector
        v_normal: Vector3d. Normal to 2 vectors that determines what is positive/negative
    
    Returns:
        theta: float. signed angle between -pi and pi
    """
    # from 0 to pi
    c = rg.Vector3d.Multiply(v1,v2)
    n = rg.Vector3d.CrossProduct(v1,v2)
    s= n.Length
    
    theta  = math.atan2(s,c)
    
    if (rg.Vector3d.Multiply(n, v_normal) < 0):
        theta *= -1
    return theta

def cir_cir_intersection(cir1,cir2):
    """
    Funtion that returns the intersection points between two circles
    
    Arguments:
        1) cir1: First circle
        2) cir2: Second Circle
    
    Returns:
        xpts: list of 2 Point3d objectts
        
    Note that there is no error checking
    """
    r1 = cir1.Radius
    r2 = cir2.Radius
    d = cir1.Center.DistanceTo(cir2.Center)
    
    a = (r1 **2 - r2**2 + d**2)/(2*d)
    h = math.sqrt(r1 **2 - a **2 )
    
    v_c1 = rg.Vector3d(cir1.Center)
    v_c2 = rg.Vector3d(cir2.Center)
    
    v_c1c2 = v_c2 - v_c1
    v_c1c2.Unitize()
    v_c1c2 *= a
    
    v_pt0 = v_c1 + v_c1c2
    
    v_pt0ptX = rg.Vector3d.CrossProduct(cir1.Normal,v_c1c2)
    v_pt0ptX.Unitize()
    v_pt0ptX *= h
    
    xpt1 = rg.Point3d(v_pt0 + v_pt0ptX)
    v_pt0ptX.Reverse()
    xpt2 = rg.Point3d(v_pt0 + v_pt0ptX)

    return [xpt1,xpt2]

def check_arguments(function):
    def decorated(*args):
        if None in args:
            raise TypeError("Invalid Argument")
        return function(*args)
    return decorated