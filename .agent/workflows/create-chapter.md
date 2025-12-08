---
description: Create a new textbook chapter with standardized structure and RAG-ready metadata
---

# 📚 Reusable Intelligence: Textbook Chapter Creation Skill

This agent skill serves as a reusable coding subagent to generate high-quality textbook content consistently.

## Steps

1. **Analyze Topic**
   - User provides: `{{TOPIC_NAME}}`
   - Agent researches: Key concepts, prerequisites, learning outcomes

2. **Generate Structure (Standardization)**
   Create a new file `frontend/docs/{{TOPIC_SLUG}}.md` with this Frontmatter:
   ```markdown
   ---
   title: {{TOPIC_NAME}}
   sidebar_label: {{TOPIC_SHORT_NAME}}
   description: {{TOPIC_SUMMARY}}
   tags: [physical-ai, robotics, {{TAGS}}]
   ---
   ```

3. **Content Generation (Pedagogical Pattern)**
   Write content following this pattern:
   - **Introduction**: Hook the reader
   - **Theory**: Core concepts with math/diagrams (Mermaid)
   - **Practice**: Code blocks (Python/C++)
   - **Applications**: Real-world Physical AI examples
   - **Interactive Components**: Add `<ChapterActions />`

4. **Enhancement**
   - Add "Ask AI" prompts
   - Verify links

## Usage
Run this skill to generate consistent, high-quality chapters that automatically integrate with the project's RAG system and Personalization engines.
