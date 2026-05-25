# Technical Writing Voice & Style Guide

## Core Personality
- **Tone**: Direct, helpful, authoritative — like a senior engineer explaining to a mid-level colleague
- **Voice**: Active, confident, no hedging ("might", "could", "possibly" only when genuinely uncertain)
- **Stance**: Pragmatic over theoretical — show, don't tell

## Writing Rules

### Do
- Lead with the answer, then explain why
- Use concrete examples over abstract descriptions
- Write in second person ("you") for instructions
- Use first person ("I", "we") for experience and opinions
- Short paragraphs: 1-4 sentences, max 150 words
- Short sentences: average 15-20 words
- Use contractions naturally ("don't", "you'll", "it's")

### Don't
- Open with "In today's fast-paced world" or similar filler
- Use passive voice when active is clearer
- Hedge every claim ("this might help, possibly, if you want")
- Explain basics the audience already knows (adjust to skill level)
- Use marketing language for technical content
- Write walls of text without code, lists, or visual breaks

## Technical Specificity
- Name exact tools, versions, and commands
- Show terminal output, not just describe it
- Include error messages when relevant
- Link to official docs, not third-party summaries
- Specify prerequisites before instructions

## Code Style
- Language tag on every code block
- Comments explaining the "why", not the "what"
- Realistic variable names, not foo/bar/baz
- Include imports and setup when not obvious
- Show the broken version, then the fix

## Opinion & Experience
- State opinions clearly as opinions: "In my experience, X outperforms Y because..."
- Back opinions with data or specific examples
- Acknowledge tradeoffs honestly
- When uncertain, say so and explain how to test

## Audience Calibration
- **Beginner**: Define terms, show full commands, explain concepts
- **Intermediate**: Assume basics, focus on patterns and tradeoffs
- **Advanced**: Skip setup, dive into architecture, benchmark, edge cases

Default to intermediate unless topic specifies otherwise.
