import collections
import pygame

from pygame.rect import Rect as Rect
from pygame.math import Vector2 as Vector2
from pygame.math import Vector3 as Vector3

from collision import AABB_point_collision

from window import instance as window

import math

#  TODO: Proper raycasts

tiles = [
	[1, 0, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 1],
	[1, 1, 0, 1, 0, 1],
	[1, 0, 0, 1, 1, 1],
	[1, 1, 0, 0, 0, 1],
	[1, 1, 1, 1, 0, 1]
]

class Player:
	def __init__(self, x: float, y: float) -> None:
		self.position: Vector2 = Vector2(x, y)
		self.velocity: Vector2 = Vector2(0, 0)
		self.aabb = Rect(x, y, 32*.90, 32)
		self.speed = 32 + 16
		self.wall = Rect(128, 128, 32, 32)
		self.minkowski = self.aabb.copy()
		self.minkowski.x -= 32
		self.minkowski.y -= 32
		self.minkowski.w += 32
		self.minkowski.h += 32
		self.floor = False
		self.ceil = False

	def update(self, dt):
		global tiles
		self.velocity.x = 0

		tiles = [
			[1, 0, 1, 1, 1, 1],
			[1, 0, 0, 0, 0, 1],
			[1, 1, 0, 1, 0, 1],
			[1, 0, 0, 1, 1, 1],
			[1, 1, 0, 0, 0, 1],
			[1, 1, 1, 1, 0, 1]
		]

		keys = pygame.key.get_pressed()
		if keys[pygame.K_w] and self.floor and not self.ceil:
			self.velocity[1] += -self.speed * 10
		if keys[pygame.K_a]:
			self.velocity[0] = -self.speed * 2
		if keys[pygame.K_s]:
			self.velocity[1] = self.speed
		if keys[pygame.K_d]:
			self.velocity[0] = self.speed * 2

		self.velocity.y += 16

		self.minkowski.x = self.aabb.x - 32
		self.minkowski.y = self.aabb.y - 32

		self.random = Rect(0, 0, 0, 0)

		collisions = []
		scale_min = 1.0
		collision_min = None



		sr = int(max(0, (self.position.y - 128) // 32 - 1))
		sc = int(max(0, (self.position.x - 128) // 32 - 1))
		er = int((self.position.y + self.aabb.h - 128 - .5) / 32) + 1
		ec = int((self.position.x + self.aabb.w - 128 - .5) / 32) + 1

		self.ceil = False

		for j, row in enumerate(tiles):
			for i, tile in enumerate(row):
				point = Vector2(i * 32 + 128, j * 32 + 128)
				rect = Rect(point.x, point.y, 32, 32)
				if j < sr or j > er or i < sc or i > ec:
					continue
				if tile == 0:
					continue
				tiles[j][i] = 2
				if rect.collidepoint(self.position.x + 1, self.position.y - 1) or rect.collidepoint(self.position.x + self.aabb.w - 1, self.position.y - 1):
					self.ceil = True
				scale, nx, ny = AABB_point_collision(*self.minkowski, *Vector2(i * 32 + 128, j * 32 + 128), *self.velocity, dt)
				collisions.append((scale, nx, ny, Vector2(i * 32 + 128, j * 32 + 128)))
				if scale < scale_min:
					scale_min = scale
					collision_min = collisions[-1]
		collided = False
		if collision_min:
			scale, nx, ny = collision_min[0], collision_min[1], collision_min[2]
			collided = True
			if ny == -1.0:
				self.floor = True
			else:
				self.floor = False
		else:
			self.floor = False
			scale = 1.0
			nx = 0
			ny = 0
		if nx != 0 or ny != 0:
			collided = True
			self.position += self.velocity * scale * dt
			self.aabb.topleft = self.position

			tl = 1.0 - scale
			dot = (self.velocity.x * ny + self.velocity.y * nx) * tl

			self.velocity.x = dot * ny
			self.velocity.y = dot * nx

			collisions = []
			scale_min = 1.0
			collision_min = None

			sr = int(max(0, (self.position.y - 128) // 32 - 1))
			sc = int(max(0, (self.position.x - 128) // 32 - 1))
			er = math.ceil((self.position.y + self.aabb.h - 128) / 32) + 1
			ec = math.ceil((self.position.x + self.aabb.w - 128) / 32) + 1

			for j, row in enumerate(tiles):
				for i, tile in enumerate(row):
					if j < sr or j >= er or i < sc or i >= ec:
						continue
					if tile == 0:
						continue
					scale, nx, ny = AABB_point_collision(*self.minkowski, *Vector2(i * 32 + 128, j * 32 + 128), *self.velocity, dt)
					collisions.append((scale, nx, ny, i, j))
					if scale < scale_min:
						scale_min = scale
						collision_min = collisions[-1]



			if collision_min:
				scale, nx, ny = collision_min[0], collision_min[1], collision_min[2]
			else:
				scale = 1.0
				nx = 0
				ny = 0

			collided = True
			self.position += self.velocity * scale * dt
			self.aabb.topleft = self.position

		if not collided:
			self.floor = False
			self.position += self.velocity * dt
			self.aabb.topleft = self.position
	def render(self):
		pygame.draw.rect(window.surface, (0, 0, 0, 255), self.aabb, width=1)
		pygame.draw.rect(window.surface, (0, 0, 0, 255), self.wall, width=1)
		for j, row in enumerate(tiles):
			for i, tile in enumerate(row):
				if tile == 0:
					continue
				rect = Rect(i * 32 + 128, j * 32 + 128, 32, 32)
				if tile == 1:
					pygame.draw.rect(window.surface, (0, 0, 0, 255), rect, width=1)
				if tile == 2:
					pygame.draw.rect(window.surface, (0, 255, 0, 255), rect, width=1)



		# pygame.draw.rect(window.surface, (0, 255, 0, 255), self.random, width=1)
		# pygame.draw.circle(window.surface, (255, 0, 0, 255), self.wall.topleft, 2)

