from typing import Tuple
from pygame import Vector2, Rect, Vector3, Vector2
import pygame

from window import instance as window

import math

def clamp(n, lower, upper) -> float:
	return max(lower, min(n, upper))

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

class PhysicsObject:
	def __init__(self, x: float, y: float) -> None:
		self.force_accumalated = Vector2(0, 0)

		self.position = Vector2(x, y)
		self.velocity = Vector2(0, 0)

		self.gravity = .001
		self.mass = 20

	def apply_force(self, force):
		self.force_accumalated += force

	def update(self, dt: int) -> None:
		if math.isclose(self.velocity.x, 0, abs_tol=0.001): self.velocity.x = 0
		if math.isclose(self.velocity.y, 0, abs_tol=0.001): self.velocity.y = 0
		coeficient = 1
		u = Vector3(0, -1, 0)
		weight = Vector3(0, self.gravity, 0) * self.mass
		magnitude = weight.dot(u)
		velocity = Vector3(self.velocity.x, self.velocity.y, 0)
		direction = u.cross(Vector3(0, 0, 1))
		sign = direction.dot(velocity)
		friction = sign * direction * magnitude * coeficient
		x_friction = Vector2(friction.x, friction.y)

		coeficient = 1
		u = Vector3(-1, 0, 0)
		weight = Vector3(self.gravity, 0, 0) * self.mass
		magnitude = weight.dot(u)
		velocity = Vector3(self.velocity.x, self.velocity.y, 0)
		direction = u.cross(Vector3(0, 0, 1))
		sign = direction.dot(velocity)
		friction = sign * direction * magnitude * coeficient
		y_friction = Vector2(friction.x, friction.y)

		friction = Vector2(x_friction.x, y_friction.y)

		print(self.velocity)
		print(friction)

		acceleration = self.force_accumalated / self.mass
		acceleration += friction / self.mass
		acceleration += Vector2(0, self.gravity)

		self.force_accumalated = Vector2(0, 0)

		self.velocity += acceleration * dt
		self.position += self.velocity * dt



class PhysicsCharacter(PhysicsObject):
	def __init__(self, x: float, y: float) -> None:
		PhysicsObject.__init__(self, x, y)
		self.on_floor = False
		self.on_wall = False
		self.terminal_sliding_speed = 0.1
		self.terminal_falling_speed = 0.75
		self.terminal_running_speed = 0.75
		self.gravity_while_falling = 0.001
		self.gravity_while_rising = 0.00075
		self.floor_friction = 0.5
		self.handle_collision = None

	def update(self, dt):
		if not self.on_floor:
			if self.velocity.y > 0:
				self.gravity = self.gravity_while_falling
			else:
				self.gravity = self.gravity_while_rising

		# if self.on_wall:
		# 	self.terminal_falling_speed = 0.25
		# else:
		# 	self.terminal_falling_speed = 0.75

		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.apply_force(Vector2(0, -0.075))
		if keys[pygame.K_a]:
			self.apply_force(Vector2(-0.0025, 0))
		if keys[pygame.K_s]:
			self.apply_force(Vector2(0, 0.0025))
		if keys[pygame.K_d]:
			self.apply_force(Vector2(0.0025, 0))


		# self.velocity.x *= self.floor_friction

		# self.velocity.y = min(self.velocity.y, self.terminal_falling_speed)

		# self.velocity.x = clamp(self.velocity.x, -self.terminal_running_speed, self.terminal_running_speed)

		if self.handle_collision: self.handle_collision(self, dt)

		PhysicsObject.update(self, dt)

	def render(self):
		pygame.draw.rect(window.surface, (0, 0, 0, 255), Rect(self.position.x, self.position.y, 32, 32))