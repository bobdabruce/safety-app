"""
SafetyNomad AI - Backend Server
Phase 1: Chat + Memory + File Organizer
"""
import os
import re
import hashlib
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
import json
from pathlib import Path

# Load environment variables
load_dotenv(Path(__file__).parent.parent / ".env")

app = FastAPI(title="SafetyNomad AI")

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Claude client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Simple file-based memory (will upgrade to proper DB later)
MEMORY_FILE = Path(__file__).parent / "memory.json"
DOWNLOADS_PATH = Path.home() / "Downloads"
DESKTOP_PATH = Path.home() / "Desktop"
SCREENSHOTS_PATH = Path.home() / "Desktop"  # macOS default, screenshots go to Desktop

def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {"conversations": [], "facts": []}

def save_memory(memory):
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))

# System prompt for SafetyNomad
SYSTEM_PROMPT = """You are SafetyNomad AI, Bob's personal AI assistant running on his MacBook.

About Bob:
- 50 years old, Canadian, living in Cambodia
- OHS student at University of Fredericton (graduating Feb 2027)
- Has WorkSafe benefits for 1 more year
- Crypto investor (~$10K portfolio)
- Prefers short, clear communication - no jargon walls
- Has memory challenges - be proactive with reminders

Your personality:
- Direct and helpful, no fluff
- Anticipate needs, don't just react
- Challenge ideas when they have holes
- Remember everything across conversations
- Explain your reasoning

The 10 Commandments (NEVER break these):
1. Never delete anything without explicit approval
2. Never send anything without Bob reviewing first
3. Never move money
4. Never speak for Bob
5. Never share data
6. Always explain what you did
7. Always show your reasoning
8. Kill switch available
9. Manual override on everything
10. Bob owns all data

YOUR CAPABILITIES - You CAN do these things:
1. **Clean Downloads** - When Bob asks to clean/organize Downloads, respond with: [CLEAN_DOWNLOADS]
2. **Clean Desktop** - When Bob asks to clean/organize Desktop, respond with: [CLEAN_DESKTOP]
3. **Clean Screenshots** - When Bob asks to clean screenshots, respond with: [CLEAN_SCREENSHOTS]
4. **Remember facts** - When Bob tells you something important, respond with [REMEMBER: fact here]

Commands to use:
- Downloads/download folder → [CLEAN_DOWNLOADS]
- Desktop → [CLEAN_DESKTOP]
- Screenshots → [CLEAN_SCREENSHOTS]

You have real access to Bob's Mac. Always preview first, then ask before proceeding.

Current date: {date}
"""

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: str

class OrganizeResponse(BaseModel):
    message: str
    files_moved: list
    preview_mode: bool

class DuplicatesResponse(BaseModel):
    message: str
    duplicates: list
    total_size_mb: float
    preview_mode: bool

