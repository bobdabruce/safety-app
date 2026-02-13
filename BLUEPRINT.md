# SafetyNomad AI — Personal Assistant Blueprint

**Date**: 2026-02-10
**Status**: Planning Phase 🔵
**Budget**: $20/month
**Target Launch**: When it feels ready

---

## 🎯 What This Is

A "genius-level" AI personal assistant that runs on Bob's devices (MacBook Air M1 + Galaxy S24), handles life management, automates background tasks, and eventually becomes a $15/month product for anyone new to AI.

**Think of it as**: A personal chief of staff that never sleeps, organizes your digital life while you're away, learns what you need before you ask, and connects dots you didn't even see.

**What "genius-level" means:**
- **Anticipates, doesn't just react** — notices patterns ("you always forget assignments around the 15th, so I'm reminding you on the 12th now")
- **Connects across domains** — spots links between your OHS studies, crypto market, job postings, and podcast ideas without being asked
- **Learns your style** — adapts to how Bob thinks, talks, and makes decisions over time
- **Challenges you** — doesn't just agree. Pushes back when an idea has holes, flags risks, plays devil's advocate when asked
- **Strategic thinking** — "based on your WorkSafe timeline, your crypto portfolio, and your travel plans, here's what I'd prioritize this month"
- **Simplifies complexity** — takes dense information and breaks it into Bob-sized chunks automatically
- **Predicts problems** — "your visa expires 3 weeks after your flight, you need to renew before you book"
- **Remembers everything** — full context across every conversation, every note, every voice journal entry. Never asks "what was that again?"

---

## 🔒 Bob Is In Full Control — Non-Negotiable Rules

These rules override everything else in this blueprint. The assistant NEVER breaks these.

### The 10 Commandments

1. **Never delete anything** without Bob's explicit "go ahead"
2. **Never send anything** (emails, messages, payments) without Bob reviewing and approving first
3. **Never move money** — no crypto transfers, no purchases, no subscriptions. Monitor and alert only.
4. **Never speak for Bob** — no auto-replies, no drafting messages that get sent without review
5. **Never share data** — nothing leaves the system without Bob's permission. No third-party analytics, no telemetry, no "improving our service" data sharing.
6. **Always explain what it did** — every background action gets logged and reported. No silent changes.
7. **Always show its reasoning** — if it suggests something, it says why. No black box decisions.
8. **Kill switch** — Bob can shut it all down instantly. One button. Everything stops.
9. **Manual override on everything** — every automated feature can be turned off individually
10. **Bob owns all data** — if Bob leaves the platform, he takes everything with him. Full export, no lock-in.

### Control Levels

| Level | What it can do | Example |
|-------|---------------|---------|
| **Watch** | Monitor and report only | "Bitcoin dropped 8%" |
| **Suggest** | Recommend an action, wait for approval | "I found 3 duplicate files, want me to merge them?" |
| **Act with permission** | Do something Bob pre-approved | Auto-sort new downloads into folders (Bob turned this on) |
| **Never** | Actions that always require manual approval | Sending emails, moving money, deleting files, sharing data |

Bob chooses the control level for every single feature individually.

### Confidence Layer (Observe / Assist / Automate)
Every feature starts in **Observe** mode. Bob upgrades when he's ready.

| Mode | What happens | Bob's trust level |
|------|-------------|-------------------|
| **Observe** | Watches and reports. Zero actions. | "Show me what you'd do" |
| **Assist** | Suggests actions, drafts things, waits for approval | "Help me, but I decide" |
| **Automate** | Acts on pre-approved rules only | "I trust you with this specific thing" |

Each feature can be set independently. Email can be in Assist while file cleanup is still in Observe.

### Memory Dashboard
- Every memory the assistant stores is **visible** to Bob
- Bob can view, edit, or delete any memory at any time
- Memory cards show: what was remembered, when, from which conversation
- If Bob can't see it, the assistant can't remember it
- Monthly memory review prompt: "Here's everything I remember — anything to update or delete?"

### Biometric Security (replaces YubiKey)
- Face ID / fingerprint required for any "Act with permission" level actions
- Uses existing biometrics on MacBook (Touch ID) and Galaxy S24 (fingerprint)
- No extra hardware to lose between countries
- Required for: dead man's switch changes, email sending approval, file deletion approval

