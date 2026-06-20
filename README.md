# SARVIS-PC

A voice-controlled AI desktop assistant inspired by the concept of JARVIS from Iron Man. This project focuses on building a practical, local-first AI assistant capable of understanding natural language, executing system commands, and evolving into a fully autonomous desktop companion.

> **Status:** 🚧 Phase 1 – Core Voice Assistant (Under Active Development)

---

## ✨ Features

- 🎙️ Wake-word activation
- 🗣️ Offline speech-to-text using OpenAI Whisper
- 🧠 Natural language command understanding using a local LLM (Llama 3 via Ollama)
- 🎯 Intent-based command parsing
- 🚀 Application launching
- 🔊 Voice feedback using Text-to-Speech
- 🛡️ Safe command validation before execution
- 🧩 Modular architecture for future expansion

---

## 🏗️ Architecture

```text
Wake Word
      │
      ▼
Speech Recognition (Whisper)
      │
      ▼
Natural Language Command
      │
      ▼
Local LLM (Llama 3)
      │
      ▼
Intent Parser
      │
      ▼
Command Validator
      │
      ▼
Desktop Action
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| Speech Recognition | OpenAI Whisper |
| Wake Word Detection | OpenWakeWord |
| Local LLM | Llama 3 (Ollama) |
| Text-to-Speech | pyttsx3 |
| Command Execution | Python subprocess |
| Operating System | Windows |

---

## 💬 Example Commands

```text
Open Edge
```

```text
Open Notepad
```

```text
Open Calculator
```

```text
What time is it?
```

```text
Shutdown the computer
```

---

## 📂 Project Structure

```text
Sarvis-PC/
│
├── assistant.py
├── wake_word.py
├── speech.py
├── llm.py
├── intent_parser.py
├── executor.py
├── config.py
├── apps.py
├── utils/
├── models/
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Sarvis-PC.git
cd Sarvis-PC
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download and install Ollama from the official website.

Then pull the Llama 3 model:

```bash
ollama pull llama3:8b
```

---

## ▶️ Running the Assistant

```bash
python assistant.py
```

Wait for the wake word.

Example:

```text
Hey Sarvis
```

Then speak your command naturally.

---

# 🗺️ Development Roadmap

## ✅ Phase 1 – Core Voice Assistant

- [x] Wake-word detection
- [x] Offline Speech-to-Text (Whisper)
- [x] Local LLM integration
- [x] Intent parsing
- [x] Application launcher
- [x] Voice responses

---

## 🚀 Phase 2 – Smarter Command Engine

- [ ] Fuzzy application matching
- [ ] Multi-command execution
- [ ] Browser automation
- [ ] File management
- [ ] Weather
- [ ] Clipboard management
- [ ] Notes
- [ ] Calendar

---

## 🤖 Phase 3 – Personal AI

- [ ] Long-term memory
- [ ] User preferences
- [ ] Local knowledge base
- [ ] Conversational dialogue
- [ ] Plugin system

---

## ⚡ Phase 4 – Desktop Intelligence

- [ ] GUI Dashboard
- [ ] Animated assistant interface
- [ ] Smart notifications
- [ ] OCR
- [ ] Vision support
- [ ] Face recognition

---

## 🧠 Phase 5 – Autonomous Assistant

- [ ] Task planning
- [ ] Workflow automation
- [ ] AI agents
- [ ] Multi-agent architecture
- [ ] Autonomous execution

---

# 🎯 Long-Term Goal

The vision is to build a **fully local AI desktop assistant** capable of:

- Understanding natural language
- Controlling the operating system
- Remembering user preferences
- Automating repetitive tasks
- Executing multi-step workflows
- Running with minimal cloud dependency

---

## ⚠️ Disclaimer

This project is developed for educational and research purposes. It is an independent open-source project inspired by AI desktop assistants and is **not affiliated with Marvel Studios or Iron Man**.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Sowrin Paul**

*"Building a real-world AI desktop assistant, one phase at a time."*
