To build a **Gumroad Factory** system on Claude, you can leverage Claude Code's unique capabilities—specifically its **Plan Mode** and file-system access—to transform a raw manuscript into a ready-to-sell digital product [1, 2].

The following is the **Master Implementation Prompt**. You can copy this entire block and paste it directly into **Claude Code** (or a similar agentic AI coding assistant) to scaffold the project and implement the system immediately.

***

### Master Implementation Prompt: The Gumroad Factory

**Project Goal:** 
Scaffold a "Gumroad Factory" agentic system that automates the creation of marketing and sales assets from book manuscripts located in a local directory [1, 3].

**Step 1: Directory Scaffolding**
Create the following directory structure:
- `/manuscripts`: For input files (Markdown, TXT, or PDF).
- `/assets/product-descriptions`: For high-conversion sales copy.
- `/assets/preview-pages`: For extracted sample chapters/content.
- `/assets/social-media-specs`: For detailed prompts for AI image generators (DALL-E/Midjourney).

**Step 2: Create the Agent Instructions (`.claudecode.md`)**
Generate a `.claudecode.md` file that defines the **Gumroad Factory Persona**. The instructions must include:
1.  **Identity:** You are the Gumroad Factory Agent, a specialist in digital productization [3].
2.  **Logic:** Upon being given a manuscript name, you must first read the file to understand the value proposition, target audience, and key takeaways [2, 4].
3.  **Plan Mode Protocol:** You must always enter **Plan Mode** to outline the specific assets to be created before writing any files. This prevents context window fatigue and ensures the user approves the marketing angle [2, 5].
4.  **Asset Requirements:**
    - **Product Description:** Must include a hook, "what's inside," and a call to action [4].
    - **Preview Pages:** Select 3-5 pages of high-value content to act as a "teaser" [4, 6].
    - **Visual Specifications:** Instead of generating images, write precise, high-fidelity prompts for social media and cover art [4, 6].

**Step 3: Implementation of a "Setup Script"**
Create a `factory-init.sh` script that automates the folder creation and creates a sample "Author Bio" data set to ensure personalized asset creation [4].

***

### Key System Components (Deep Dive)

Drawing from the source material, here is the breakdown of how this Claude-adapted project functions:

#### 1. The Power of "Plan Mode"
A critical advantage of using Claude for this project is its **Plan Mode**. The source notes that while other CLIs might struggle with context, Claude Code builds a plan, asks for approval, and then **clears the context window** to execute the plan cleanly [2, 5]. This is essential when processing a 100+ page manuscript [2].

#### 2. Automated Asset Creation
The system is designed to generate three core outputs for every manuscript [6]:
*   **Sales Copy:** A Markdown file formatted for the Gumroad product page [4].
*   **Preview Content:** Representative pages that can be converted into a "Look Inside" PDF [4].
*   **Social Media Specs:** Detailed descriptions that bridge the gap between the book's text and the visual marketing needed on platforms like X or Instagram [4].

#### 3. Continuous Skill Development
The source suggests that as you use this system, you should "dial in" repetitive tasks by turning them into **skills or tools** [2]. In your Claude project, this can be achieved by creating **reusable templates** (e.g., a `templates/` folder) that the agent must reference to ensure every book has a consistent "brand voice."

### How to Run Your Factory
Once the scaffolding is complete:
1.  Place a manuscript (e.g., `manuscripts/The_AI_Engineer.md`) in the folder [3, 6].
2.  In the Claude Code CLI, type: 
    > *"Gumroad Factory: Process 'The AI Engineer'. Create all defined assets."*
3.  Claude will use the `.claudecode.md` instructions to read the file, enter **Plan Mode**, and then write the finished marketing files to your `/assets` folder—a process that typically takes under seven minutes [4].

Would you like me to generate a **Tailored Report** detailing the specific marketing prompts the agent should use for the social media specifications?