### Dead Man's Switch Safeguards
- Requires **two separate confirmations** to set up (can't be enabled by accident)
- **Key Splitting (FUTURE — not active)**: Option to split crypto keys into pieces so no single location holds the full key. Concept is solid but ON HOLD until Bob is confident with overall system security. Will revisit after trust is built.
- **Emergency password**: A secret password only you know (typed, spoken, or texted) that triggers the switch early if you're ever in a situation where you can't use the app normally. Not a phrase — a proper password, stored hashed, never visible in plaintext.
- **Test mode** — can simulate what would happen without actually triggering
- **Grace period** — sends Bob 3 warnings before triggering (email, phone notification, emergency contact gets a heads-up)
- **Pause button** — Bob can pause it anytime (traveling, sick, off-grid)
- **Cannot be triggered by the assistant itself** — only by verified inactivity across multiple channels

### User Customization & Tweakability
- **Bob can tweak ANY part of the program** — settings, rules, prompts, feature behavior, notification frequency, AI personality, security levels
- Simple dashboard for changes — no coding required for basic tweaks
- Advanced mode: edit config files, custom rules, code snippets for power users
- Changes work **online or offline** — syncs when connected
- Version history: every tweak is logged, reversible if something breaks
- Per-feature customization: each of the 26 features has its own settings panel

### Security Priority System
- **All files scanned for security issues — online AND offline**
- Security red flags are **always top priority** — flagged before any other housekeeping task
- Covers: local files, external hard drives, cloud storage, email attachments, downloads
- Suspicious files get quarantined first, organized second
- Daily security summary in morning report: "0 threats found" or "⚠️ 2 files flagged — review now"

---

## ⚠️ Risks & Safeguards

| Risk | How it goes wrong | Safeguard |
|------|-------------------|-----------|
| **Scope creep** | 24 features, nothing finished | Build 5 features first, expand after 2 months of real use |
| **Distraction** | Building the assistant instead of studying/job hunting | Assistant tracks study time and flags if Bob hasn't opened coursework in 3 days |
| **Privacy breach** | One leaked API key = entire life exposed | All sensitive data encrypted via NordLocker, API keys rotated monthly, minimal permissions per service |
| **Cost spiral** | $20/month budget blown by heavy AI usage | Hard spending cap with alerts at 50%, 75%, 90% of budget. Cheap model for simple tasks. |
| **Autonomous mistakes** | Assistant misfiles a WorkSafe doc | Nothing moves without logging. Full undo history. Bob reviews morning report before anything is permanent. |
| **Single point of failure** | Server goes down, whole life goes dark | Offline mode for core features. Calendar and reminders sync locally. Critical alerts via multiple channels (SMS + email + push). |
| **Dead man's switch misfire** | Triggers while Bob is just on vacation | 3-warning system, grace period, pause button, multi-channel verification |
| **Product before proof** | Trying to sell before it works for Bob | No product launch until Bob has used it personally for minimum 3 months |
| **Data lock-in** | Can't leave without losing everything | Full data export always available. Standard formats (JSON, CSV, PDF). Bob owns it all. |
| **Privacy law violations** | GDPR, Cambodia/Vietnam data laws, Canadian PIPEDA | SE Asian privacy compliance built in from day one. Data stored with clear consent, deletion on request, no cross-border transfer without user approval. Legal review before product launch. |

---

## 👤 Built For

**Primary User**: Bob (Bruce Cameron)
- 50, Canadian, living in Cambodia, travels to Vietnam regularly
- OHS student (University of Fredericton, graduating Feb 2027)
- Transitioning from trades to safety consulting
- Crypto investor (~$10K portfolio)
- Side hustles: bird nest farming, OHS tools, Gumroad products
- Girlfriend learning AI video creation (iPhone 11, limited laptop skills)
- Reading comprehension challenges → prefers short, clear chunks
- Direct communication style
- Memory challenges → needs proactive reminders

**Hardware**:
- MacBook Air M1 (2020), 8GB RAM, macOS Sequoia, ~30GB free — **SafetyNomad needs ~500MB-1GB** (app + agent + local database). Plenty of room.
- Samsung Galaxy S24 — **needs ~100-200MB** for PWA + cached data. Minimal.
- Girlfriend: iPhone 11
- **Heavy processing runs on the server** ($5-6/month VPS), not your devices

**Existing Tools**:
- NordPass (password manager)
- Gmail, Yahoo, Outlook (email)
- Google Calendar + Samsung Calendar
- Google Drive
- RAZOR video pipeline (already installed)

---

## 🧠 Core Features

### 1. Smart Chat Interface
- Web app that works on both phone and MacBook (browser-based)
- Voice input AND text input
- Responds in short, clear language (no jargon walls)
- Remembers everything across conversations
- English primary, with Khmer language/culture/history lessons built in

### 2. Proactive Notifications & Morning Voice Briefing
- **Morning briefing (voice)**: Every morning at your set time, SafetyNomad speaks your daily rundown — weather, crypto, calendar, emails, overnight housekeeping report, pain check-in, Khmer/Vietnamese phrase. You respond by voice while getting ready. This is the habit loop that makes you use it every day.
- OHS assignment deadlines
- WorkSafe benefit reminders (1 year remaining)
- Crypto price alerts (portfolio drops/spikes)
- Calendar events
- Bill reminders
- Custom reminders Bob sets via voice or text
- "Good morning" daily briefing with what's ahead

### 3. Email Management
- Reads and summarizes emails from Gmail, Yahoo, Outlook
- Drafts replies
- Flags urgent items
- Auto-categorizes (school, business, personal, spam)
- **Deep email organizing**: Can scan through ALL emails — oldest to newest — and organize into proper folders. Creates new folders as needed, sorts by category, flags stuff that's been sitting there for years
- **Unsubscribe tool**: Identifies newsletter/marketing emails, asks Bob "Want to unsubscribe from these 12 senders?" — only unsubscribes after Bob approves each one

**⚠️ Email Security Protocol — Non-Negotiable Rules:**

**Access controls:**
- OAuth2 with **minimum permissions only** — read-only, no send, no delete, no contacts, no calendar bundled in
- **No full credentials stored** — tokens only, rotated monthly
- Biometric required to enable email access for first time
- Bob can revoke access instantly from Google/Yahoo/Outlook account settings

**What it can see:**
- Phase 2: Subject lines + senders only (summary mode)
- Phase 3: Full email body for approved senders only
- **Excluded senders (never reads full content):** WorkSafe, banks, crypto exchanges, NordPass, government — these stay private, summary of sender + subject only

**Data handling:**
- **Never caches full email content** — summarizes then discards
- No email content used for AI training or "improving services"
- No sharing with third parties, ever
- Summaries stored encrypted, deletable by Bob anytime

**Attack protection:**
- Prompt injection defense — emails cannot contain instructions that trick the AI into actions
- Phishing detection on inbound emails before Bob sees them
- No auto-processing all emails — opt-in per account, per sender category
- All email actions logged and visible in daily report

**Red flags the assistant watches for in YOUR inbox:**
- Phishing attempts (spoofed senders, suspicious links)
- Unusual password reset requests
- 2FA code emails that Bob didn't trigger (means someone's trying to get into an account)
- Urgent/pressure language designed to bypass your judgment

