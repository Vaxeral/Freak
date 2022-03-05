import math

def is_AABB_collision(a, b, v, dt):
	dx = v.x * dt
	dy = v.y * dt

	if dx > 0.0:
		enx = b.x - (a.x + a.w)
		exx = (b.x + b.w) - a.x
	else:
		enx = (b.x + b.w) - a.x
		exx = b.x - (a.x + a.w)

	if dy > 0.0:
		eny = b.y - (a.y + a.h)
		exy = (b.y + b.h) - a.y
	else:
		eny = (b.y + b.h) - a.y
		exy = b.y - (a.y + a.h)

	if dx == 0.0:
		entx = -math.inf
		extx = math.inf
	else:
		entx = enx / dx
		extx = exx / dx

	if dy == 0.0:
		enty = -math.inf
		exty = math.inf
	else:
		enty = eny / dy
		exty = exy / dy

	if entx > 1.0: entx = -math.inf
	if enty > 1.0: enty = -math.inf

	ent = max(entx, enty)
	ext = min(extx, exty)

	nx = 0
	ny = 0

	if ent > ext: 
		return 1.0, nx, ny

	if entx < 0.0 and enty < 0.0:
		return 1.0, nx, ny

	if entx < 0.0:
		if a.x + a.w <= b.x or a.x >= b.x + b.w:
			return 1.0, nx, ny

	if enty < 0.0:
		if a.y + a.h <= b.y or a.y >= b.y + b.h:
			return 1.0, nx, ny

	if entx > enty:
		if enx < 0.0:
			nx = 1.0
			ny = 0.0
		else:
			nx = -1.0
			ny = 0.0
	else:
		if eny < 0.0:
			nx = 0.0
			ny = 1.0
		else:
			nx = 0.0
			ny = -1.0

	return ent, nx, ny