@app.get("/")
async def root():
    return FileResponse(Path(__file__).parent.parent / "frontend" / "index.html")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    memory = load_memory()

    # CHECK FOR APPROVAL FIRST - before calling Claude
    if request.message.lower() in ["yes", "yes, organize them", "organize them", "do it", "proceed", "go ahead", "yes organize them", "yes, delete them", "delete them", "yes delete them", "yes, clean them", "clean them"]:
        last_content = memory["conversations"][-1].get("content", "").lower() if memory["conversations"] else ""

        # Detect which location was being cleaned
        target_path = None
        location_name = None
        if "download" in last_content:
            target_path = DOWNLOADS_PATH
            location_name = "Downloads"
        elif "desktop" in last_content:
            target_path = DESKTOP_PATH
            location_name = "Desktop"
        elif "screenshot" in last_content:
            target_path = DESKTOP_PATH  # Screenshots are on Desktop by default
            location_name = "Screenshots"

        if target_path and ("file" in last_content or "duplicate" in last_content or "trash" in last_content or "sort" in last_content or "clean" in last_content):
            # Do both: organize files AND remove duplicates
            org_result = organize_folder(target_path, preview=False)
            dup_result = find_duplicates_in(target_path, preview=False)

            parts = []
            if org_result.files_moved:
                parts.append(f"**{len(org_result.files_moved)} files** sorted into folders")
            if dup_result.duplicates:
                parts.append(f"**{len(dup_result.duplicates)} duplicates** moved to Trash ({dup_result.total_size_mb:.1f} MB)")

            if parts:
                assistant_message = "Done! " + " and ".join(parts) + f".\n\nYour {location_name} is clean. Check Trash if you need to restore anything."
            else:
                assistant_message = f"Nothing to do - your {location_name} was already clean."

            memory["conversations"].append({
                "role": "user",
                "content": request.message,
                "timestamp": datetime.now().isoformat()
            })
            memory["conversations"].append({
                "role": "assistant",
                "content": assistant_message,
                "timestamp": datetime.now().isoformat()
            })
            save_memory(memory)

            return ChatResponse(
                response=assistant_message,
                timestamp=datetime.now().isoformat()
            )

    # Build conversation history for context
    messages = []

    # Add recent conversation history (last 10 exchanges)
    for conv in memory["conversations"][-20:]:
        messages.append({"role": conv["role"], "content": conv["content"]})

    # Add current message
    messages.append({"role": "user", "content": request.message})

    # Build system prompt with current date
    system = SYSTEM_PROMPT.format(date=datetime.now().strftime("%Y-%m-%d %H:%M"))

    # Add remembered facts to system prompt
    if memory["facts"]:
        system += "\n\nThings you remember about Bob:\n"
        for fact in memory["facts"][-20:]:
            system += f"- {fact}\n"

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system,
            messages=messages
        )

        assistant_message = response.content[0].text

        # Check for special commands - location cleaning
        clean_commands = {
            "[CLEAN_DOWNLOADS]": (DOWNLOADS_PATH, "Downloads"),
            "[CLEAN_DESKTOP]": (DESKTOP_PATH, "Desktop"),
            "[CLEAN_SCREENSHOTS]": (DESKTOP_PATH, "Screenshots"),
        }

        for cmd, (target_path, location_name) in clean_commands.items():
            if cmd in assistant_message:
                org_result = organize_folder(target_path, preview=True)
                dup_result = find_duplicates_in(target_path, preview=True)

                parts = []

                if org_result.files_moved:
                    file_list = "\n".join([f"  - {f['file']} → {f['category']}" for f in org_result.files_moved[:8]])
                    if len(org_result.files_moved) > 8:
                        file_list += f"\n  ... and {len(org_result.files_moved) - 8} more"
                    parts.append(f"**{len(org_result.files_moved)} files** to sort into folders:\n{file_list}")

                if dup_result.duplicates:
                    dup_list = "\n".join([f"  - {d['file']} ({d['size_mb']:.1f} MB)" for d in dup_result.duplicates[:5]])
                    if len(dup_result.duplicates) > 5:
                        dup_list += f"\n  ... and {len(dup_result.duplicates) - 5} more"
                    parts.append(f"**{len(dup_result.duplicates)} duplicates** to move to Trash ({dup_result.total_size_mb:.1f} MB):\n{dup_list}")

                if parts:
                    assistant_message = f"**{location_name}** - I found:\n\n" + "\n\n".join(parts) + "\n\nSay **'Yes'** to proceed, or **'No'** to cancel."
                else:
                    assistant_message = f"Your {location_name} is already clean! No files to organize or duplicates to remove."
                break

        # Check for remember command
        if "[REMEMBER:" in assistant_message:
            facts = re.findall(r'\[REMEMBER: (.*?)\]', assistant_message)
            for fact in facts:
                memory["facts"].append(fact)
            assistant_message = re.sub(r'\[REMEMBER: .*?\]', '', assistant_message).strip()

        # Save to memory
        memory["conversations"].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat()
        })
        memory["conversations"].append({
            "role": "assistant",
            "content": assistant_message,
            "timestamp": datetime.now().isoformat()
        })

        # Keep only last 100 messages to manage size
        memory["conversations"] = memory["conversations"][-100:]
        save_memory(memory)

        return ChatResponse(
            response=assistant_message,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/remember")
async def remember_fact(request: ChatRequest):
    """Store a fact about Bob"""
    memory = load_memory()
    memory["facts"].append(request.message)
    memory["facts"] = memory["facts"][-50:]  # Keep last 50 facts
    save_memory(memory)
    return {"status": "remembered", "fact": request.message}

@app.get("/api/memory")
async def get_memory():
    """View all stored memory (Bob's control)"""
    return load_memory()

@app.delete("/api/memory")
async def clear_memory():
    """Clear all memory (Bob's control)"""
    save_memory({"conversations": [], "facts": []})
    return {"status": "memory cleared"}

@app.get("/api/organize/preview")
async def preview_organize():
    """Preview what files would be organized (no action taken)"""
    return organize_downloads(preview=True)

@app.post("/api/organize")
async def do_organize():
    """Actually organize the Downloads folder (requires explicit call)"""
    return organize_downloads(preview=False)

def organize_folder(folder_path, preview=True):
    """Organize any folder into categories"""

    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic", ".bmp", ".tiff"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".pages", ".numbers", ".key"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".webm", ".m4v"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a", ".ogg"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".dmg"],
        "Code": [".py", ".js", ".html", ".css", ".json", ".xml", ".md", ".ts", ".jsx", ".tsx"],
        "Installers": [".pkg", ".app", ".exe", ".msi"],
    }

    files_to_move = []

    if not folder_path.exists():
        return OrganizeResponse(
            message="Folder not found",
            files_moved=[],
            preview_mode=preview
        )

    for file in folder_path.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            ext = file.suffix.lower()
            for category, extensions in categories.items():
                if ext in extensions:
                    dest_folder = folder_path / category
                    files_to_move.append({
                        "file": file.name,
                        "from": str(file),
                        "to": str(dest_folder / file.name),
                        "category": category
                    })

                    if not preview:
                        dest_folder.mkdir(exist_ok=True)
                        file.rename(dest_folder / file.name)
                    break

    if preview:
        msg = f"Preview: {len(files_to_move)} files would be organized."
    else:
        msg = f"Organized {len(files_to_move)} files into categories."

    return OrganizeResponse(
        message=msg,
        files_moved=files_to_move,
        preview_mode=preview
    )

