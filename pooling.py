from threading import Thread
from time import sleep
from typing import Callable

from telegram_api import Update, API


class Pooling:
	def __init__(self, api, handler: Callable[[Update], None], update_time: float = 5):
		self.__api: API = api
		self.__handler: Callable[[Update], None] = handler
		self.__update_time: float = update_time
		self.__pooling: [Thread, None] = None
		self.__lastUpdate: int = 0
		self.__isRunning = False

	def start(self):
		if self.__pooling:
			raise RuntimeError("[Pooling] already running")

		self.__isRunning = True
		self.__pooling = Thread(target=self.__request_update)
		self.__pooling.start()

		return self

	def stop(self):
		if not self.__pooling:
			raise RuntimeError("[Pooling] not running")

		self.__isRunning = False

	def __request_update(self):
		print("[Pooling] started")
		while self.__isRunning:
			self.__do_request()

			# try:
			# 	self.__do_request()
			# except Exception as ex:
			# 	print("[Pooling] got exception", ex)
			sleep(self.__update_time)
		self.__pooling = None
		print("[Pooling] stopped")

	def __do_request(self):
		updates = self.__api.get_updates(offset=self.__lastUpdate)
		for update in updates:
			self.__lastUpdate = update.update_id + 1
			self.__handler(update)