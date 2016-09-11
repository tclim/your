"""
This module contains functions that are used for kinematics
TODO (Jason): kinematics will be placed in robot base class later (??)
"""

import Rhino.Geometry as rg
import math

def forward_kinematics(base, dh_parameters):
    """
    Function that returns all the frames in a serial kinematic chain given DH_parameters
    
    Args:
        base: Plane. frame 0 
        dh_parameters: Tuple of (joint_distance, joint_angle, link_length, link_twist). This is the Denavit Hartenberg parameter table. 
    
    Returns:
        frames: A list of plane (frames)
    """
    
    _matrices_fk = [dh_matrix(dh[0], dh[1], dh[2], dh[3]) for dh in dh_parameters]
    
    #Set base frame
    frame_0 = rg.Plane.WorldXY
    frames_fk = [frame_0]
    _m = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, base)

    #Transform all frames
    for i in range(len(dh_parameters)):
        _p = rg.Plane(frame_0)
        _p.Transform(reduce(lambda x,y: x*y, (_matrices_fk[:i+1])))
        _p.Transform(_m)
        frames_fk.append(_p)
    
    return frames_fk[1:]

def inverse_kinematics(target, dhTable, right_hand = False, elbow_Up = False, wrist_up = False ):
    """
    Function that returns joint angles for the UR5 robot given a target place
    
    Args:
        target: Target plane. 
        dhTable: Tuple of (joint_distance, joint_angle, link_length, link_twist). This is the Denavit Hartenberg parameter table.
        right_hand: True to return right hand solution. Optional
        elbow_up: True to return elbow_up solution. Optional
        wrist_up: True to return writs up solution. Optional
    
    Returns:
        frames: A tuple of 6 joint angles
    """

    # 1 - Find Base
    frame5Target = rg.Plane(target)
    frame5Target.Translate(target.ZAxis * (-dhTable[5][0]))
    vOP = rg.Vector3d(frame5Target.OriginX, frame5Target.OriginY, 0)
    r = dhTable[3][0]
    d = vOP.Length
    if (abs(r/d) > 1):
        print "Target plane is to close to robot base (< 0.10915m). Math domain error"
        return None
    angleTOP = math.acos(r / d)
    vOT = rg.Vector3d(vOP)
    vOT *= (r / vOT.Length)
    if (right_hand):
      vOT.Rotate(-angleTOP, rg.Vector3d.ZAxis)
    else:
      vOT.Rotate(angleTOP, rg.Vector3d.ZAxis)
    j0 = signed_angle(rg.Vector3d.YAxis, -vOT, rg.Vector3d.ZAxis)

    # 3 - Find shoulder (frame 1)
    m01 = dh_matrix(dhTable[0][0], dhTable[0][1] + j0, dhTable[0][2], dhTable[0][3])
    frame1 = rg.Plane(rg.Plane.WorldXY)
    frame1.Transform(m01)

    # 4 - Find wrist 2 (frame 4)
    frame1Offset = rg.Plane(frame1)
    xF1F5Target = rg.Intersect.Intersection.PlanePlane(frame1, frame5Target)[1]
    vFrame4z = xF1F5Target.Direction
    vFrame4z.Unitize()
    if (vFrame4z.IsTiny(0.00001)):
      vFrame4z.X = vFrame4z.Y = 0
      vFrame4z.Z = 1
    if (wrist_up and vFrame4z.Z < 0):
        vFrame4z.Reverse()
    elif (not wrist_up and vFrame4z.Z > 0):
        vFrame4z.Reverse()

    vFrame4z *= dhTable[4][0]
    vOF4 = rg.Vector3d(frame5Target.Origin + vFrame4z)
    vOF4 -= (frame1.Normal * dhTable[3][0])  #align in same plane as frame 1

    # 5 - Circle circle intersection
    cirFrame1 = rg.Circle(frame1Offset, dhTable[1][2]) # ok to use negative value?
    cirFrame4 = rg.Circle(rg.Plane(rg.Point3d(vOF4), frame1Offset.XAxis, frame1Offset.YAxis), dhTable[2][2])
    xPts = cir_cir_intersection(cirFrame1, cirFrame4)

    if (xPts is None):
        print "Circle circle intersection failed"
        return None

    if (xPts[0].Z < xPts[1].Z): 
        xPts.reverse()
    frame2Origin = xPts[0] if elbow_up else xPts[1] # selct base on elbow choice

    # 6 - Find j1 and elbow (frame 2)
    vF1F2 = rg.Vector3d(frame2Origin - frame1.Origin)
    vF1F2.Unitize()
    j1 = signed_angle(-frame1.XAxis, vF1F2, frame1.Normal)
    m12 = dh_matrix(dhTable[1][0], dhTable[1][1] + j1, dhTable[1][2], dhTable[1][3])
    frame2 = rg.Plane(rg.Plane.WorldXY)
    frame2.Transform(m01 * m12)

    # 7 - Find j2 and wrist1 (frame 3)
    vOF2 = rg.Vector3d(frame2.Origin)
    vF2F4 = vOF4 - vOF2
    vF2F4.Unitize()
    j2 = signed_angle(-frame2.XAxis, vF2F4, frame2.Normal)
    m23 = dh_matrix(dhTable[2][0], dhTable[2][1] + j2, dhTable[2][2], dhTable[2][3])
    frame3 = rg.Plane(rg.Plane.WorldXY)
    frame3.Transform(m01 * m12 * m23)

    #8 - Find j3 and wrist 2 (frame4)
    j3 = signed_angle(-frame3.YAxis, -vFrame4z, frame3.Normal)
    m34 = dh_matrix(dhTable[3][0], dhTable[3][1] + j3, dhTable[3][2], dhTable[3][3])
    frame4 = rg.Plane(rg.Plane.WorldXY)
    frame4.Transform(m01 * m12 * m23 * m34)

    #9 - Find j4 and wrist 3 (frame 5)
    j4 = signed_angle(frame4.YAxis, target.Normal, frame4.Normal)
    m45 = dh_matrix(dhTable[4][0], dhTable[4][1] + j4, dhTable[4][2], dhTable[4][3])
    frame5 = rg.Plane(rg.Plane.WorldXY)
    frame5.Transform(m01 * m12 * m23 * m34 * m45)

    #10 - Find j5
    j5 = signed_angle(frame5.YAxis, target.YAxis, frame5.Normal)

    return (j0,j1,j2,j3,j4,j5)

def dh_matrix(d, theta, r, alpha):
    """Returns Denavit Hartenberg transformation matrix 
    
    Arguments:
        d - Joint distance. in mm
        theta- joint angle. in radians
        r- link length. in mm
        alpha- twist angle around common normal. in radians
    
    Returns:
        m: Denavit Hartenberg transformation matrix
    """
    
    _matrix = [(math.cos(theta), -math.sin(theta) * math.cos(alpha),math.sin(theta) * math.sin(alpha), r * math.cos(theta)),
               (math.sin(theta), math.cos(theta) * math.cos(alpha), -math.cos(theta) * math.sin(alpha), r * math.sin(theta)),
               (0, math.sin(alpha),math.cos(alpha),d),
               (0,0,0,1)]
    
    m = rg.Transform()
    for i in range(4):
        for j in range(4):
            m[i,j] = _matrix[i][j]
            
    return m

