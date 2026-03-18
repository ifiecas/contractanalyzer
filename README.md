# ◈ Local Contract Analyzer

A privacy-first contract analysis tool that runs 100% offline using Microsoft Foundry Local. Upload a PDF contract and get a plain-English breakdown — risk level, red flags, key terms, important dates, and questions to ask before signing. **Nothing ever leaves your device.**

## 🎯 Overview

This project demonstrates how to build a private AI-powered contract analyzer using Foundry Local. All processing happens on your local machine — no internet connection required after setup, no data sent to external servers, and no information used for model training.

## ✨ Features

- **100% Private**: All data stays on your device
- **Offline Operation**: No internet required after initial model download
- **PDF Support**: Upload contracts directly as PDF files
- **Structured Analysis**: Risk banner, red flags, key terms, dates, numbers, recommendation, and questions to ask
- **No Data Training**: Your contracts are never used to train AI models
- **Clean UI**: Minimal, demo-ready interface

## 🛠️ Tech Stack

- **Foundry Local**: Microsoft's local AI runtime (OpenAI-compatible API)
- **phi-4-mini**: Fast, lightweight model optimised for document analysis
- **Streamlit**: Web application frontend
- **pymupdf (fitz)**: PDF parsing
- **Python**: Application runtime

## 💻 Requirements

- **OS**: macOS (Apple Silicon recommended), Windows 10/11, or Linux
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: At least 5GB free space
- **Python**: 3.8 or higher
- **Internet**: Required once to download the model — fully offline after that

## 🚀 Getting Started

### 1. Install Foundry Local

**macOS:**
```bash
brew tap microsoft/foundrylocal
brew install foundrylocal
```

**Windows:**
```bash
winget install Microsoft.FoundryLocal
```

> After installing, verify it works:
> ```bash
> foundry --version
> ```

---

### 2. Download the model *(one-time, requires internet)*

```bash
foundry model run phi-4-mini
```

Wait until you see the service is running ✅

> This downloads phi-4-mini (~3.7GB) and caches it locally. You only need to do this once — after that it runs completely offline.

---

### 3. Clone this repository

```bash
git clone https://github.com/ifiecas/contract-analyzer.git
cd contract-analyzer
```

---

### 4. Set up a virtual environment *(recommended)*

```bash
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

---

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

Every time you want to use the app, you need two terminal tabs:

**Terminal 1 — Start the AI model:**
```bash
foundry model run phi-4-mini
```
Wait until you see the service is running ✅

**Terminal 2 — Launch the app:**
```bash
cd contract-analyzer
bash start.sh
```

Then open your browser to the local URL shown in the terminal (usually `http://localhost:8501`).

> **Two commands. That's the entire setup.**

---

## 🏗️ How It Works

```
┌─────────────────────────────┐
│        Your Machine         │
│                             │
│  ┌─────────────────────┐   │
│  │   Foundry Local      │   │  ← Serves phi-4-mini locally
│  │  (localhost API)     │   │  ← OpenAI-compatible endpoint
│  └─────────────────────┘   │
│            ↕                │
│  ┌─────────────────────┐   │
│  │  Contract Analyzer   │   │  ← Streamlit frontend
│  │     (app.py)         │   │
│  └─────────────────────┘   │
└─────────────────────────────┘
         ↕
   Your PDF Contract
   (Never leaves your device)
```

The app connects to Foundry Local via a local OpenAI-compatible API running on `localhost`. Your contract is sent to the model running on your own machine — no external servers involved.

---

## 📋 What You Get

Upload a PDF contract and the app returns:

- **Risk Level** → High / Medium / Low with a plain-English summary
- **What is this contract** → 2-3 sentence overview
- **Who is involved** → Parties and their obligations
- **Red Flags** → Issues ranked by severity with suggestions
- **Terms Explained** → Legal jargon in plain English
- **Key Dates & Numbers** → Important figures at a glance
- **Recommendation** → Sign, negotiate, or avoid
- **Questions to Ask** → Before you sign

## 📄 Supported Contract Types

- Employment agreements
- Service contracts
- NDAs
- Lease agreements
- Vendor agreements
- Partnership agreements
- License agreements

## 🔧 Troubleshooting

**"Could not connect to Foundry Local"**
→ Make sure `foundry model run phi-4-mini` is running in a separate terminal tab first.

**"streamlit: command not found"**
→ Use `bash start.sh` instead of calling `streamlit` directly. This activates the correct environment.

**App is slow on first run**
→ The model takes a moment to load into memory. Subsequent analyses in the same session will be faster.

**Model not found**
→ Run `foundry model list` to confirm phi-4-mini is downloaded. If not, run `foundry model run phi-4-mini` again with an internet connection.

---

## 🔐 Privacy & Security

- **No Cloud Processing**: Everything runs locally on your machine
- **No Telemetry**: No usage data collected
- **No Model Training**: Your data never trains the AI
- **Offline After Setup**: Internet only needed for first-time model download

---

## 📧 Contact

**Portfolio**: [ifiecas.com](https://ifiecas.com)

**Blog post**: [A Private Contract Analyzer That Never Shares Your Data](https://ifiecas.com/2025/12/19/a-private-contract-analyzer-that-never-shares-your-data/)

---

**⚠️ Disclaimer**: This tool is intended for educational and experimental purposes only and is a demonstration of Foundry Local's capabilities for running AI models privately on your local machine.

**This tool does not provide legal advice.** The analysis generated by this application should not be relied upon for legal decisions. Always consult a qualified attorney or legal professional for advice on contracts or any legal matters. The author assumes no liability for any decisions made based on the output of this tool.
