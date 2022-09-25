import threading, websocket, bloxflip, random, base64, string, time, json, ssl, os
from websocket import create_connection
from bloxflip import  Authorization
from random import randbytes
from termcolor import cprint



class Main:
	def __init__(self):
		os.system("")
		# websocket.enableTrace(True)
		try:
			self.Setup()
			self.Spam()
		except Exception as e: 
			print(e)


	def print(self, message="", option=None): # print the ui's text with
		print("[ ", end="")
		if not option:
			cprint("AUTOBET", "magenta", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "magenta")
		elif option == "error":
			cprint("ERROR", "red", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "red")
		elif option == "warning":
			cprint("WARNING", "yellow", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "yellow")
		elif option == "yellow":
			cprint("AUTOBET", "yellow", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "yellow")
		elif option == "good":
			cprint("AUTOBET", "green", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "green")
		elif option == "bad":
			cprint("AUTOBET", "red", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "red")



	def Connect(self, auth):
		return create_connection("wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket", header={
												"Accept-Encoding": "gzip, deflate, br",
												"Accept-Language": "en-US,en;q=0.9",
												"Cache-Control": "no-cache",
												"Connection": "Upgrade",
												"Host": "sio-bf.blox.land",
												"Origin": "https://bloxflip.com",
												"Pragma": "no-cache",
												# "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
												"Sec-WebSocket-Key": str(base64.b64encode(randbytes(16)).decode('utf-8')),
												"Sec-WebSocket-Version": "13",
												"Upgrade": "websocket",
												"x-auth-token": auth,
												"Cookie": "__cf_bm=q3IhEUjTdruLw8J7qlMEsOoChcOSEMCrOz1wtbvJgLs-1663533789-0-AdUibmLxIDRluYADk0r13/arKvEfequiaQx4ZcPP5gXKreT1LE9DjS5JzmFq8xEb+kZplzWwtJLJufeZnndb6/U=; path=/; expires=Sun, 18-Sep-22 21:13:09 GMT; domain=.bloxflip.com; HttpOnly; Secure; SameSite=None",
												"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
										}, sslopt={"cert_reqs": ssl.CERT_NONE}, suppress_origin=True)
		


	def Setup(self):
		uiprint = self.print

		try:
			open("config.json", "r").close()
		except:
			uiprint("config.json file is missing. Make sure you downloaded all the files and they're all in the same folder", "error")

		with open("config.json", "r+") as data:
			try:
				config = json.load(data)
			except:
				uiprint("Invalid JSON format redownload file form github", "erorr")

			try:
				self.message = config["message"].replace("\\", "\\\\").replace('"', '\\"')
				print(self.message)
			except ValueError:
				uiprint("Invalid message inside JSON file. Must be string number", "error")
				time.sleep(1.6)
				exit()

			try:
				self.sleep = float(config["wait_time"])
			except ValueError:
				uiprint("Invalid wait time inside JSON file. Must be valid number", "error")
				time.sleep(1.6)
				exit()

			try:
				self.auths = config["authorization"]
			except ValueError:
				uiprint("Invalid authorization time inside JSON file. Must be valid string", "error")
				time.sleep(1.6)
				exit()



	def do_request(self, auth):
		message = self.message
		uiprint = self.print
		sleep = self.sleep

		while True:
			try:
				self.ws = self.Connect(auth)
				break
			except Exception as e:
				print(e)
				uiprint("Failed to connect to webserver. Retrying in 1.5 seconds...", "error")
				time.sleep(1.5)

		ws = self.ws
		uiprint("Connected to websocket successfully!", "good")


		ws.send("40/chat,")
		ws.send(f'42/feed,["auth","{auth}"]')
		ws.send(f'42/crash,["auth","{auth}"]')
		ws.send(f'42/chat,["auth", "{auth}"]')
		ws.send(f'42/wallet,["auth","{auth}"]')
		ws.send(f'42/jackpot,["auth","{auth}"]')
		ws.send(f'42/mode-queue,["auth","{auth}"]')
		ws.send(f'42/marketplace,["auth","{auth}"]')
		ws.send(f'42/cloud-games,["auth","{auth}"]')
		ws.send(f'42/case-battles,["auth","{auth}"]')

		for _ in range(3):
			if "notify-error" in str(ws.recv()):
				uiprint("Muted by moderator", "bad")
				return


		while True:
			self.c += 1
			try:
				ws.send(f'42/chat,["send-chat-message","{message}"]')
				uiprint(f"{self.c}:Sent message successfully!")
			except:
				uiprint("Failed to send message. Reconnecting to websocket.")
				time.sleep(1.5)
				ws = self.Connect()
				ws.send("40/chat,")
				ws.send(f'42/chat,["auth", "{auth}"]')
			time.sleep(sleep)
		
	

	def Spam(self):
		uiprint = self.print
		auths = self.auths

		self.c = 0
		for auth in auths:
			if not Authorization.validate(auth):
				uiprint(f"Invalid authorization", "error")
				continue
			threading.Thread(target=self.do_request, args=(auth,)).start()

if __name__ == "__main__":
	Main()