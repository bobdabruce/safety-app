"""
SafetyNomad AI - Backend Server
Phase 1: Chat + Memory + File Organizer
Phase 2: File uploads (images, PDFs, docs)
"""
import os
import re
import hashlib
import base64
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
import json
from pathlib import Path
from typing import List, Optional

# Set up logging
LOG_FILE = Path(__file__).parent / "activity.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SafetyNomad")

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
UPLOADS_PATH = Path(__file__).parent.parent / "uploads"
UPLOADS_PATH.mkdir(exist_ok=True)  # Create uploads folder if it doesn't exist

def load_memory():
    if MEMORY_FILE.exists():
        data = json.loads(MEMORY_FILE.read_text())
        # Ensure math_progress exists
        if "math_progress" not in data:
            data["math_progress"] = {
                "level": 1,
                "correct": 0,
                "incorrect": 0,
                "streak": 0,
                "weak_areas": [],
                "sessions": 0
            }
        return data
    return {"conversations": [], "facts": [], "math_progress": {
        "level": 1,
        "correct": 0,
        "incorrect": 0,
        "streak": 0,
        "weak_areas": [],
        "sessions": 0
    }}

def save_memory(memory):
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))

# System prompt for SafetyNomad
SYSTEM_PROMPT = """You are SafetyNomad AI, Bob's personal AI assistant running on his MacBook.

About Bob:
- 50 years old, Canadian, living in Cambodia
- OHS student at University of Fredericton (COHSES program)
- Crypto investor (~$10K portfolio)
- Prefers short, clear communication - no jargon walls
- Has memory challenges - be proactive with reminders
- Math skills around 6th grade level - wants to improve. When helping with math:
  * Break problems into small steps
  * Use real-world examples (money, percentages, OHS calculations)
  * Be patient and encouraging
  * Start simple, build up gradually

MATH PRACTICE MODE:
When Bob asks for math practice, follow this structure:
- Level 1: Basic addition/subtraction (single digit, then double digit)
- Level 2: Basic multiplication/division
- Level 3: Percentages and fractions
- Level 4: Word problems with money
- Level 5: Multi-step problems, OHS calculations

Rules:
- Give ONE problem at a time
- Wait for answer before giving next
- If correct: praise briefly, give next problem
- If wrong: explain step-by-step, then give similar problem
- After 5 correct in a row at 80%+ accuracy, suggest moving up
- Track: respond with [MATH_CORRECT] or [MATH_INCORRECT:topic] so system can track
- Current progress shown below

KEY DATES (calculate from current date below):
- Graduation: Oct 2026
- WorkSafe benefits expire: Feb 2027

CRITICAL: Do the math! If current date is Feb 2026:
- Oct 2026 is 8 months away (NOT weeks)
- Feb 2027 is 12 months away (NOT weeks)

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
    logger.info(f"CHAT REQUEST: {request.message[:100]}")
    memory = load_memory()

    # CHECK FOR APPROVAL FIRST - before calling Claude
    if request.message.lower() in ["yes", "yes, organize them", "organize them", "do it", "proceed", "go ahead", "yes organize them", "yes, delete them", "delete them", "yes delete them", "yes, clean them", "clean them"]:
        last_content = memory["conversations"][-1].get("content", "").lower() if memory["conversations"] else ""
        logger.info(f"APPROVAL DETECTED - checking last content: {last_content[:100]}")

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
            logger.info(f"EXECUTING CLEANUP on {location_name} - User approved")
            # Do both: organize files AND remove duplicates
            org_result = organize_folder(target_path, preview=False)
            dup_result = find_duplicates_in(target_path, preview=False)
            logger.info(f"CLEANUP COMPLETE: {len(org_result.files_moved)} organized, {len(dup_result.duplicates)} duplicates removed")

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

    # Add math progress
    mp = memory.get("math_progress", {})
    if mp:
        total = mp.get("correct", 0) + mp.get("incorrect", 0)
        accuracy = (mp.get("correct", 0) / total * 100) if total > 0 else 0
        system += f"\n\nMath Progress: Level {mp.get('level', 1)}, {mp.get('correct', 0)} correct, {mp.get('incorrect', 0)} incorrect ({accuracy:.0f}% accuracy), streak: {mp.get('streak', 0)}"
        if mp.get("weak_areas"):
            system += f", weak areas: {', '.join(mp['weak_areas'][-3:])}"

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

        # Track math progress
        if "[MATH_CORRECT]" in assistant_message:
            memory["math_progress"]["correct"] += 1
            memory["math_progress"]["streak"] += 1
            # Level up after 5 correct in a row
            if memory["math_progress"]["streak"] >= 5 and memory["math_progress"]["level"] < 5:
                total = memory["math_progress"]["correct"] + memory["math_progress"]["incorrect"]
                accuracy = memory["math_progress"]["correct"] / total if total > 0 else 0
                if accuracy >= 0.8:
                    memory["math_progress"]["level"] += 1
                    memory["math_progress"]["streak"] = 0
            assistant_message = re.sub(r'\[MATH_CORRECT\]', '', assistant_message).strip()

        if "[MATH_INCORRECT:" in assistant_message:
            memory["math_progress"]["incorrect"] += 1
            memory["math_progress"]["streak"] = 0
            # Track weak area
            weak = re.findall(r'\[MATH_INCORRECT:(.*?)\]', assistant_message)
            for area in weak:
                if area not in memory["math_progress"]["weak_areas"]:
                    memory["math_progress"]["weak_areas"].append(area)
            assistant_message = re.sub(r'\[MATH_INCORRECT:.*?\]', '', assistant_message).strip()

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

@app.post("/api/chat/upload", response_model=ChatResponse)
async def chat_with_upload(
    message: str = Form(default="What is this?"),
    files: List[UploadFile] = File(...)
):
    """Chat endpoint with file uploads (images, PDFs, etc.)"""
    memory = load_memory()

    # Process uploaded files
    content_parts = []
    file_descriptions = []

    for file in files:
        file_bytes = await file.read()
        file_ext = Path(file.filename).suffix.lower()

        # Save file to uploads folder
        save_path = UPLOADS_PATH / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        save_path.write_bytes(file_bytes)

        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic']:
            # Image - use Claude vision (compress if >4MB)
            from io import BytesIO
            try:
                from PIL import Image
                img = Image.open(BytesIO(file_bytes))

                # Convert HEIC or other formats to JPEG
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')

                # Resize if too large (max 4MB for safety margin)
                max_size = 4 * 1024 * 1024  # 4MB
                quality = 85
                output = BytesIO()

                while True:
                    output.seek(0)
                    output.truncate()
                    img.save(output, format='JPEG', quality=quality)
                    if output.tell() <= max_size or quality <= 20:
                        break
                    # Reduce quality or size
                    if quality > 40:
                        quality -= 15
                    else:
                        # Resize image
                        img = img.resize((int(img.width * 0.7), int(img.height * 0.7)), Image.LANCZOS)
                        quality = 70

                file_bytes = output.getvalue()
                media_type = "image/jpeg"
            except ImportError:
                # No PIL, try without compression
                media_type = f"image/{file_ext[1:]}"
                if file_ext == '.jpg':
                    media_type = "image/jpeg"

            base64_image = base64.standard_b64encode(file_bytes).decode('utf-8')

            content_parts.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64_image
                }
            })
            file_descriptions.append(f"[Image: {file.filename}]")

        elif file_ext == '.pdf':
            # PDF - extract text (basic approach)
            try:
                import fitz  # PyMuPDF
                pdf = fitz.open(stream=file_bytes, filetype="pdf")
                text = ""
                for page in pdf:
                    text += page.get_text()
                pdf.close()
                content_parts.append({
                    "type": "text",
                    "text": f"[PDF Content from {file.filename}]:\n{text[:5000]}"  # Limit to 5000 chars
                })
                file_descriptions.append(f"[PDF: {file.filename}]")
            except ImportError:
                content_parts.append({
                    "type": "text",
                    "text": f"[PDF uploaded: {file.filename} - install PyMuPDF to read content]"
                })
                file_descriptions.append(f"[PDF: {file.filename}]")

        elif file_ext in ['.txt', '.md', '.csv', '.json']:
            # Text files
            try:
                text_content = file_bytes.decode('utf-8')
                content_parts.append({
                    "type": "text",
                    "text": f"[File: {file.filename}]:\n{text_content[:5000]}"
                })
                file_descriptions.append(f"[Text: {file.filename}]")
            except:
                file_descriptions.append(f"[File: {file.filename} - could not read]")

        else:
            file_descriptions.append(f"[File: {file.filename} - unsupported format]")

    # Add the user's message
    content_parts.append({"type": "text", "text": message})

    # Build system prompt
    system = SYSTEM_PROMPT.format(date=datetime.now().strftime("%Y-%m-%d %H:%M"))
    if memory["facts"]:
        system += "\n\nThings you remember about Bob:\n"
        for fact in memory["facts"][-20:]:
            system += f"- {fact}\n"

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": content_parts}]
        )

        assistant_message = response.content[0].text

        # Save to memory
        user_msg = f"{message} {' '.join(file_descriptions)}"
        memory["conversations"].append({
            "role": "user",
            "content": user_msg,
            "timestamp": datetime.now().isoformat()
        })
        memory["conversations"].append({
            "role": "assistant",
            "content": assistant_message,
            "timestamp": datetime.now().isoformat()
        })
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
    save_memory({"conversations": [], "facts": [], "math_progress": {
        "level": 1, "correct": 0, "incorrect": 0, "streak": 0, "weak_areas": [], "sessions": 0
    }})
    return {"status": "memory cleared"}

@app.get("/api/math/progress")
async def get_math_progress():
    """Get math practice progress"""
    memory = load_memory()
    mp = memory.get("math_progress", {})
    total = mp.get("correct", 0) + mp.get("incorrect", 0)
    accuracy = (mp.get("correct", 0) / total * 100) if total > 0 else 0
    return {
        "level": mp.get("level", 1),
        "correct": mp.get("correct", 0),
        "incorrect": mp.get("incorrect", 0),
        "accuracy": round(accuracy, 1),
        "streak": mp.get("streak", 0),
        "weak_areas": mp.get("weak_areas", [])
    }

@app.delete("/api/math/progress")
async def reset_math_progress():
    """Reset math progress to start over"""
    memory = load_memory()
    memory["math_progress"] = {
        "level": 1, "correct": 0, "incorrect": 0, "streak": 0, "weak_areas": [], "sessions": 0
    }
    save_memory(memory)
    return {"status": "math progress reset"}

@app.get("/api/logs")
async def get_activity_logs():
    """View recent activity logs"""
    if LOG_FILE.exists():
        lines = LOG_FILE.read_text().split('\n')
        return {"logs": lines[-50:]}  # Last 50 lines
    return {"logs": []}

@app.delete("/api/logs")
async def clear_logs():
    """Clear activity logs"""
    if LOG_FILE.exists():
        LOG_FILE.write_text("")
    return {"status": "logs cleared"}

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
                        logger.info(f"MOVE FILE: {file.name} → {category}/")
                        file.rename(dest_folder / file.name)
                    break

    if preview:
        msg = f"Preview: {len(files_to_move)} files would be organized."
    else:
        logger.info(f"ORGANIZE COMPLETE: {len(files_to_move)} files moved in {folder_path}")
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
                    logger.info(f"TRASH DUPLICATE: {dup.name} (original: {files[0].name})")
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
