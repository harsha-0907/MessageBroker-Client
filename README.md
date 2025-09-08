# 📡 Message Broker Client - SwitchMQ

A simple and lightweight **client module** to communicate with the [Custom Message Broker](https://github.com/your-username/broker-repo) — enabling easy integration with producer and consumer applications.

This client is designed to provide:
- 🧵 **Simple APIs** to publish and consume messages
- ⚡ **Fast communication** with the broker
- 🧱 A clean foundation to build language-specific SDKs or microservices around the broker

> Built alongside the [Custom Message Broker](https://github.com/your-username/broker-repo) as part of the MVP-1 release.

---

## ⚙️ What It Does

- 📤 Send messages to queues (Producer)
- 📥 Receive messages from queues (Consumer)
- 📡 Communicates with the broker over **HTTP&Websocket**

---

## ✨ Features

- [x] Connect to the broker and maintain session
- [x] Publish messages to a named queue
- [x] Consume messages from a queue
- [x] Basic error handling — with clear exceptions for debugging
- [ ] Message acknowledgment (coming soon)
- [ ] Retry logic and delivery guarantees (coming soon)

### 📝 Note

> This client is designed to be easily integrated into your existing application — **non-blocking and async-friendly**, so you can publish and consume messages without disrupting your main workflow or thread.

## 📦 Installation

1. Clone the repository git clone `https://github.com/harsha-0907/MessageBroker-Client.git`
2. Change directory to the repository `cd MessageBroker-Client`
3. Create Virtual Environment `python3 -m venv .venv`
4. Activate the virtual environment: \
    a. For Linux `source .venv/bin/activate` \
    b. For Windows `..venv\Scripts\activate` 
5. Install the necessary packages using `pip install -r requirments.txt`


