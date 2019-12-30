#!/usr/bin/env python

from collections import namedtuple
from math import sqrt

Node = namedtuple('Node', 'axis value split left right')


def distance(a, b):
    """Euclidian distance"""
    assert len(a) == len(b), "points must have same dimensions"
    return sqrt(sum([(i - j) ** 2 for i, j in zip(a, b)]))


class KDTree:
    """K-D Tree"""

    def __init__(self):
        self.root = None
        self.dimensions = None

    @staticmethod
    def from_points(points, dimensions=None):
        """Build a KDTree from a list of points"""
        if not points:
            return

        tree = KDTree()
        tree.dimensions = dimensions if dimensions else len(points[0])
        tree.root = KDTree._nodes_from_points(points, tree.dimensions)

        return tree

    @staticmethod
    def _nodes_from_points(points, dimensions, depth=0):
        """Build the Node structure recursively from points"""
        if not points:
            return

        axis = depth % dimensions
        points.sort(key=lambda x: x[axis])
        median = len(points) // 2

        return Node(
            axis=axis,
            value=points[median],
            split=points[median][axis],
            left=KDTree._nodes_from_points(points[:median], dimensions, depth=depth + 1),
            right=KDTree._nodes_from_points(points[median + 1:], dimensions, depth=depth + 1)
        )

    def nearest(self, point):
        """Get the point in the tree nearest to the provided point"""
        stack = [(True, self.root), (False, self.root)]
        closest = None
        closest_distance = None

        while stack:
            check_opposite, node = stack.pop()

            if not check_opposite:
                dist = distance(node.value, point)

                if not closest or dist < closest_distance:
                    closest_distance = dist
                    closest = node

            if point[node.axis] < node.split:
                if check_opposite:
                    if node.right:
                        if (point[node.axis] + closest_distance) >= node.split:
                            stack.append((False, node.right))
                else:
                    if node.left:
                        stack.append((True, node.left))
                        stack.append((False, node.left))
            else:
                if check_opposite:
                    if node.left:
                        if (point[node.axis] - closest_distance) <= node.split:
                            stack.append((False, node.left))
                else:
                    if node.right:
                        stack.append((True, node.right))
                        stack.append((False, node.right))

        return closest_distance, closest
