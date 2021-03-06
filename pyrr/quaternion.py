# -*- coding: utf-8 -*-
"""Provide functions for the creation and manipulation of Quaternions.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import math

import numpy

from pyrr import vector, vector3, vector4


class index:
    #: The index of the X value within the quaternion
    x = 0

    #: The index of the Y value within the quaternion
    y = 1

    #: The index of the Z value within the quaternion
    z = 2

    #: The index of the W value within the quaternion
    w = 3


def create( x, y, z, w ):
    return numpy.array( [ x, y, z, w ], dtype = float )

def create_identity():
    return vector4.create_identity()

def create_from_x_rotation( theta ):
    thetaOver2 = theta * 0.5

    return numpy.array(
        [
            # x
            math.sin( thetaOver2 ),
            # y
            0.0,
            # z
            0.0,
            # w
            math.cos( thetaOver2 )
            ]
        )

def create_from_y_rotation( theta ):
    thetaOver2 = theta * 0.5

    return numpy.array(
        [
            # x
            0.0,
            # y
            math.sin( thetaOver2 ),
            # z
            0.0,
            # w
            math.cos( thetaOver2 )
            ]
        )

def create_from_z_rotation( theta ):
    thetaOver2 = theta * 0.5

    return numpy.array(
        [
            # x
            0.0,
            # y
            0.0,
            # z
            math.sin( thetaOver2 ),
            # w
            math.cos( thetaOver2 )
            ]
        )

def create_from_axis_rotation( axis, theta ):
    # make sure the vector is normalised
    assert (numpy.linalg.norm( axis, ord = None ) - 1.0) < 0.01
    
    thetaOver2 = theta * 0.5
    sinThetaOver2 = math.sin( thetaOver2 )
    
    return numpy.array(
        [
            # x
            axis[ 0 ] * sinThetaOver2,
            # y
            axis[ 1 ] * sinThetaOver2,
            # z
            axis[ 2 ] * sinThetaOver2,
            # w
            math.cos( thetaOver2 )
            ]
        )

def create_from_eulers( eulers ):
    """Creates a quaternion from a set of Euler angles.

    Eulers are an array of length 3 in the following order::
        [ yaw, pitch, roll ]
    """
    halfYaw = eulers[ 0 ] * 0.5
    sinYaw = math.sin( halfYaw )
    cosYaw = math.cos( halfYaw )

    halfPitch = eulers[ 1 ] * 0.5
    sinPitch = math.sin( halfPitch )
    cosPitch = math.cos( halfPitch )

    halfRoll = eulers[ 2 ] * 0.5
    sinRoll = math.sin( halfRoll )
    cosRoll = math.cos( halfRoll )
    
    return numpy.array(
        [
            # x = -cy * sp * cr - sy * cp * sr
            (-cosYaw * sinPitch * cosRoll) - (sinYaw * cosPitch * sinRoll),
            # y = cy * sp * sr - sy * cp * cr
            (cosYaw * sinPitch * sinRoll) - (sinYaw * cosPitch * cosRoll),
            # z = sy * sp * cr - cy * cp * sr
            (sinYaw * sinPitch * cosRoll) - (cosYaw * cosPitch * sinRoll),
            # w = cy * cp * cr + sy * sp * sr
            (cosYaw * cosPitch * cosRoll) + (sinYaw * sinPitch * sinRoll) 
            ]
        )

def create_from_inverse_of_eulers( eulers ):
    """Creates a quaternion from the inverse of a set of Euler angles.

    Eulers are an array of length 3 in the following order::
        [ yaw, pitch, roll ]
    """
    halfYaw = eulers[ 0 ] * 0.5
    sinYaw = math.sin( halfYaw )
    cosYaw = math.cos( halfYaw )

    halfPitch = eulers[ 1 ] * 0.5
    sinPitch = math.sin( halfPitch )
    cosPitch = math.cos( halfPitch )
    
    halfRoll = eulers[ 2 ] * 0.5
    sinRoll = math.sin( halfRoll )
    cosRoll = math.cos( halfRoll )
    
    return numpy.array(
        [
            # x = cy * sp * cr + sy * cp * sr
            (cosYaw * sinPitch * cosRoll) + (sinYaw * cosPitch * sinRoll),
            # y = -cy * sp * sr + sy * cp * cr
            (-cosYaw * sinPitch * sinRoll) + (sinYaw * cosPitch * cosRoll),
            # z = -sy * sp * cr + cy * cp * sr
            (-sinYaw * sinPitch * cosRoll) + (cosYaw * cosPitch * sinRoll),
            # w = cy * cp * cr + sy * sp * sr
            (cosYaw * cosPitch * cosRoll) + (sinYaw * sinPitch * sinRoll)
            ]
        )

def cross( quat1, quat2 ):
    """Returns the cross-product of the two quaternions.

    Quaternions are **not** communicative. Therefore, order is important.

    This is NOT the same as a vector cross-product.
    Quaternion cross-product is the equivalent of matrix multiplication.
    """
    q1x, q1y, q1z, q1w = quat1
    q2x, q2y, q2z, q2w = quat2

    return numpy.array(
        [
            # x = q1.w * q2.x + q1.x * q2.w + q1.z * q2.y - q1.y * q2.z 
            (q1w * q2x) + (q1x * q2w) + (q1z * q2y) - (q1y * q2z),
            # y = q1.w * q2.y + q1.y * q2.w + q1.x * q2.z - q1.z * q2.x
            (q1w * q2y) + (q1y * q2w) + (q1x * q2z) - (q1z * q2x),
            # z = q1.w * q2.z + q1.z * q2.w + q1.y * q2.x - q1.x * q2.y
            (q1w * q2z) + (q1z * q2w) + (q1y * q2x) - (q1x * q2y),
            # w = q1.w * q2.w - q1.x * q2.x - q1.y * q2.y - q1.z * q2.z
            (q1w * q2w) - (q1x * q2x) - (q1y * q2y) - (q1z * q2z)
            ]
        )

def is_zero_length( quat ):
    """Checks if a quaternion is zero length.

    :param numpy.array quat: The quaternion to check.
    :rtype: boolean.
    :return: True if the quaternion is zero length, otherwise False.
    """
    return quat[ 0 ] == quat[ 1 ] == quat[ 2 ] == quat[ 3 ] == 0.0

def is_non_zero_length( quat ):
    """Checks if a quaternion is not zero length.

    This is the opposite to 'is_zero_length'.
    This is provided for readabilities sake.

    :param numpy.array quat: The quaternion to check.
    :rtype: boolean
    :return: False if the quaternion is zero length, otherwise True.

    .. seealso:: is_zero_length
    """
    return not is_zero_length( quat )

def squared_length( quat ):
    """Calculates the squared length of a quaternion.

    Useful for avoiding the performanc penalty of
    the square root function.

    :param numpy.array quat: The quaternion to measure.
    :rtype: float, numpy.array
    :return: If a 1d array was passed, it will be a scalar.
        Otherwise the result will be an array of scalars with shape
        vec.ndim with the last dimension being size 1.
    """
    return vector.squared_length( quat )

def length( quat ):
    """Calculates the length of a quaternion.
    
    :param numpy.array quat: The quaternion to measure.
    :rtype: float, numpy.array
    :return: If a 1d array was passed, it will be a scalar.
        Otherwise the result will be an array of scalars with shape
        vec.ndim with the last dimension being size 1.
    """
    return vector.length( quat )

def normalise( quat ):
    """Ensure a quaternion is unit length (length ~= 1.0).

    The quaternion is **not** changed in place.
    
    :param numpy.array quat: The quaternion to normalise.
    :rtype: numpy.array
    :return: The normalised quaternion(s).
    """
    return vector.normalise( quat )

def get_rotation_angle( quat ):
    """Calculates the rotation around the quaternion's axis.

    :param numpy.array quat: The quaternion.
    :rtype: float.
    :return: The quaternion's rotation about the its axis in radians.
    """
    # extract the W component
    thetaOver2 = math.acos( quat[ 3 ] )
    return thetaOver2 * 2.0

def get_rotation_axis( quat ):
    """Calculates the axis of the quaternion's rotation.

    :param numpy.array quat: The quaternion.
    :rtype: numpy.array.
    :return: The quaternion's rotation axis.
    """
    # extract W component
    sinThetaOver2Sq = 1.0 - (quat[ 3 ] ** 2)
    
    if sinThetaOver2Sq <= 0.0:
        # assert here for the time being
        assert False
        print("rotation axis was identity")
        
        # identity quaternion or numerical imprecision.
        # return a valid vector
        # we'll treat -Z as the default
        out[:] = [ 0.0, 0.0, -1.0 ]
        return out
    
    oneOverSinThetaOver2 = 1.0 / math.sqrt( sinThetaOver2Sq )
    
    # we use the x,y,z values
    return numpy.array(
        [
            quat[ 0 ] * oneOverSinThetaOver2,
            quat[ 1 ] * oneOverSinThetaOver2,
            quat[ 2 ] * oneOverSinThetaOver2
            ]
        )

def dot( quat1, quat2 ):
    """Calculate the dot product of quaternions.

    :param numpy.array quat1: The first quaternion(s).
    :param numpy.array quat2: The second quaternion(s).
    :rtype: float, numpy.array
    :return: If a 1d array was passed, it will be a scalar.
        Otherwise the result will be an array of scalars with shape
        vec.ndim with the last dimension being size 1.
    """
    return vector.dot( quat1, quat2 )

def conjugate( quat ):
    """Calculates a quaternion with the opposite rotation.

    :param numpy.array quat: The quaternion.
    :rtype: numpy.array.
    :return: A quaternion representing the conjugate.
    """

    # invert x,y,z and leave w as is
    return numpy.array(
        [
            -quat[ 0 ],
            -quat[ 1 ],
            -quat[ 2 ],
            quat[ 3 ]
            ]
        )

def power( quat, exponent ):
    """Multiplies the quaternion by the exponent.

    The quaternion is **not** changed in place.

    :param numpy.array quat: The quaternion.
    :param float scalar: The exponent.
    :rtype: numpy.array.
    :return: A quaternion representing the original quaternion
        to the specified power.
    """
    # check for identify quaternion
    if math.fabs( quat[ w ] ) > 0.9999:
        # assert for the time being
        assert False
        print("rotation axis was identity")
        
        out[:] = quat
        return out
    
    alpha = math.acos( quat[ index.w ] )
    newAlpha = alpha * exponent
    multi = math.sin( newAlpha ) / math.sin( alpha )
    
    return numpy.array(
        [
            # x
            quat[ index.x ] * multi,
            # y
            quat[ index.y ] * multi,
            # z
            quat[ index.z ] * multi,
            # w
            math.cos( newAlpha )
            ]
        )

def inverse( quat ):
    """Calculates the inverse quaternion.

    The inverse of a quaternion is defined as
    the conjugate of the quaternion divided
    by the magnitude of the original quaternion.

    :param numpy.array quat: The quaternion to invert.
    :rtype: numpy.array.
    :return: The inverse of the quaternion.
    """
    return conjugate( quat ) / squared_length( quat )

def negate( quat ):
    """Calculates the negated quaternion.

    This is essentially the quaternion * -1.0.

    :param numpy.array quat: The quaternion.
    :rtype: numpy.array
    :return: The negated quaternion.
    """
    return quat * -1.0

def apply_to_vector( quat, vec ):
    """Rotates a vector by a quaternion.

    :param numpy.array quat: The quaternion.
    :param numpy.array vec: The vector.
    :rtype: numpy.array
    :return: The vector rotated by the quaternion.

    .. seealso:: http://content.gpwiki.org/index.php/OpenGL:Tutorials:Using_Quaternions_to_represent_rotation
    """
    def apply( quat, vec3 ):
        """
        v = numpy.array( vec )
        return v + 2.0 * vector.cross(
            quat[:-1],
            vector.cross( quat[:-1], v ) + (quat[-1] * v)
            )
        """
        length = vector.length( vec3 )
        vec3 = vector.normalise( vec3 )

        # use the vector to create a new quaternion
        # this is basically the vector3 to vector4 conversion with W = 0
        vec_quat = numpy.array( [ vec3[ 0 ], vec3[ 1 ], vec3[ 2 ], 0.0 ] )

        # quat * vec * quat^-1
        result = cross( quat, cross( vec_quat, conjugate( quat ) ) )
        return result[ :-1 ] * length

    if vec.size == 3:
        # convert to vector4
        # ignore w component
        return apply( quat, vec )
    elif vec.size == 4:
        vec3 = vector3.create_from_vector4( vec )
        vec3 = apply( quat, vec3 )
        return vector4.create_from_vector3( vec3 )
    else:
        raise ValueError( "Vector size unsupported" )

