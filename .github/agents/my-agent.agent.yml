name: portfolio-necromancer-dev-agent
version: "1.0"

description: >
  Development agent for Portfolio Necromancer.
  Runs tasks using prompts stored in /agent/prompts and Python tools
  stored in /agent/tools. Designed for GitHub Actions + local CLI use.

model:
  provider: openai
  model: gpt-4.1
  temperature: 0.2

prompts:
  scraping: "agent/prompts/scraping.md"
  summarizing: "agent/prompts/summarizing.md"
  generation: "agent/prompts/generation.md"

tools:
  scrape:   "agent/tools/scrape.py"
  categorize: "agent/tools/categorize.py"
  summarize:  "agent/tools/summarize.py"
  generate:   "agent/tools/generate_site.py"

workflow:
  default:
    - scrape
    - categorize
    - summarize
    - generate
