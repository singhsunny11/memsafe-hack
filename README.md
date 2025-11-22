# MemSafe — C to Rust Safety Assistant

A Streamlit-based tool that analyzes C code for memory safety vulnerabilities and suggests Rust-based solutions.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up AI Provider (Choose ONE)

#### Option A: OpenAI (Free Tier Available!)

**$5 free credits for new accounts - no credit card required initially!**

1. Sign up: https://platform.openai.com/signup
2. Get API key: https://platform.openai.com/api-keys
3. Create `.env` file:
   ```bash
   OPENAI_API_KEY=sk-your-api-key-here
   ```

See [OPENAI_FREE_SETUP.md](OPENAI_FREE_SETUP.md) for detailed instructions.

**Note**: Hugging Face API is currently unavailable (all models returning errors).

1. Get API key: https://platform.openai.com/api-keys
2. Create `.env` file:
   ```bash
   OPENAI_API_KEY=sk-your-api-key-here
   ```

### 3. Run the App

**Option A: Using the run script (recommended)**
```bash
./run.sh
```

**Option B: Direct Streamlit command**
```bash
streamlit run app/main.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 📝 How to Use

1. **Select Provider**: Choose "Hugging Face (FREE)" or "OpenAI (Paid)" in settings
2. **Paste C Code**: Copy and paste your C code into the text area
3. **Click Analyze**: The app will analyze your code for vulnerabilities
4. **Review Results**: 
   - See a summary of findings
   - Check the safety score (0-100)
   - Review detected vulnerabilities with code snippets
   - Explore suggested Rust fixes

**💡 Student Tip**: Use "Hugging Face (FREE)" - it's completely free and works great!

## 🧪 Example Code

Try analyzing one of the example files in the `examples/` directory:

- `1_malloc_free_misuse.c` - Memory allocation issues
- `2_buffer_overflow.c` - Buffer overflow vulnerabilities
- `3_null_deref.c` - Null pointer dereferences
- `4_use_after_free.c` - Use-after-free bugs
- `5_pointer_arith.c` - Pointer arithmetic issues

## 🏗️ Project Structure

```
memsafe-hack/
├── app/
│   └── main.py              # Streamlit application
├── utils/
│   ├── json_parser.py       # Robust JSON extraction
│   ├── snippet_extractor.py # Code snippet extraction
│   ├── severity.py          # Severity scoring
│   ├── prompt_template.txt  # AI prompt template
│   └── analyzer.py          # Analysis utilities
├── examples/                # Example C files
├── requirements.txt         # Python dependencies
└── run.sh                   # Quick start script
```

## ✨ Features

- **Robust JSON Parsing**: Handles malformed AI responses with multiple fallback strategies
- **Smart Snippet Extraction**: Extracts vulnerable code using line numbers or pattern matching
- **Automatic Score Calculation**: Calculates safety scores from vulnerabilities if not provided
- **Comprehensive Error Handling**: Clear error messages for API issues and parsing failures
- **Modern UI**: Clean, organized interface with expandable sections

## 🔧 Troubleshooting

**App won't start?**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're running from the project root directory

**API errors?**
- Verify your `.env` file exists and contains a valid `OPENAI_API_KEY`
- Check your OpenAI account has available credits

**No results showing?**
- Try with one of the example files first
- Check the browser console for errors
- Look for error messages in the Streamlit UI

## 📄 License

This project is part of a hackathon submission.