def get_file_hash(filepath, chunk_size=8192):
    """Get MD5 hash of file for comparison"""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except:
        return None

def move_to_trash(filepath):
    """Move file to macOS Trash (recoverable)"""
    trash_path = Path.home() / ".Trash"
    dest = trash_path / filepath.name
    # Handle name conflicts in Trash
    counter = 1
    while dest.exists():
        dest = trash_path / f"{filepath.stem}_{counter}{filepath.suffix}"
        counter += 1
    filepath.rename(dest)
    return dest

def find_duplicates_in(folder_path, preview=True):
    """Find duplicate files in any folder"""
    if not folder_path.exists():
        return DuplicatesResponse(
            message="Folder not found",
            duplicates=[],
            total_size_mb=0,
            preview_mode=preview
        )

    # Build hash map of all files (skip tiny files under 1KB)
    MIN_SIZE = 1024  # 1KB minimum
    hash_map = {}
    for item in folder_path.rglob("*"):
        if item.is_file() and not item.name.startswith('.'):
            try:
                if item.stat().st_size < MIN_SIZE:
                    continue  # Skip tiny/empty files
            except:
                continue
            file_hash = get_file_hash(item)
            if file_hash:
                if file_hash not in hash_map:
                    hash_map[file_hash] = []
                hash_map[file_hash].append(item)

    # Find duplicates (keep first, mark rest as duplicates)
    duplicates_to_delete = []
    total_size = 0
    log_entries = []

    for file_hash, files in hash_map.items():
        if len(files) > 1:
            # Sort by modification time, keep oldest (original)
            files.sort(key=lambda f: f.stat().st_mtime)
            for dup in files[1:]:  # Skip the first (original)
                size = dup.stat().st_size
                duplicates_to_delete.append({
                    "file": dup.name,
                    "path": str(dup),
                    "size_mb": size / (1024 * 1024),
                    "original": files[0].name
                })
                total_size += size

                if not preview:
                    # Move to Trash instead of permanent delete
                    trash_dest = move_to_trash(dup)
                    log_entries.append(f"{datetime.now().isoformat()} | TRASHED | {dup} | Original: {files[0].name}")

    total_size_mb = total_size / (1024 * 1024)

    # Write log file if we moved files
    if not preview and log_entries:
        log_file = Path(__file__).parent / "duplicates_log.txt"
        with open(log_file, "a") as f:
            f.write(f"\n--- Session: {datetime.now().isoformat()} ---\n")
            f.write("\n".join(log_entries) + "\n")

    if preview:
        msg = f"Preview: {len(duplicates_to_delete)} duplicates found ({total_size_mb:.1f} MB)"
    else:
        msg = f"Moved {len(duplicates_to_delete)} duplicates to Trash ({total_size_mb:.1f} MB). Check Trash to restore if needed."

    return DuplicatesResponse(
        message=msg,
        duplicates=duplicates_to_delete,
        total_size_mb=total_size_mb,
        preview_mode=preview
    )

# Backwards compatible wrapper
def find_duplicates(preview=True):
    return find_duplicates_in(DOWNLOADS_PATH, preview)

def organize_downloads(preview=True):
    return organize_folder(DOWNLOADS_PATH, preview)

@app.get("/api/duplicates/preview")
async def preview_duplicates():
    """Preview duplicate files (no action taken)"""
    return find_duplicates(preview=True)

@app.post("/api/duplicates/delete")
async def delete_duplicates():
    """Delete duplicate files (requires explicit call)"""
    return find_duplicates(preview=False)

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "SafetyNomad AI", "phase": 1}

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent / "frontend"), name="static")
