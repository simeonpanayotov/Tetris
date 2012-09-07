import unittest
import shapes

class SquareShapeBoxPositioning(unittest.TestCase):
    def test_square_boxes_form_square(self):
        square = shapes.Square(0, 0)

        self.assertEqual(square.blocks[0].x, 0)
        self.assertEqual(square.blocks[0].y, 0)

        self.assertEqual(square.blocks[1].x, 1)
        self.assertEqual(square.blocks[1].y, 0)

        self.assertEqual(square.blocks[2].x, 0)
        self.assertEqual(square.blocks[2].y, 1)

        self.assertEqual(square.blocks[3].x, 1)
        self.assertEqual(square.blocks[3].y, 1)

#class SquareShapeRotationTests(unittest.TestCase):
#    def setUp(self):
#        self.square = Square(Coords(0, 0))
#
#    def test_rotate_does_not_change_boxes_coords(self):
#        self.square.rotate()
#
#        self.assertEqual(self.square.boxUpperLeft.x, )

if __name__ == '__main__':
    unittest.main()
