from typing import Tuple
from pygame import Vector2, Rect
from enum import Enum

def is_AABB_intersection(rect: Rect, other: Rect) -> bool:
	return rect.x < other.x + other.w and other.x < rect.x + rect.w and rect.y < other.y + other.h and other.y < rect.y + rect.h

def AABB_distance_to(rect: Rect, other: Rect) -> Tuple[int, int]:
	dx = 0
	dy = 0

	if rect.x < other.x:
		dx = other.x - (rect.x + rect.w)
	elif rect.x > other.x:
		dx = rect.x - (other.x + other.w)

	if rect.y < other.y:
		dy = other.y - (rect.y + rect.h)
	elif rect.y > other.y:
		dy = rect.y - (other.y + other.h)

	return dx, dy

class AABBEdges(Enum):
	LEFT = 0
	RIGHT = 1
	TOP = 2
	BOTTOM = 3
	CORNER = 4

def AABB_collision_response(rect: Rect, velocity: Vector2, other: Rect, side: AABBEdges, dt: float):
	distance_x, distance_y = AABB_distance_to(rect, other)
	velocity_x, velocity_y = velocity.x * dt, velocity.y * dt
	x_axis_time_until_collide = abs(float(distance_x) / float(velocity_x)) if velocity_x != 0 else 0	
	y_axis_time_until_collide = abs(float(distance_y) / float(velocity_y)) if velocity_y != 0 else 0

	if velocity_x != 0 and velocity_y == 0:
		if side == AABBEdges.LEFT or side == AABBEdges.RIGHT:
			velocity.x = x_axis_time_until_collide * velocity.x

	elif velocity_x == 0 and velocity_y != 0:
		if side == AABBEdges.TOP or side == AABBEdges.BOTTOM: 
			velocity.y = y_axis_time_until_collide * velocity.y

	else:
		if side == AABBEdges.LEFT or side == AABBEdges.RIGHT:
			velocity.x = x_axis_time_until_collide * velocity.x

		if side == AABBEdges.TOP or side == AABBEdges.BOTTOM:
			velocity.y = y_axis_time_until_collide * velocity.y

		if side == AABBEdges.CORNER:
			shortest_time = min(x_axis_time_until_collide, y_axis_time_until_collide)
			velocity.x = shortest_time * velocity.x


class BasicPhysicsObject:
	def __init__(self, x, y, collisions_handle) -> None:
		self.position = Vector2(x, y)
		self.velocity = Vector2(0, 0)
		self.collisions_handle = collisions_handle

	def update(self, dt: float):
		self.collisions_handle(self, dt)
		self.position += self.velocity * dt