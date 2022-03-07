import math
from typing import Union

from pygame.rect import Rect as Rect
from pygame.math import Vector2 as Vector2

def AABB_point_collision(
	ax: Union[float, int], 
	ay: Union[float, int], 
	aw: Union[float, int], 
	ah: Union[float, int],
	bx: Union[float, int],
	by: Union[float, int],
	dx: Union[float, int],
	dy: Union[float, int],
	dt: float):

	dx *= dt
	dy *= dt

	if dx > 0.0:
		entryx = bx - (ax + aw)
		exitx = bx - ax
	else:
		entryx = bx - ax
		exitx = bx - (ax + aw)

	if dy > 0.0:
		entryy = by - (ay + ah)
		exity = by - ay
	else:
		entryy = by - ay
		exity = by - (ay + ah)

	if dx == 0.0:
		entrytx = -math.inf
		exittx = math.inf
	else:
		entrytx = entryx / dx
		exittx = exitx / dx

	if dy == 0.0:
		entryty = -math.inf
		exitty = math.inf
	else:
		entryty = entryy / dy
		exitty = exity / dy

	if entrytx > 1.0: entrytx = -math.inf
	if entryty > 1.0: entryty = -math.inf

	ent = max(entrytx, entryty)
	ext = min(exittx, exitty)

	nx = 0
	ny = 0

	if ent > ext: 
		return 1.0, nx, ny

	if entrytx < 0.0 and entryty < 0.0:
		return 1.0, nx, ny

	if entrytx < 0.0:
		if ax + aw <= bx or ax >= bx:
			return 1.0, nx, ny

	if entryty < 0.0:
		if ay + ah <= by or ay >= by:
			return 1.0, nx, ny

	if entrytx > entryty:
		if entryx < 0.0:
			nx = 1.0
			ny = 0.0
		else:
			nx = -1.0
			ny = 0.0
	else:
		if entryy < 0.0:
			nx = 0.0
			ny = 1.0
		else:
			nx = 0.0
			ny = -1.0

	return ent, nx, ny

def is_AABB_collision(a, b, v, dt):
	dx = v.x * dt
	dy = v.y * dt

	if dx > 0.0:
		entryx = bx - (ax + aw)
		exitx = (bx + bw) - ax
	else:
		entryx = (bx + bw) - ax
		exitx = bx - (ax + aw)

	if dy > 0.0:
		entryy = by - (ay + ah)
		exity = (by + bh) - ay
	else:
		entryy = (by + bh) - ay
		exity = by - (ay + ah)

	if dx == 0.0:
		entrytx = -math.inf
		exittx = math.inf
	else:
		entrytx = entryx / dx
		exittx = exitx / dx

	if dy == 0.0:
		entryty = -math.inf
		exitty = math.inf
	else:
		entryty = entryy / dy
		exitty = exity / dy

	if entrytx > 1.0: entrytx = -math.inf
	if entryty > 1.0: entryty = -math.inf

	ent = max(entrytx, entryty)
	ext = min(exittx, exitty)

	nx = 0
	ny = 0

	if ent > ext: 
		return 1.0, nx, ny

	if entrytx < 0.0 and entryty < 0.0:
		return 1.0, nx, ny

	if entrytx < 0.0:
		if ax + aw < bx or ax > bx + bw:
			return 1.0, nx, ny

	if entryty < 0.0:
		if ay + ah < by or ay > by + bh:
			return 1.0, nx, ny

	if entrytx > entryty:
		if entryx < 0.0:
			nx = 1.0
			ny = 0.0
		else:
			nx = -1.0
			ny = 0.0
	else:
		if entryy < 0.0:
			nx = 0.0
			ny = 1.0
		else:
			nx = 0.0
			ny = -1.0

	return ent, nx, ny
