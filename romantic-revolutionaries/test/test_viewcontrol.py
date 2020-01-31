"""Unitest the view control.

Run these tests with either with "pytest" or python -m "unittest"
from within the same directory.
"""

import unittest

from modules.view.viewcontrol import ViewControl
from modules.navigation.navcont import NavControl, Directions
from modules.map.MapControl import DungeonMap


class Observer:
    def __init__(self):
        self.descriptive_text = ''

    def callback(self, descriptive_text):
        self.descriptive_text = descriptive_text
        # print(self.descriptive_text)


class TestViewControl(unittest.TestCase):
    def setUp(self):
        # setup the initial test map
        DungeonMap.map_vector = [
                [1, 0, 0, 0],
                [0, 1, 6, 0],
                [0, 9, 1, 0],
                [0, 0, 0, 0]]

        self.ob = Observer()
        self.mc = DungeonMap()
        self.nc = NavControl()
        self.vc = ViewControl()

        self.nc.subscribe(self.mc.callback)
        self.mc.subscribe(self.vc.callback)
        self.vc.subscribe(self.ob.callback)

    def test_look(self):
        self.nc.go(Directions.NORTH)
        self.vc.look(Directions.NORTH)
        expected = """You have run into a wall.
There is a wall in front of you.
It is bordered to the left with a dark passage.
It is bordered to the right with a wall.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.vc.look(Directions.SOUTH)
        expected = """You have run into a wall.
There is a dark passage ahead of you.
It is bordered to the left with a dark passage.
It is bordered to the right with a wall.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.vc.look(Directions.EAST)
        expected = """You have run into a wall.
There is a dark passage ahead of you.
It is bordered to the left with a wall.
It is bordered to the right with a dark passage.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.vc.look(Directions.WEST)
        expected = """You have run into a wall.
There is a wall in front of you.
It is bordered to the left with a wall.
It is bordered to the right with a dark passage.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.nc.go(Directions.SOUTH)
        self.vc.look(Directions.NORTH)
        expected = """There is a dark passage ahead of you.
It is bordered to the left with a wall.
It is bordered to the right with a 6.
At your feet there is 9.
"""

        self.assertEqual(self.ob.descriptive_text, expected)
        expected = """There is a dark passage ahead of you.
It is bordered to the left with a wall.
It is bordered to the right with a 6.
At your feet there is 9.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.vc.look(Directions.SOUTH)
        expected = """There is a wall in front of you.
It is bordered to the left with a wall.
It is bordered to the right with a wall.
At your feet there is 9.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.vc.look(Directions.EAST)
        expected = """There is a dark passage ahead of you.
It is bordered to the left with a 6.
It is bordered to the right with a wall.
At your feet there is 9.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.vc.look(Directions.WEST)
        expected = """There is a wall in front of you.
It is bordered to the left with a wall.
It is bordered to the right with a wall.
At your feet there is 9.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.nc.go(Directions.EAST)
        self.vc.look(Directions.NORTH)
        expected = """There is a dark passage ahead of you.
It is bordered to the left with a dark passage.
It is bordered to the right with a wall.
"""
        self.assertEqual(self.ob.descriptive_text, expected)
        self.vc.look(Directions.SOUTH)
        expected = """There is a wall in front of you.
It is bordered to the left with a wall.
It is bordered to the right with a wall.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.vc.look(Directions.EAST)
        expected = """There is a wall in front of you.
It is bordered to the left with a wall.
It is bordered to the right with a wall.
"""
        self.assertEqual(self.ob.descriptive_text, expected)
        self.vc.look(Directions.WEST)
        expected = """There is a dark passage ahead of you.
It is bordered to the left with a wall.
It is bordered to the right with a dark passage.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.nc.go(Directions.WEST)
        self.vc.look(Directions.NORTH)
        expected = """There is a dark passage ahead of you.
It is bordered to the left with a wall.
It is bordered to the right with a 6.
At your feet there is 9.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.vc.look(Directions.SOUTH)
        expected = """There is a wall in front of you.
It is bordered to the left with a wall.
It is bordered to the right with a wall.
At your feet there is 9.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.vc.look(Directions.EAST)
        expected = """There is a dark passage ahead of you.
It is bordered to the left with a 6.
It is bordered to the right with a wall.
At your feet there is 9.
"""
        self.assertEqual(self.ob.descriptive_text, expected)

        self.vc.look(Directions.WEST)
        expected = """There is a wall in front of you.
It is bordered to the left with a wall.
It is bordered to the right with a wall.
At your feet there is 9.
"""
        self.assertEqual(self.ob.descriptive_text, expected)