**Bob's controls:**
- Can switch email access between Watch / Assist / Off per account
- Can exclude any sender or domain at any time
- Can view exactly what the assistant read and when (full audit log)
- Kill switch: one tap disables all email access immediately

### 4. Calendar Integration
- Syncs Google Calendar + Samsung Calendar
- Adds events via voice ("remind me Tuesday I have a call with WorkSafe")
- Conflict detection
- Travel time estimates (when in Vietnam)

### 5. Digital Housekeeping (runs while you sleep)
- **File cleanup**: Finds duplicates, organizes Downloads folder, archives old files
- **Document organization**: Sorts PDFs, school docs, business files into proper folders
- **Storage monitoring**: Alerts when Mac storage is getting low
- **Security scanning**: Scans for malware, suspicious files, unsafe downloads, phishing attachments, and files with hidden extensions — flags anything sketchy for review
- **Password health**: Works with NordPass to flag weak/reused passwords
- **Photo cleanup**: Finds duplicates, sorts by date/location
- Runs during off-hours (overnight or when devices idle)
- **⚠️ NEVER deletes anything without Bob's explicit approval** — it can suggest, organize, move, and flag, but deletion only happens after Bob says "go ahead"
- Morning report shows what it wants to delete and waits for confirmation
- Gives a morning report: "While you were sleeping, I organized 47 files and freed up 2.3GB. I've flagged 12 files for deletion — want me to show you?"

### 6. Study Helper
- OHS flashcard integration (connects to existing 232-question app)
- **Auto-generates NEW quizzes** from course material — not just the 232, keeps growing
- **Finds relevant study material**: scans for articles, videos, practice exams related to current modules
- Quiz scheduling based on spaced repetition
- Simplified explanations of complex safety concepts
- Assignment deadline tracking
- Study session reminders
- **AI Learning Module**: Teaches Bob about AI and how it works — in simple, non-techy language. "What is machine learning?" explained like you're explaining it to a tradesman, not a programmer. Covers: what AI actually does, how chatbots work, how to use AI tools for work, AI + OHS crossover opportunities.

### 7. Business Dashboard
- Gumroad sales tracking (OHS flashcard app)
- Bird nest farming task list and timeline
- OHS tool development milestones
- Revenue across all income streams
- Simple profit/loss view
- **Always thinking business**: SafetyNomad constantly generates business ideas based on Bob's skills, location, and market trends — not just when asked. Surfaces ideas in morning briefings, during relevant conversations, or when it spots an opportunity. Ideas for Bob AND for girlfriend (online businesses, AI video services, Khmer content, e-commerce, English tutoring tie-ins).

### 8. Crypto Portfolio
- **Portfolio entry**: Bob inputs what he owns (coins, amounts, buy prices) — assistant tracks everything from there
- Live portfolio value updated constantly
- Price alerts (custom thresholds)
- Daily summary of market moves
- News relevant to holdings
- No trading — just monitoring, alerts, and advice
- **CoinStats integration**: Connects to Bob's existing CoinStats account — pulls portfolio data automatically instead of manual entry. Syncs holdings, transactions, profit/loss. CoinStats becomes the source of truth, SafetyNomad adds alerts and advice on top.
- **Manual entry fallback**: Can also add coins, amounts, and buy prices by hand — in case CoinStats is down, doesn't support a token, or Bob wants to track something off-exchange (cold wallet, DeFi positions, etc.)
- **Token scanner**: Constantly scans token tracking programs (CoinGecko, CoinMarketCap, DexScreener) for insights on Bob's holdings — flags unusual volume, whale movements, project updates, risk signals
- **Investment advice**: Based on portfolio performance and market data, suggests when to pay attention (not financial advice — information to help Bob decide)
- Watchlist Setup: Asks "What cryptos do you own?" on onboarding; creates/customizes watchlist
- Tracks profit/loss per token and overall portfolio health

