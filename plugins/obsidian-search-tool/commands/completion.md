---
description: Generate shell completion script
argument-hint: bash|zsh|fish
---

Generate shell completion scripts for bash, zsh, or fish.

## Usage

```bash
obsidian-search-tool completion SHELL
```

## Arguments

- `SHELL`: Shell type (bash, zsh, or fish)

## Examples

```bash
# Generate bash completion
eval "$(obsidian-search-tool completion bash)"

# Install zsh completion permanently
echo 'eval "$(obsidian-search-tool completion zsh)"' >> ~/.zshrc

# Install fish completion
mkdir -p ~/.config/fish/completions
obsidian-search-tool completion fish > ~/.config/fish/completions/obsidian-search-tool.fish
```

## Output

Outputs shell-specific completion script to stdout.
