import pygame

from pygame import Rect, Vector2

from physics import is_AABB_collision

from window import instance as window

import math

class Player:
	def __init__(self, x: float, y: float) -> None:
		self.position = Vector2(x, y)
		self.velocity = Vector2(0, 0)
		self.aabb = Rect(x, y, 32, 32)
		self.speed = 32
		self.wall = Rect(128, 128, 32, 32)

	def update(self, dt):
		self.velocity = Vector2(0, 0)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.velocity[1] = -self.speed
		if keys[pygame.K_a]:
			self.velocity[0] = -self.speed
		if keys[pygame.K_s]:
			self.velocity[1] = self.speed
		if keys[pygame.K_d]:
			self.velocity[0] = self.speed

		scale, nx, ny = is_AABB_collision(self.aabb, self.wall, self.velocity, dt)

		print(scale)

		self.position += self.velocity * scale * dt

		tl = 1.0 - scale
		dot = (self.velocity.x * ny + self.velocity.y * nx) * tl

		self.velocity.x = dot * ny * dt
		self.velocity.y = dot * nx * dt

		self.position += self.velocity

		self.aabb.topleft = self.position

	def render(self):
		pygame.draw.rect(window.surface, (0, 0, 0, 255), self.aabb, width=1)
		pygame.draw.rect(window.surface, (0, 0, 0, 255), self.wall, width=1)
