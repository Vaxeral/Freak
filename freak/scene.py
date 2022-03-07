from typing import Type
import pygame
from pygame.event import Event
from pygame import Rect
from player import Player

from window import instance as window

class Scene:
	def __init__(self, name: str):
		self.name: str = name
		self.manager: SceneManager = None  # type: ignore

	def handle_event(self, event: Event):
		pass

	def update(self, dt: float):
		pass 

	def render(self):
		pass

class SceneGame(Scene):
	def __init__(self, name):
		Scene.__init__(self, name)
		self.player = Player(128, 128 - 32)

	def update(self, dt: float):
		self.player.update(dt)

	def render(self):
		self.player.render()


class SceneManager:
	def __init__(self):
		self.scenes = dict()
		self.current_scene: Scene = None #  type: ignore

	def scene_switch(self, name: str):
		to_switch = self.scenes.get(name, None)
		assert to_switch, f"Scene with name, {name}, does not exist."
		self.current_scene = to_switch

	def scene_add(self, scene_type: Type[Scene], name: str, *args, **kwargs):
		assert self.scenes.get(name, None) is None, f"Scene with name, {name}, already exists."
		scene = scene_type(name, *args, *kwargs)
		scene.manager = self
		self.scenes[name] = scene
		if self.current_scene is None:
			self.current_scene = self.scenes[name]

	def scene_remove(self, name: str):
		self.scenes.pop(name)
		self.current_scene = None  # type: ignore

	def scene_clear(self):
		self.scenes.clear()
		self.current_scene = None  # type: ignore

instance = SceneManager()