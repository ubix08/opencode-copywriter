---
name: images
agent: copywriter-orchestrator
description: Fetch and embed real images into an article using Pexels and Hugging Face
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/blog-patterns.md

You are the Copywriter Orchestrator.

**File to process:** $ARGUMENTS

Fetch and embed real images into this article. This command replaces image placeholder comments with actual images.

### How It Works

1. Read the article and identify image placeholder comments in this format:
   ```
   <!-- image: query="search terms" type="photo|diagram" alt="descriptive alt text" -->
   ```

2. For each placeholder:
   - **type="photo"**: Search Pexels API for a relevant stock photo
   - **type="diagram"**: Generate a technical illustration using Hugging Face FLUX model

3. Download/save images to `content/images/`

4. Replace each placeholder comment with a markdown image tag:
   ```markdown
   ![descriptive alt text](content/images/filename.jpg)
   <!-- Photo by Photographer from Pexels: https://... -->
   ```

5. Save the updated article.

### API Configuration

- **Pexels API key**: Read from environment variable `PEXELS_API_KEY` or ask the user
- **Hugging Face token**: Read from environment variable `HF_TOKEN` or ask the user

If neither is configured, inform the user how to get them:
- Pexels: https://www.pexels.com/api/ (free, instant key)
- Hugging Face: https://huggingface.co/settings/tokens (free token)

### Execution

Run the image fetcher script:
```bash
python3 scripts/fetch-images.py <article.md> [--pexels-key KEY] [--hf-token TOKEN]
```

### Image Rules

- **Photos** (type="photo"): Use for hero images, section breakers, team/collaboration shots
- **Diagrams** (type="diagram"): Use for architecture diagrams, flowcharts, technical illustrations
- **Alt text**: Must be descriptive, include keyword naturally, under 125 characters
- **Query**: Use specific search terms. For photos: "server room technology", "developer coding laptop". For diagrams: "layered architecture stack", "data flow pipeline"
- **Minimum**: 1 image per 500 words of article content

### Output

Report:
- Number of placeholders found
- Number successfully replaced
- Number failed (and why)
- List of images added with file paths
