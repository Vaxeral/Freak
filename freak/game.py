import pygame

from window import instance as window
from scene import instance as scene_manager

clock = pygame.time.Clock()

class Game:
	def __init__(self) -> None:
		self.is_running = False
		self.frame_rate = 60
		setattr(window, "game", self)

	def event_handle(self, event: pygame.event.Event) -> None:
		if event.type == pygame.QUIT:
			self.is_running = False
		window.handle_event(event)
		scene_manager.current_scene_run("event_handle", event)

	def update(self, dt: int) -> None:
		scene_manager.current_scene_run("update", dt)

	def render(self) -> None:
		window.surface.fill(window.fill)

		scene_manager.current_scene_run("render")

		pygame.display.update()

	def run(self) -> None:
		self.is_running = True
		while self.is_running:
			for event in pygame.event.get():
				self.event_handle(event)

			dt = clock.tick(self.frame_rate)

			self.update(dt)
			self.render()