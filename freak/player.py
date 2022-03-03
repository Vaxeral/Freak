from pygame import Rect, Vector2
import pygame

from physics import AABBEdges, BasicPhysicsObject, AABB_collision_response, is_AABB_intersection
from window import instance as window

tiles = [
	[0, 0, 1, 0, 0, 0],
	[0, 1, 0, 0, 0, 0],
	[0, 1, 0, 0, 1, 0],
	[0, 2, 0, 1, 2, 0],
	[0, 0, 0, 0, 0, 0],
	[1, 0, 1, 0, 2, 2]
]

def collisions_handle(self, dt):
	# wall = Rect(0, 400, 640, 32)


	# rect = Rect(self.position.x + self.velocity.x * dt, self.position.y + self.velocity.y * dt, self.aabb.w, self.aabb.h)

	# intersection = is_AABB_intersection(rect, wall)

	# if intersection:
	# 	AABB_collision_response(self.aabb, self.velocity, wall, AABBEdges.TOP, dt)

	# wall = Rect(100, 0, 32, 300)

	# intersection = is_AABB_intersection(rect, wall)

	# if intersection:
	# 	AABB_collision_response(self.aabb, self.velocity, wall, AABBEdges.LEFT, dt)
	RECT_W = 32
	RECT_H = 32
	collisions = []
	for j, row in enumerate(tiles):
		for i, tile in enumerate(row):
			if not tile:
				continue
			wall = Rect(128 + i * RECT_W, 128 + j * RECT_H, RECT_W, RECT_H)
			rect = Rect(self.position.x + self.velocity.x * dt, self.position.y + self.velocity.y * dt, self.aabb.w, self.aabb.h)
			intersection = is_AABB_intersection(rect, wall)
			if intersection:
				lx = self.aabb.left
				rx = self.aabb.right
				mx = self.aabb.centerx
				y = self.aabb.bottom + max(self.velocity.y * dt, 1)
				floor = False

				#  Raycasts need one every tile width
				if self.velocity.y >= 0:
					if wall.collidepoint(lx + 1, y) or wall.collidepoint(rx - 1, y) or wall.collidepoint(mx, y):
						floor = True


				y = self.aabb.top + min(self.velocity.y * dt, -1)

				ceil = False
				if self.velocity.y <= 0:
					if wall.collidepoint(lx + 1, y) or wall.collidepoint(rx - 1, y) or wall.collidepoint(mx, y):
						ceil = True


				lx = self.aabb.left + self.velocity.x * dt
				rx = self.aabb.right + self.velocity.x * dt
				ty = self.aabb.top
				by = self.aabb.bottom
				my = self.aabb.centery
				wally = False

				if self.velocity.x <= 0:
					if wall.collidepoint(lx, ty + 1) or wall.collidepoint(lx, by - 1) or wall.collidepoint(lx, my):
						wally = True
				elif self.velocity.x >= 0:
					if wall.collidepoint(rx, ty + 1) or wall.collidepoint(rx, by - 1) or wall.collidepoint(rx, my):
						wally = True

				side = None

				if floor:
					side = AABBEdges.TOP
				if ceil:
					side = AABBEdges.BOTTOM
				if wally:
					side = AABBEdges.LEFT
				if intersection and not (side or ceil or floor):
					side = AABBEdges.CORNER
				collisions.append((wall, side))

	# print(collisions)

	for collision in collisions:
		AABB_collision_response(self.aabb, self.velocity, collision[0], collision[1], dt, len(collisions))

class Player(BasicPhysicsObject):
	def __init__(self, x: float, y: float):
		BasicPhysicsObject.__init__(self, x, y, collisions_handle)
		self.aabb = Rect(x, y, 32, 32)
		self.speed = .25

	def update(self, dt: float):
		self.velocity = Vector2(0, 0)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.velocity.y = -self.speed
		if keys[pygame.K_a]:
			self.velocity.x = -self.speed
		if keys[pygame.K_s]:
			self.velocity.y = self.speed
		if keys[pygame.K_d]:
			self.velocity.x = self.speed 

		if self.velocity != Vector2(0, 0): 
			self.velocity = self.velocity.normalize() * self.velocity.magnitude()

		self.aabb.x = int(self.position.x)
		self.aabb.y = int(self.position.y)
		BasicPhysicsObject.update(self, dt)

	def render(self):
		pygame.draw.rect(window.surface, (0, 0, 0, 255), self.aabb, width=1)