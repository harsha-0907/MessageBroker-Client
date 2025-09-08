
import json
import time, asyncio, sys
import requests, socket, websockets
from mbexceptions import *

class MBClient:
    def __init__(self, uri: str, username: str, password: str, httpPort: int=42425, webPort: int = 42426, is_SSl: bool = False):
        self.uri = uri
        self.username = username
        self.password = password
        self.isAuthenticated = self.isConnected = False
    
        self.httpUri = "https://"+uri+f':{httpPort}' if is_SSl else "http://"+uri+f':{httpPort}'
        self.webUri = "wss://"+uri+f':{webPort}' if is_SSl else "ws://"+uri+f':{webPort}'
        
    # Auth & Connection Operations
    def __authenticate(self):
        try:
            LOGIN_PATH = "/auth/login"

            _resp = requests.post(self.httpUri+LOGIN_PATH, json={
                "username": self.username,
                "password": self.password
            })

            if _resp.status_code != 200:
                self.isAuthenticated = False
                if _resp.status_code == 404:
                    raise HostNotFoundException()

                raise CredentialException(f"Authentication failed: {self.uri}")

            _resp_json = _resp.json()
            self.authToken = _resp_json.get("auth-token", None)
            print(self.authToken)
            self.isAuthenticated = True

            if self.authToken is None:
                self.isAuthenticated = False
                raise UnknownException("Auth Token is invalid (None)")

        except socket.gaierror:
            # DNS resolution failed
            raise HostNotFoundException(f"Host not found: {self.uri}")

        except requests.exceptions.RequestException as e:
            # Request-level errors (connection refused, timeout, etc.)
            raise HostNotFoundException(f"Could not connect to host: {e}") from e
        
        except ConnectionRefusedError as _ce:
            print("Connection Refused by the Server")
        
        except Exception as _e:
            print(f"Caught Error {str(_e)}")        
    
    async def __initializeClient(self):
        """ Here, we will be creating a websocket connection"""
        WEBSOCKET_PATH = "/mb"
        if not self.isAuthenticated:
            # TO-DO - Can add authentication if required
            raise CredentialException("Client not Authenticated. Authenticate First")

        headers = {
            "Authorization": self.authToken
        }

        try:
            self.socket = await websockets.connect(self.webUri+WEBSOCKET_PATH, additional_headers=headers)
            await self.ping()
        
        except Exception as _e:
            print(_e)

    async def ping(self):
        """ Checks if the client can ping the server - Updates the status of `isConnected` """
        try:
            st = time.time()
            await self.socket.send("Ping")
            resp = await self.socket.recv()

            if resp == "Suii":
                timeTaken = time.time()-st
                print(f"Ping Successful - Time {timeTaken*100}ms")
                self.isConnected = True
            
            else:
                print("Unable to Ping the system - Wrong Reply")
                self.isConnected = False
        
        except websockets.exceptions.ConnectionClosedError:
            print("Websocket Disconnected")
            self.isConnected = False
        
        except Exception as _e:
            print(f"Exception {_e}")
            self.isConnected = False

        finally:
            return self.isConnected

    async def authAndConnect(self):
        self.__authenticate()
        await self.__initializeClient()

    # Client Defined Operations
    async def __sendMessage(self, data, ack):
        if not self.isConnected:
            raise CredentialException()
        
        await self.socket.send(data)
        if ack:
            resp = await self.socket.recv()
            return resp
    
    def __str__(self):
        if self.isConnected:
            return f"ConnectionObject-Connected:{self.isConnected}-{self.username}:{self.password}@{self.uri}"
        else:
            return f"ConnectionObject-Authenticated:{self.isAuthenticated}-{self.username}:{self.password}@{self.uri}"
    
    async def push(self, _message: str, exchange: str="", queues: list=[""], ack: bool = False):
        ACTION = "POST"
        message = {
            "action": ACTION,
            "exchange": exchange,
            "queues": queues, # Many
            "message": _message,
            "ack": ack
        }
        resp = await self.__sendMessage(json.dumps(message), ack)
        if ack:
            resp = json.loads(resp)
            if resp.get("error", False):
                statusCode = resp.get("statusCode", 600)
                errorMessage = resp.get("message")
                raise UnknownException(errorMessage)

            return resp.get("message")

    async def pull(self, exchange: str="", queue: str = ""):
        ACTION = "GET"
        if not isinstance(queue, str):
            raise UnknownException("Expects one queue, recieved list")

        message = {
            "action": ACTION,
            "exchange": exchange,
            "queues": [queue],
            "message": "",
            "ack": True
        }

        resp = json.loads(await self.__sendMessage(json.dumps(message), True))
        
        if resp.get("error", False):
            statusCode = resp.get("statusCode", 600)
            errorMessage = resp.get("message")
            raise UnknownException(errorMessage)

        return resp.get("message")

    async def close(self):
        await self.socket.close()
        print("Socket Closed")

