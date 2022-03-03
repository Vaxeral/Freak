import pygame

class Window:
	def __init__(self, width, height, caption) -> None:
		pygame.display.set_caption(caption)
		pygame.display.set_mode((width, height), pygame.RESIZABLE)
		self.surface = pygame.display.get_surface()
		self.fill = (255, 255, 255, 255)

	def handle_event(self, event: pygame.event.Event) -> None:
		if event.type == pygame.WINDOWCLOSE:
			game = getattr(self, "game", None)
			if game:
				game.is_running = False
	

instance = Window(640, 480, "Freak")