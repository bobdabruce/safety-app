# SafetyNomad AI - Phase 1

Your personal AI assistant.

## Quick Start

Open Terminal and run:
```
cd ~/safetynomad-ai
./start.sh
```

Then open in your browser:
- **On Mac**: http://localhost:8000
- **On Phone**: Use the IP address shown in Terminal

## Features (Phase 1)

- ✅ Chat interface (text + voice)
- ✅ Remembers conversations
- ✅ File organizer for Downloads folder
- ✅ Works on MacBook + phone

## Voice Input

Click the 🎤 button and speak. It will transcribe and send automatically.

## Organize Downloads

Say or type: "Organize my Downloads folder"

The AI will first PREVIEW what it would do. Then ask it to proceed if you approve.

## Your Data

- All data stored locally in `backend/memory.json`
- Nothing sent anywhere except Claude API for chat
- You can view memory: http://localhost:8000/api/memory
- You can clear memory: DELETE http://localhost:8000/api/memory