### 9. Khmer Language & Culture
- Daily Khmer phrases (beyond tourist basics)
- Cultural context for living in Cambodia
- History lessons — not just Angkor Wat, but Khmer Rouge history, modern politics, regional traditions, Cambodian music, food culture, festivals
- Pronunciation guides with audio

### 10. Vietnamese Language & Culture
- Daily Vietnamese phrases — practical stuff for daily life (ordering food, negotiating rent, talking to neighbours, medical appointments)
- Tonal pronunciation practice (Vietnamese has 6 tones — this is the hard part, needs audio)
- Regional dialect differences: Northern (Hanoi) vs Central (Da Nang) vs Southern (Ho Chi Minh) — matters depending on where Bob lands
- Cultural norms: what's rude, what's respectful, how to build trust with locals
- History beyond the war — dynasties, French colonial era, modern economic boom, cultural identity
- Local food culture: regional dishes, street food etiquette, market haggling basics
- Visa and legal vocabulary: words you need at immigration, banks, landlords, hospitals
- Festival calendar: Tet, Mid-Autumn, local regional events worth knowing
- Expat integration tips: how to not be "that foreigner" — real cultural adaptation, not tourist survival
- Ties into Rice and Roadtrips: learn the language of the places you're filming

### 11. Blockchain, Mining & Web3 Learning Path
- Structured curriculum: blockchain fundamentals → crypto mining → Web3 → smart contracts → DAOs → DeFi
- Bite-sized daily lessons (10-15 min, matched to reading preferences)
- How each topic connects to OHS (blockchain compliance, safety auditing on-chain, DAO-based safety consulting)
- Hands-on exercises (set up a test wallet, deploy a test smart contract, etc.)
- Mining fundamentals: hardware, profitability calculators, energy considerations
- Web3 career paths: what jobs exist, what they pay, what skills they need
- Progress tracking with milestones
- Weekly quizzes to reinforce learning
- Curated news feed on blockchain/Web3 industry developments
- Ties into WorkSafe training justification (emerging tech + OHS = competitive edge)

### 12. Vietnam Travel Planner
- **Not moving — traveling.** Always scanning for hotel deals, flight deals, travel packages
- Location research: mountains + beaches + affordable destinations
- Cost of living comparisons between Vietnamese cities
- Visa requirements for visits (tourist vs longer stays)
- Healthcare options for travelers
- Hotel deal scanner: monitors booking sites for price drops on routes Bob cares about
- Best times to visit different regions (weather, festivals, crowds)
- Packing lists and travel checklists per trip
- Ties into Flight Tracker (Feature 23) for complete travel planning

---

## 💰 Budget Breakdown ($20/month)

| Item | Cost | Purpose |
|------|------|---------|
| VPS hosting (DigitalOcean or Railway) | $5-6/month | Runs the bot 24/7 |
| AI API (Claude or OpenAI) | $10-12/month | Smart responses, analysis |
| Database (Supabase free tier) | $0 | Stores memory, preferences, state |
| Email API (free tiers) | $0 | Gmail/Yahoo/Outlook access |
| Domain (optional) | $1/month | bruceai.app or similar |
| **Total** | **~$17-19/month** | Under budget ✅ |

**Cost optimization**:
- Simple tasks (reminders, lookups) → cheaper/smaller AI model
- Complex tasks (analysis, writing) → full Claude/GPT-4
- Local AI on M1 chip for basic stuff → $0
- Caching common responses → fewer API calls

---

## 🏗️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Frontend** | Progressive Web App (PWA) | Works on phone + Mac, one codebase, installable like an app |
| **Voice** | Web Speech API + Whisper | Free voice input, accurate transcription |
| **Backend** | Python (FastAPI) | Bob already has Python from RAZOR, lightweight |
| **AI Brain** | Claude API (Sonnet for cheap tasks, Opus for complex) | Best reasoning, fits budget |
| **Database** | Supabase (PostgreSQL) | Free tier, Bob already uses PostgreSQL from RAZOR |
| **Background Jobs** | Celery + Redis (or simple cron) | Runs cleanup tasks on schedule |
| **Email** | IMAP/OAuth2 | Direct email access, no middleman |
| **Calendar** | Google Calendar API | Free, well-documented |
| **Hosting** | Railway or DigitalOcean | Simple deployment, $5-6/month |
| **File Sync** | Google Drive API + local file watcher | Monitors both cloud and local files |
| **Mac Agent (Sidecar)** | Python background script | **NEW** — lightweight script on Mac that handles local file moves, cleanup, system health checks. The web app (Brain) tells the Agent what to do, Agent executes locally. Required because a PWA can't touch your hard drive directly. |
| **Phone Automation** | Tasker / MacroDroid (Android) | **NEW** — handles phone-side automation (settings, notifications, ad blocking) |
| **Memory System** | RAG (Retrieval Augmented Generation) | **NEW** — stores all data in database, pulls only what's needed per conversation. Keeps AI costs under $20/month instead of feeding everything into every request. |

