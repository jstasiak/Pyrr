import unittest
import math

import numpy

from pyrr import geometric_tests as gt

from pyrr import line
from pyrr import plane
from pyrr import ray
from pyrr import aabb


class test_geometric_tests( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def closest_point_on_line( self ):
        new_line = line.create_from_points(
            [ 0.0, 0.0, 0.0 ],
            [10.0, 0.0, 0.0 ]
            )
        points = numpy.array( [ 0.5, 1.0, 0.0 ] )

        result = gt.closest_point_on_line( new_line, point )

        expected = numpy.array( [ 0.5, 0.0, 0.0 ] )

        self.assertTrue(
            numpy.array_equal( result, expected ),
            "Closest point on plane incorrect"
            )

    def test_height_above_plane( self ):
        v1 = numpy.array( [ 0.0, 0.0, 1.0 ] )
        v2 = numpy.array( [ 1.0, 0.0, 1.0 ] )
        v3 = numpy.array( [ 0.0, 1.0, 1.0 ] )
        point = numpy.array([ 0.0, 0.0, 20.0 ])

        p = plane.create_from_points( v1, v2, v3 )
        p = plane.invert_normal( p )

        result = gt.point_height_above_plane( point, p )

        # should be 19.0
        expected = 19.0

        self.assertEqual(
            result,
            expected,
            "Height above plane incorrect"
            )

    def test_closest_point_on_plane( self ):
        p = numpy.array( [ 0.0, 1.0, 0.0, 0.0 ] )
        point = numpy.array([ 5.0, 20.0, 5.0 ])
        
        result = gt.point_closest_point_on_plane( point, p )

        # should be # 0, 0, 1
        expected = numpy.array( [ 5.0, 0.0, 5.0 ] )

        self.assertTrue(
            numpy.array_equal( result, expected ),
            "Closest point on plane incorrect"
            )

    def test_point_intersect_rectangle( self ):
        def valid_intersections():
            rect = numpy.array(
                [
                    [0.0, 0.0],
                    [5.0, 5.0]
                    ]
                )

            def point_1():
                point = [ 0.0, 0.0 ]
                result = gt.point_intersect_rectangle( point, rect )

                self.assertTrue(
                    numpy.array_equal( result, point )
                    )
            point_1()

            def point_2():
                point = [ 5.0, 5.0 ]
                result = gt.point_intersect_rectangle( point, rect )

                self.assertTrue(
                    numpy.array_equal( result, point )
                    )
            point_2()

            def point_3():
                point = [ 1.0, 1.0 ]
                result = gt.point_intersect_rectangle( point, rect )

                self.assertTrue(
                    numpy.array_equal( result, point )
                    )
            point_3()
        valid_intersections()

        def invalid_intersections():
            rect = numpy.array(
                [
                    [0.0, 0.0],
                    [5.0, 5.0]
                    ]
                )

            def point_1():
                point = [-1.0, 1.0 ]
                result = gt.point_intersect_rectangle( point, rect )

                self.assertFalse(
                    numpy.array_equal( result, point )
                    )
            point_1()

            def point_2():
                point = [ 1.0, 10.0 ]
                result = gt.point_intersect_rectangle( point, rect )

                self.assertFalse(
                    numpy.array_equal( result, point )
                    )
            point_2()

            def point_3():
                point = [ 1.0,-1.0 ]
                result = gt.point_intersect_rectangle( point, rect )

                self.assertFalse(
                    numpy.array_equal( result, point )
                    )
            point_3()
        invalid_intersections()

    def test_ray_intersect_aabb( self ):
        def valid_intersections():
            def ray_1():
                aabb = numpy.array( [ [-1.0,-1.0,-1.0 ], [ 1.0, 1.0, 1.0 ] ] )
                ray = numpy.array( [ [ 0.5, 0.5, 0.0 ], [ 0.0, 0.0,-1.0 ] ] )
                expected = numpy.array( [ 0.5, 0.5,-1.0 ] )

                result = gt.ray_intersect_aabb( ray, aabb )

                self.assertTrue(
                    numpy.array_equal( result, expected ),
                    "Ray vs AABB intersection incorrect: expected %s, got %s" % (
                        expected, result
                        )
                    )
            ray_1()

            def ray_2():
                aabb = numpy.array( [ [-1.0,-1.0,-1.0 ], [ 1.0, 1.0, 1.0 ] ] )
                ray = numpy.array( [ [2.0, 2.0, 2.0 ], [ -1.0, -1.0, -1.0 ] ] )
                expected = numpy.array( [1.0, 1.0, 1.0] )

                result = gt.ray_intersect_aabb( ray, aabb )

                self.assertTrue(
                    numpy.array_equal( result, expected ),
                    "Ray vs AABB intersection incorrect: expected %s, got %s" % (
                        expected, result
                        )
                    )
            ray_2()
        valid_intersections()

        def invalid_intersections():
            pass
        invalid_intersections()



if __name__ == '__main__':
    unittest.main()

