import collections
import pygame

from pygame import Rect, Vector2, Vector3

from collision import is_AABB_point_collision

from window import instance as window

import math

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
		self.position = Vector2(x, y)
		self.velocity = Vector2(0, 0)
		self.aabb = Rect(x, y, 32, 32)
		self.speed = 32 + 16
		self.wall = Rect(128, 128, 32, 32)
		self.minkowski = self.aabb.copy()
		self.minkowski.x -= 32
		self.minkowski.y -= 32
		self.minkowski.w += 32
		self.minkowski.h += 32

	def update(self, dt):
		self.velocity.x = 0
		self.velocity.y = 0

		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.velocity[1] = -self.speed
		if keys[pygame.K_a]:
			self.velocity[0] = -self.speed * 2
		if keys[pygame.K_s]:
			self.velocity[1] = self.speed
		if keys[pygame.K_d]:
			self.velocity[0] = self.speed * 2

		# self.velocity.y += 16

		self.minkowski.x = self.aabb.x - 32
		self.minkowski.y = self.aabb.y - 32

		self.random = Rect(0, 0, 0, 0)

		collisions = []
		scale_min = 1.0
		collision_min = None

		count = 0

		for j, row in enumerate(tiles):
			for i, tile in enumerate(row):
				if tile == 0:
					continue
				scale, nx, ny = is_AABB_point_collision(self.minkowski, Vector2(i * 32 + 128, j * 32 + 128), self.velocity, dt)
				if nx != 0 or ny != 0:
					count += 1
				collisions.append((scale, nx, ny, Vector2(i * 32 + 128, j * 32 + 128)))
				if scale < scale_min:
					scale_min = scale
					collision_min = collisions[-1]
				if scale == scale_min:
					if collisions[-1][1] != 0:
						collision_min = collisions[-1]
		collided = False

		if collision_min:
			rect = Rect(*collision_min[3], 32, 32)
			self.random = rect
			nx, ny = collision_min[1], collision_min[2]
			if count == 1 and rect.collidepoint(self.position.x, self.position.y + 32 - ny) and not rect.collidepoint(self.position.x + 8, self.position.y + 32 - ny):
				# self.position.x = rect.x + rect.w
				# self.position.y += 1
				self.velocity.x += 64 / (rect.x + rect.w - self.position.x)
				self.velocity.y = 0
				if self.position.x + self.velocity.x * dt >= rect.x + rect.w:
					self.position.x = rect.x + rect.w
					self.velocity.x = 0
					self.position.y += 1
				self.aabb.topleft = self.position
				# self.velocity.x = 0

				print(self.velocity.x)

			if count == 1 and rect.collidepoint(self.position.x + self.aabb.w, self.position.y + 32 - ny) and not rect.collidepoint(self.position.x + self.aabb.w - 8, self.position.y + 32 - ny):
				# self.position.x = rect.x + rect.w
				# self.position.y += 1
				if (self.position.x + self.aabb.w - rect.x) != 0:

					self.velocity.x -= 64 / (self.position.x + self.aabb.w - rect.x)
					self.velocity.y = 0
					if self.position.x + self.velocity.x * dt <= rect.x - rect.w:
						self.position.x = rect.x - rect.w
						self.velocity.x = 0
						self.position.y += 1
					self.aabb.topleft = self.position
				# self.velocity.x = 0

				print(self.velocity.x)

			print(ny, rect.collidepoint(self.position.x, self.position.y - ny))

			if count == 1 and rect.collidepoint(self.position.x, self.position.y - ny) and not rect.collidepoint(self.position.x + 8, self.position.y - ny):
				print("left")
				# self.position.x = rect.x + rect.w
				# self.position.y += 1
				self.velocity.x += 64 / (rect.x + rect.w - self.position.x)
				self.velocity.y = 0
				if self.position.x + self.velocity.x * dt >= rect.x + rect.w:
					self.position.x = rect.x + rect.w
					self.velocity.x = 0
					self.position.y -= 1
				self.aabb.topleft = self.position
				# self.velocity.x = 0

				print(self.velocity.x)

			if count == 1 and rect.collidepoint(int(self.position.x + self.aabb.w), self.position.y - ny) and not rect.collidepoint(self.position.x + self.aabb.w - 8, self.position.y - ny):
				print("right")

				# self.position.x = rect.x + rect.w
				# self.position.y += 1
				if (self.position.x + self.aabb.w - rect.x) != 0:

					self.velocity.x -= 64 / (self.position.x + self.aabb.w - rect.x)
					self.velocity.y = 0
					if self.position.x + self.velocity.x * dt <= rect.x - rect.w:
						self.position.x = rect.x - rect.w
						self.velocity.x = 0
						self.position.y -= 1
					self.aabb.topleft = self.position
				# self.velocity.x = 0

				print(self.velocity.x)

			# if count == 1 and rect.collidepoint(self.position.x + self.aabb.w - 1, self.position.y + 32 - ny) and not rect.collidepoint(self.position.x + self.aabb.w - 2, self.position.y + 32 - ny):
			# 	print("woass")
			# 	self.position.x = rect.x - rect.w
			# 	self.position.y += 1
			# 	self.velocity.x = 0
			# 	self.aabb.topleft = self.position

		collisions = []
		scale_min = 1.0
		collision_min = None

		for j, row in enumerate(tiles):
			for i, tile in enumerate(row):
				if tile == 0:
					continue
				scale, nx, ny = is_AABB_point_collision(self.minkowski, Vector2(i * 32 + 128, j * 32 + 128), self.velocity, dt)
				collisions.append((scale, nx, ny, Vector2(i * 32 + 128, j * 32 + 128)))
				if scale < scale_min:
					scale_min = scale
					collision_min = collisions[-1]
				if scale == scale_min:
					if collisions[-1][1] != 0:
						collision_min = collisions[-1]

		if collision_min:
			scale, nx, ny = collision_min[0], collision_min[1], collision_min[2]
			collided = True
		else:
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

			for j, row in enumerate(tiles):
				for i, tile in enumerate(row):
					if tile == 0:
						continue
					scale, nx, ny = is_AABB_point_collision(self.minkowski, Vector2(i * 32 + 128, j * 32 + 128), self.velocity, dt)
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
				pygame.draw.rect(window.surface, (0, 0, 0, 255), rect, width=1)



		pygame.draw.rect(window.surface, (0, 255, 0, 255), self.random, width=1)
		# pygame.draw.circle(window.surface, (255, 0, 0, 255), self.wall.topleft, 2)