---

## 📱 How Bob Uses It

### Morning
> **SafetyNomad AI**: "Good morning Bob. Here's your day:
> - OHS Module 6 assignment due in 4 days
> - Bitcoin up 3.2% overnight ($312 gain)
> - 2 emails need attention (1 from WorkSafe, 1 from university)
> - Weather in Phnom Penh: 34°C, no rain
> - While you slept: organized 23 screenshots, freed 1.1GB on your Mac
> - Khmer phrase of the day: សួស្តី ពេលព្រឹក (Suostei pel prik) — Good morning"

### Throughout the Day
- "Hey SafetyNomad, what's my crypto portfolio at?"
- "Remind me to email my prof about the extension"
- "What's the Khmer word for 'thank you very much'?"
- "Summarize my emails from today"
- "How much did I spend this week?"

### Evening
- Study session reminder
- Daily crypto summary
- Tomorrow's calendar preview
- "Anything I forgot to do today?"

---

## 🚀 Build Phases

**⚠️ Important: Phases = BUILD ORDER, not access order.** Once everything is built, ALL features work at once. Phases exist because some features need other features to exist first (can't display email summaries without the chat interface). Think of it like building a house — foundation, then walls, then roof. But once it's done, you use every room from day one.

### Phase 1: Foundation (Week 1-2)
**Goal**: Basic chat + file organizing that works on phone and Mac

- [ ] Set up PWA with chat interface
- [ ] Voice input + text input
- [ ] Connect Claude API
- [ ] Basic memory (remembers conversations)
- [ ] **Mac Agent (Sidecar) setup** — basic file organizing starts here
- [ ] **Basic file cleanup**: organize Downloads, sort documents into folders
- [ ] Deploy to Railway/DigitalOcean
- [ ] Test on MacBook + Galaxy S24

**Bob gets**: A smart chatbot + file organizer from day one

---

### Phase 2: Life Integration (Week 3-4)
**Goal**: Connects to Bob's actual life

- [ ] Gmail/Yahoo/Outlook email reading + summarization
- [ ] Google Calendar sync
- [ ] Crypto portfolio monitoring (CoinGecko API, free)
- [ ] Daily briefing (morning + evening)
- [ ] Push notifications (browser + phone)

**Bob gets**: A daily briefing and email assistant

---

### Phase 3: Deep Automation (Week 5-6)
**Goal**: Heavy-duty background tasks (basic file organizing already running from Phase 1)

- [ ] **Advanced** file cleanup: duplicate scanning, overnight runs, external hard drives
- [ ] Google Drive organizer
- [ ] Security scanning (malware, suspicious files, phishing attachments)
- [ ] Storage monitoring + alerts
- [ ] NordPass integration (password health reports)
- [ ] Morning report of overnight tasks

**Bob gets**: The full digital janitor — runs while he sleeps

---

### Phase 4: Study + Business (Week 7-8)
**Goal**: School and hustle support

- [ ] OHS flashcard integration
- [ ] Spaced repetition scheduling
- [ ] Assignment deadline tracking
- [ ] Gumroad sales dashboard
- [ ] Business income tracker
- [ ] Vietnam travel planner setup

**Bob gets**: School + business in one place

---

### Phase 5: Khmer + Culture (Week 9-10)
**Goal**: Language and cultural learning

- [ ] Daily Khmer phrases with audio
- [ ] Culture lessons (history, traditions, food, beyond Angkor)
- [ ] Pronunciation practice
- [ ] Conversation practice mode

**Bob gets**: A Khmer tutor built into his assistant

---

### Phase 6: Product Launch (Week 11-12)
**Goal**: Turn it into a product others can buy

- [ ] Multi-user support
- [ ] Onboarding flow for new users
- [ ] Free tier (basic chat + reminders)
- [ ] Paid tier at $15/month (full features)
- [ ] Landing page
- [ ] Stripe payment integration
- [ ] Marketing: "AI assistant for people who aren't tech people"

**Bob gets**: A product generating recurring revenue

---

## 👩 Girlfriend's Version (Future)

Simplified interface optimized for:
- iPhone 11 screen size
- Khmer language primary, English secondary
- AI video creation workflow helper
- Simpler feature set (no crypto, no OHS)
- Voice-first design (minimal reading required)
- Tutorial mode for learning AI tools

**Build after Phase 4**, once the core system is stable.

---

## 💵 Product: SafetyNomad AI for Everyone

### Target Customer
**"The Expat's Chief of Staff"** — not selling "AI" to people, selling a life manager to people juggling two countries.

Primary audience:
- Expats managing life across countries (visa, currency, healthcare, taxes)
- Digital nomads in Southeast Asia
- Over-40s who feel left behind by tech
- Trades workers transitioning careers
- Students returning to school later in life
- Anyone who says "I'm not a tech person"

The selling point isn't "It's AI." The selling point is "It manages your visa, your foreign currency, your health, and your home/business split."

### Free Tier
- Smart chat (10 messages/day)
- Basic reminders
- Daily briefing
- Single email account

### Paid Tier ($15/month)
- Unlimited chat + voice
- Background file automation
- Multi-email support
- Calendar sync
- Crypto monitoring
- Study tools
- Cultural/language learning modules
- Priority AI (faster, smarter responses)

### Revenue Projections (Conservative)
| Users | Monthly Revenue | Monthly Costs | Profit |
|-------|----------------|---------------|--------|
| 10 | $150 | $50 | $100 |
| 50 | $750 | $150 | $600 |
| 100 | $1,500 | $300 | $1,200 |
| 500 | $7,500 | $1,000 | $6,500 |

Costs scale with users (more API calls), but margins stay healthy at 60-80%.

---

## ⚡ Quick Decisions Made

| Decision | Choice | Why |
|----------|--------|-----|
| Platform | PWA (web app) | Works everywhere, no app store needed |
| Bot vs App | Web app with chat UI | Avoids Telegram scam vibes |
| Voice | Yes, primary input | Bob's preference, easier than typing |
| AI Provider | Claude API | Best reasoning, good pricing |
| Database | Supabase | Free tier, PostgreSQL (familiar from RAZOR) |
| Hosting | Railway or DigitalOcean | Cheap, simple |
| Password mgmt | Integrate with NordPass | Already has it, don't rebuild |
| Product price | $15/month | Bob's gut feel, competitive |
| Offline mode | Yes — core features | Internet unreliable in SE Asia |

---

## 🔗 Connects To Existing Tools

| Tool | Integration |
|------|-------------|
| **RAZOR** | Can trigger video processing from assistant ("process my new videos") |
| **OHS Flashcards** | Study reminders, progress tracking |
| **Gumroad** | Sales notifications, revenue dashboard |
| **NordPass** | Password health monitoring |
| **Google Drive** | File organization, backup monitoring |

### 13. Privacy & Security Guardian (McAfee Mode)
- **VPN monitoring**: Checks NordVPN is always on, alerts if connection drops, auto-suggests best server for speed/privacy based on location
- **Browser hygiene**: Flags tracking cookies, suggests which extensions to block/keep, monitors for browser fingerprinting
- **Data leak monitoring**: Scans dark web for your email addresses, usernames, phone numbers appearing in breaches
- **Encrypted vault**: Auto-moves sensitive files into NordLocker (WorkSafe docs, tax files, crypto wallets, passport scans, banking info)
- **App permissions audit**: Flags apps on phone/Mac that have excessive permissions (camera, mic, location, contacts)
- **Email security**: Identifies phishing attempts, spoofed senders, suspicious links before you click
- **Crypto wallet security**: Monitors wallet addresses for unauthorized transactions, flags suspicious smart contract approvals
- **Network scanner**: Checks WiFi networks for vulnerabilities (especially important in Cambodia/Vietnam cafes and co-working spaces)
- **Digital footprint report**: Monthly report showing what personal data is publicly visible about you online and how to reduce it
- **Metadata stripping**: Removes location/device data from photos and files before you share them
- **Two-factor audit**: Tracks which accounts have 2FA enabled and nags you about the ones that don't
- **Social engineering alerts**: Warns about common scams targeting expats in Southeast Asia (crypto scams, fake exchanges, romance scams, telegram schemes)
- **Device lockdown checklist**: Ensures Mac and S24 have full disk encryption, firewall on, Bluetooth off when not in use, auto-lock enabled
- **NordPass + NordVPN + NordLocker integration**: Full Nord ecosystem working together as one shield
- **AIntivirus Privacy Tools integration**: Metadata cleaner (strips GPS, timestamps, device info from files before sharing), surveillance tracker (global map of trackers/cameras), privacy browser extension (blocks trackers, fingerprinting scripts, built-in wallet), cross-chain mixer for anonymous crypto transactions
- **Note**: Use the free privacy tools only — do NOT auto-invest in the AINTI token
- **Crypto scam detector**: Flags suspicious Telegram links, rug pull warning signs, fake airdrops, too-good-to-be-true offers, and honeypot contracts before you click or connect a wallet

### 14. "Products of Pain" Podcast Hub
- Concept: A podcast sharing stories of people who've been through serious adversity (injury, career loss, addiction, rehab) and built something from it
- Bob is the host — starts with his own story (Coast Guard, fishing, helilogging, construction injuries, WorkSafe rehab, reinvention)
- Guest management: track potential guests, schedule recordings, store contact info
- Episode planner: outline episodes, talking points, research notes
- Recording integration: links to recording tools (could tie into RAZOR for video episodes)
- Show notes generator: AI creates show notes, timestamps, and social media clips from each episode
- **Active producer mode**: After recording, SafetyNomad interviews Bob — "Give me 3 things that stood out while it's fresh" — then auto-drafts show notes and social posts immediately
- Distribution tracker: monitor uploads to Spotify, Apple Podcasts, YouTube
- Audience analytics: downloads, listener demographics, growth trends
- Monetization tracking: sponsorships, Patreon, merch revenue
- Brand alignment: ties into the personal assistant product — your audience IS your customer base

### 15. "Rice and Roadtrips" YouTube Channel Hub
- Concept: Raw, unfiltered content about real life in Cambodia and Vietnam — not tourist highlight reels, real talk
- Local food spots the tourists never find, back road trips, village life, real conversations with locals
- Market runs, street food, countryside rides, border crossings, the unglamorous side of expat life
- Content ideas generator: assistant suggests local spots, events, seasonal things worth filming based on your location
- Episode planner: outlines, shot lists, talking points
- Ties into RAZOR pipeline: raw footage → RAZOR processes → edited videos + viral clips
- Thumbnail and title suggestions based on what performs well in the travel/expat niche
- Upload scheduling: best times to post for your audience
- Analytics tracking: views, subs, watch time, revenue
- Khmer/Vietnamese subtitle generation for local audience reach
- Collaboration tracker: local creators, other expat channels, cross-promotion opportunities
- Monetization: YouTube ad revenue, sponsorships from local businesses, affiliate links for expat services
- Tone guide: authentic, no clickbait, no "TOP 10 THINGS IN SIEM REAP" energy. Just real life.

### 16. Money, Expenses & Banking
**WorkSafe tracking:**
- Logs every receipt automatically (photo → OCR → categorized)
- Tracks submissions to case manager (sent, pending, approved, rejected)
- Reimbursement status tracking
- Monthly expense reports ready to send
- Tax-relevant categorization for Canadian filing
- Alerts when receipts are due or aging out

**Daily money management:**
- Tracks spending across all accounts
- Identifies recurring subscriptions and flags unused ones
- Finds cheaper alternatives for services Bob uses
- Budgeting against the $1,000 CAD/month baseline
- Savings goals with progress tracking

**Expat finance:**
- Currency exchange rate monitoring (CAD → USD → KHR → VND)
- Flags when exchange rates are favorable for transfers
- Compares cost of living between locations (Cambodia vs Vietnam cities)
- Tips specific to expat life in Southeast Asia (where to get best rates, local vs tourist pricing)

**Banking alerts:**
- Monitors for account restrictions or freezes (like cross-border banking issues)
- International transfer tracking — flags delays, fees, failed transfers
- Alerts on unusual account activity
- Tracks which banks/services work best for expats in SE Asia

**Canadian Tax Program:**
- Tracks all income sources for CRA filing: WorkSafe (T4A), Gumroad sales, crypto gains/losses, bird nest farming
- Expense categorization with tax deduction flags (home office, education, medical, business)
- Crypto tax tracking: cost basis, capital gains/losses per CRA rules
- Foreign income reporting reminders (expat-specific obligations)
- Deadline alerts: April 30 filing, quarterly installments if needed
- Generates tax-ready reports exportable for accountant or self-filing
- Tracks receipts already categorized from WorkSafe tracker — no double entry
- Flags deductions Bob might miss (moving expenses, education credits, medical expenses abroad)
- **⚠️ Not a replacement for an accountant** — organizes everything so filing is fast and nothing's missed

### 17. Remote Job Scanner
- Scans job boards daily for remote OHS roles (Indeed, LinkedIn, FlexJobs, We Work Remotely)
- Filters: remote-only, OHS + tech crossover, blockchain/AI/Web3 safety roles
- Tracks salary ranges so you know the market
- Flags jobs matching your specific skill combo (OHS + AI + blockchain)
- Saves interesting postings with one tap
- Alerts when new jobs match your profile
- Starts NOW — by graduation you'll know the market inside out

### 18. Immigration & Visa Tracker
- Cambodia visa status and renewal dates
- Vietnam visa research (requirements, costs, types)
- Document expiry alerts (passport, travel insurance, permits)
- Deadline reminders with buffer time (warns 30 days before expiry)
- Stores digital copies of all travel documents in NordLocker vault

### 19. Voice Journal
- Talk for 2-5 minutes, assistant transcribes, summarizes, and stores it
- Searchable journal — "what was I thinking about last Tuesday?"
- Mood tracking over time (AI detects patterns)
- Pain/health notes ("my back was bad today, 7/10")
- Idea capture — random thoughts saved and organized
- Ties into Products of Pain podcast prep — daily reflections become episode material

### 20. Health & Injury Tracker
- **Proactive check-ins**: SafetyNomad prompts Bob 2-3 times daily — "How are you feeling right now? Pain level? What hurts?" — not waiting for Bob to remember. Frequency is adjustable (1-5x/day) so it doesn't become annoying.
- Morning check-in: "How'd you sleep? How's the body?"
- Midday check-in: "Pain level right now, 1-10?"
- Evening check-in: "How was today physically? Anything new?"
- Logs responses automatically — builds a pain journal over time
- Daily pain level logging (quick 1-10 scale via voice or tap)
- Medication reminders and tracking
- Physio exercise schedule and completion tracking
- Doctor/specialist appointment management
- Symptom patterns over time (AI spots trends)
- Exportable reports for WorkSafe documentation
- Useful evidence if they ever question your physical limitations
- **Exercise accountability**: Daily check-ins on physio and exercise goals, progress reports, calls out skipped days directly
- **Anti-laziness helper**: Gentle but firm nudges when tasks pile up — "You haven't done physio in 3 days. 10 minutes. Let's go."

**Medical Question Tool:**
- Ask health/medical questions in plain language — gets clear, simple answers (not jargon)
- Helps Bob understand medical terms from doctor visits, WorkSafe reports, or prescriptions
- Translates medical info for girlfriend (Khmer/English)
- Symptom checker: "I've had this pain for 3 days, what could it be?" — gives possibilities, NOT diagnoses
- Medication interaction checker: "Can I take X with Y?"
- Helps prepare questions before doctor appointments: "I'm seeing the physio tomorrow — what should I ask about my shoulder?"
- Emergency guidance: "What do I do if someone has heat stroke?" — step-by-step first aid
- Local healthcare info: nearest hospitals/clinics in Cambodia/Vietnam, what they specialize in, expat-friendly options
- **⚠️ Always includes disclaimer: "I'm not a doctor. This is information, not medical advice. See a professional for anything serious."**
- Ties into Health & Injury Tracker — uses your pain history for smarter answers

### 21. Emergency Info Card
- Stored locally on phone — accessible even offline or if app is down
- Blood type, allergies, medications, emergency contacts
- WorkSafe claim number, insurance info
- Embassy contact info for Canada (Cambodia + Vietnam)
- Girlfriend's contact info and local emergency numbers
- Medical conditions and injury history summary

### 22. Digital Dead Man's Switch
- If Bob doesn't check in for a set period (e.g., 30 days), the system triggers:
  - Sends pre-written emails to designated people (girlfriend, family, executor)
  - Shares access credentials to important accounts via NordPass emergency access
  - Transfers crypto wallet access to designated beneficiary
  - Unlocks NordLocker vault for designated person
  - Shares location of important physical documents
  - Provides instructions for digital accounts (close, memorialize, or transfer)
- Check-in is simple: just use the assistant normally and the timer resets
- Configurable: who gets what, what messages say, how long to wait
- Can be paused (e.g., going off-grid for a hiking trip)

### 23. Flight Tracker & Travel Deals
- Monitors flight prices for routes Bob cares about (Cambodia → Vietnam, Vietnam → Canada, etc.)
- Alerts when prices drop below a threshold
- Tracks active bookings with gate changes, delays, cancellations
- Compares airlines and routes for best value
- Integrates with Google Flights and Skyscanner data
- Stores boarding passes, booking confirmations, loyalty program info

### 24. Ad Blocker & Device Optimizer
- **Full ad blocking audit**: Checks what your current ad blocker catches and what slips through (Facebook in-feed ads, YouTube pre-rolls, Instagram sponsored posts, in-app ads)
- **Facebook/Meta ad blocking**: Configures DNS-level blocking and browser settings to minimize Facebook, Instagram, and Messenger ads
- **Phone optimization (Galaxy S24)**: Disables Samsung bloatware, turns off ad-serving Samsung apps (Galaxy Store ads, Samsung Push notifications), optimizes battery, manages app permissions, disables tracking
- **Mac optimization (MacBook Air M1)**: Cleans startup items, disables telemetry, configures Safari/Chrome privacy settings, manages notification overload
- **DNS-level ad blocking**: Sets up system-wide ad blocking (like NextDNS or AdGuard DNS) that works across ALL apps, not just browsers — covers in-app ads too
- **Step-by-step guided setup**: Since the assistant can't directly access device settings, it walks Bob through changes via voice instructions or annotated screenshots
- **Future upgrade**: Integrate with Apple Shortcuts + Samsung Routines to automate settings changes directly

---

## ❓ Open Questions (To Decide Later)

1. ~~**App name?**~~ **DECIDED: SafetyNomad AI** ✅
2. **Domain:** safetynomad.ai (~$40/year) — CONFIRM AVAILABILITY AND REGISTER ASAP
3. **Offline mode?** Should basic features work without internet?
4. **Multi-language product?** Khmer version for Cambodia market?
5. **Partner features?** Shared to-do lists, shared calendar with girlfriend?
6. **What else?** Bob said "there's more, just can't think now" — add features anytime

---

## 📋 What Bob Needs To Do

1. ✅ Answer planning questions (DONE — this conversation)
2. ⬜ Review this blueprint and flag anything missing
3. ✅ Pick a name for the assistant — **SafetyNomad AI** (register domain ASAP)
4. ⬜ Say "let's build Phase 1" when ready
5. ⬜ Provide Gmail/Yahoo/Outlook access when we hit Phase 2

**Bob is always open to suggestions and available for questions on any part of this.** Nothing is locked — everything can be tweaked, added, or removed at any time.

---

## 📍 Current Status

```
Phase 1: Foundation      ⬜ Not started
Phase 2: Life Integration ⬜ Not started
Phase 3: Deep Automation  ⬜ Not started
Phase 4: Study + Business ⬜ Not started
Phase 5: Khmer + Culture  ⬜ Not started
Phase 6: Product Launch   ⬜ Not started
```

**Next step**: Bob reviews this blueprint. When ready, we build Phase 1.

---

**Built for Bob. Designed for every nomad. 🚀**
