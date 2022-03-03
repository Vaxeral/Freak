from typing import Type
from pygame.event import Event
from player import Player

class Scene:
	def __init__(self, name: str, manager):
		self.name = name
		self.manager = manager

	def event_handle(self, event: Event):
		pass

	def update(self, dt: float):
		pass

	def render(self):
		pass

class SceneGame(Scene):
	def __init__(self, name: str, manager):
		Scene.__init__(self, name, manager)
		self.player = Player(0, 0)

	def update(self, dt: float):
		self.player.update(dt)

	def render(self):
		self.player.render()

class SceneManager:
	def __init__(self):
		self.scenes = dict()
		self.current_scene = None

	def scene_switch(self, name: str):
		to_switch = self.scenes.get(name, None)
		assert to_switch, f"Scene with name, {name}, does not exist."
		self.current_scene = to_switch

	def scene_add(self, scene_type: Type[Scene], name: str, *args, **kwargs):
		scene = scene_type(name, *args, *kwargs)
		assert self.scenes.get(name, None) is None, f"Scene with name, {name}, already exists."
		self.scenes[name] = scene
		if self.current_scene is None:
			self.current_scene = self.scenes[name]

	def scene_remove(self, name: str):
		self.scenes.pop(name)
		self.current_scene = None

	def scene_clear(self):
		self.scenes.clear()
		self.current_scene = None

	def current_scene_run(self, name, *args, **kwargs):
		method = getattr(self.current_scene, name, None)
		if method: method(*args, **kwargs)

instance = SceneManager()