
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
        
    async def __authenticate(self):
        try:
            LOGIN_PATH = "/auth/login"

            _resp = requests.post(self.httpUri+LOGIN_PATH, json={
                "username": self.username,
                "password": self.password
            })

            if _resp.status_code != 200:
                if _resp.status_code == 404:
                    raise HostNotFoundException()

                raise CredentialException(f"Authentication failed: {self.uri}")

            _resp_json = _resp.json()
            self.authToken = _resp_json.get("auth-token", None)
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
    
    async def __connectToMB(self):
        """ Here, we will be creating a websocket connection"""
        WEBSOCKET_PATH = "/mb"
        if not self.isAuthenticated:
            await self.__authenticate()
            if not self.isAuthenticated:
                raise CredentialException("Unable to Authenticate, couldn't connect")

        headers = {
            "Authorization": self.authToken
        }

        try:
            self.socket = await websockets.connect(self.webUri+WEBSOCKET_PATH, additional_headers=headers)
            self.isConnected = await self.ping()
            return self.socket
        
        except Exception as _e:
            print(_e)
    
    def authAndConnect(self):
        asyncio.run(self.__connectToMB())

    async def ping(self):
        try:
            st = time.time()
            await self.socket.send("Ping")
            resp = await self.socket.recv()

            if resp == "Reply":
                timeTaken = time.time()-st
                print(f"Ping Successful - Time {timeTaken*100}ms")
                return True
            
            return False
        
        except websockets.exceptions.ConnectionClosedError:
            print("Websocket Disconnected")
            return False
        
        except Exception as _e:
            return False

    def __str__(self):
        if self.isConnected:
            return f"ConnectionObject-Connected:{self.isConnected}-{self.username}:{self.password}@{self.uri}"
        else:
            return f"ConnectionObject-Authenticated:{self.isAuthenticated}-{self.username}:{self.password}@{self.uri}"

client = MBClient(uri="localhost",
    username="guest", password="guest")

connection.authAndConnect()

print(connection)