from pygame import Rect, Vector2
import pygame

from physics import AABBEdges, BasicPhysicsObject, AABB_collision_response, is_AABB_intersection
from window import instance as window

def collisions_handle(self, dt):
	wall = Rect(0, 400, 640, 32)


	rect = Rect(self.position.x + self.velocity.x * dt, self.position.y + self.velocity.y * dt, self.aabb.w, self.aabb.h)

	intersection = is_AABB_intersection(rect, wall)

	if intersection:
		AABB_collision_response(self.aabb, self.velocity, wall, AABBEdges.TOP, dt)

	wall = Rect(100, 0, 32, 300)

	intersection = is_AABB_intersection(rect, wall)

	if intersection:
		AABB_collision_response(self.aabb, self.velocity, wall, AABBEdges.LEFT, dt)

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