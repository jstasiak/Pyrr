""" Provides functions to calculate and manipulate
Axis-Aligned Minimum Bounding Boxes (AAMBB).

AAMBB are a simple 3D rectangle with no orientation.
It is up to the user to provide translation.
AAMBB differ from AABB in that they allow for the
content to rotate freely and still be within the AAMBB.

An AABB is represented by an array of 2 x 3D vectors.
The first vector represents the minimum extent.
The second vector represents the maximum extent.

TODO: add transform( matrix )
TODO: add point_within_aabb
TODO: use point_within_aabb for unit tests
"""

import numpy

import aabb
import vector


def _empty():
    return numpy.empty( (2,3), dtype = numpy.float )

def create_from_bounds( min, max, out = None ):
    """ Creates an AAMBB using the specified minimum
    and maximum values.
    """
    # stack our bounds together and add them as points
    bounds = numpy.vstack( min, max )
    return create_from_points( bounds, out )

def create_from_points( points, out = None ):
    """ Creates an AAMBB from the list of specified points.

    Points must be a 2D list. Ie:
    [
        [ x, y, z ],
        [ x, y, z ],
    ]
    """
    if out == None:
        out = _empty()

    # convert any negative values to positive
    abs_points = numpy.absolute( points )

    # extract the maximum extent as a vector
    vec = numpy.amax( abs_points, axis = 0 )

    # find the length of this vector
    length = vector.length( vec )

    # our AAMBB extends from +length to -length
    # in all directions
    out[:] = [
        [-length,-length,-length ],
        [ length, length, length ]
        ]

def create_from_aabbs( aabbs, out = None ):
    """ Creates an AAMBB from a list of existing AABBs.

    AABBs must be a 2D list. Ie:
    [
        AABB,
        AABB,
    ]
    """
    # reshape the AABBs as a series of points
    points = aabbs.view()
    points.shape = (-1, 3 )

    return create_from_points( points, out )

def add_points( aabb, points, out = None ):
    """ Extends an AAMBB to encompass a list
    of points.

    It should be noted that this ensures that
    the encompassed points can rotate freely.
    Calling this using the min / max points from
    the AAMBB will create an even bigger AAMBB.
    """
    if out == None:
        out = _empty()

    # add our AABB to the list of points
    values = numpy.vstack( points, aabb[ 0 ], aabb[ 1 ] )

    # convert any negative values to positive
    abs_points = numpy.absolute( values )

    # extract the maximum extent as a vector
    vec = numpy.amax( abs_points, axis = 0 )

    # find the length of this vector
    length = vector.length( vec )

    # our AAMBB extends from +length to -length
    # in all directions
    out[:] = [
        [-length,-length,-length ],
        [ length, length, length ]
        ]

def add_aabbs( aabb, aabbs, out = None ):
    """ Extend an AAMBB to encompass a list
    of other AABBs or AAMBBs.

    It should be noted that this ensures that
    the encompassed AABBs can rotate freely.
    Using the AAMBB itself in this calculation
    will create an event bigger AAMBB.
    """
    # reshape the AABBs as a series of points
    points = aabbs.view()
    points.shape = (-1, 3 )

    # use the add_points
    return add_points( aabb, points, out )

def centre_point( aabb ):
    """ Returns the centre point of the AABB.
    This should always be [0.0, 0.0, 0.0]
    """
    return (aabb[ 0 ] + aabb[ 1 ]) * 0.5

def minimum( aabb ):
    """ Returns the minimum point of the AABB.
    """
    return aabb[ 0 ]

def maximum( aabb ):
    """ Returns the maximum point of the AABB.
    """
    return aabb[ 1 ]

def clamp_points( aabb, points, out = None ):
    """ Takes a list of points and modifies them to
    fit within the AABB.
    """
    # use the same function as present in AABB
    aabb.clamp_points( aabb, points, out )
