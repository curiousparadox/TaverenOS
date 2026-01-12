# TaverenOS
Symbolic recursive AI system for field diagnostics, EEV compression, and ritual automation

## ChatGPT Export Processor

This repository includes a simple processor that converts exported ChatGPT conversations into Obsidian markdown notes. Run it with:

```bash
python -m taverenos path/to/export.json -o path/to/vault --thread my-thread
```

Use `-` as the input path to read from `stdin`. Notes are written into the specified vault directory with YAML frontmatter, tagged using symbolic keywords and autolinked with Obsidian `[[wikilinks]]`.

Tag weights are calculated with `tag_score = (occurrences / total_words) * 1000` and summed into the `symbolic_weight` field.
