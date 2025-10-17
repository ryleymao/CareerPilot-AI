# Ollama Setup Guide - FREE & Unlimited LLM!

## What is Ollama?

Ollama runs AI models **locally on your Mac** - completely **FREE**, **UNLIMITED**, and **PRIVATE**!

- ✅ No API costs
- ✅ No token limits
- ✅ Works offline (after download)
- ✅ Your resume data never leaves your computer
- ✅ Easy to switch models

## Quick Start

Ollama is already installed and configured! 🎉

### 1. Verify Ollama is Running

```bash
ollama list
```

You should see `llama3.1` (or currently downloading).

### 2. Switch Models Anytime

Want to try a different model? Super easy:

```bash
# Download a new model
ollama pull mistral       # Fast & smart
ollama pull codellama     # Great for code
ollama pull phi3          # Lightweight
ollama pull gemma2        # Google's model

# Use it by editing .env:
# Change OLLAMA_MODEL=llama3.1 to OLLAMA_MODEL=mistral
```

### 3. Test It Out

```bash
ollama run llama3.1
```

Type a question and press Enter. Type `/bye` to exit.

## Using in JobRight Clone

The project is **already configured** to use Ollama by default!

Just make sure Ollama is running:
```bash
brew services start ollama
```

That's it! Resume tailoring will use your local LLM.

## Switching to Cloud APIs (Optional)

Want to use Claude or GPT instead? Edit `.env`:

```bash
# For Anthropic Claude (costs $0.05-0.10 per resume)
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-key-from-anthropic

# OR for OpenAI GPT (costs $0.03-0.08 per resume)
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key-from-openai

# OR back to FREE Ollama
LLM_PROVIDER=ollama
```

## Popular Ollama Models

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| llama3.1 | 4.7GB | Medium | Excellent | General use (DEFAULT) |
| mistral | 4.1GB | Fast | Great | Speed + quality balance |
| codellama | 3.8GB | Fast | Great | Code/technical content |
| phi3 | 2.3GB | Very Fast | Good | Lightweight/fast |
| gemma2 | 5.4GB | Medium | Excellent | Google's latest |

## Commands Cheat Sheet

```bash
# List installed models
ollama list

# Download a model
ollama pull <model-name>

# Run/test a model interactively
ollama run <model-name>

# Delete a model
ollama rm <model-name>

# Check Ollama status
brew services info ollama

# Start Ollama
brew services start ollama

# Stop Ollama
brew services stop ollama

# Restart Ollama
brew services restart ollama
```

## Troubleshooting

### "Connection refused" error

Ollama isn't running. Start it:
```bash
brew services start ollama
```

### Model not found

Download it first:
```bash
ollama pull llama3.1
```

### Slow performance

Try a lighter model:
```bash
ollama pull phi3
# Then change OLLAMA_MODEL=phi3 in .env
```

### Out of memory

Close other apps or use a smaller model (phi3, mistral)

## Why Ollama vs Cloud APIs?

**Ollama (Local)**
- ✅ FREE - unlimited usage
- ✅ PRIVATE - data stays on your Mac
- ✅ OFFLINE - works without internet
- ⚠️ Quality: 80-90% of Claude/GPT
- ⚠️ Slower: 10-20 seconds vs 3-5

**Claude/GPT (Cloud)**
- ⚠️ PAID - ~$0.05-0.10 per resume
- ⚠️ ONLINE - requires internet
- ⚠️ PRIVACY - data sent to servers
- ✅ Quality: Best available
- ✅ Fast: 3-5 seconds

## Recommendation

**Start with Ollama** (free, unlimited). If you need higher quality for a specific job application, switch to Claude/GPT for just those important ones.

---

🎯 Ready to use! The project is configured to use Ollama by default.
