"""Shell completion command for Obsidian Search Tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click
from click.shell_completion import BashComplete, FishComplete, ZshComplete


@click.command()
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"], case_sensitive=False))
def completion(shell: str) -> None:
    """Generate shell completion script.

    Generates completion scripts for bash, zsh, or fish shells to enable
    tab completion of commands, options, and arguments. This improves the
    command-line user experience by providing auto-completion suggestions.

    SHELL: The shell type (bash, zsh, fish)

    \b
    INSTALLATION INSTRUCTIONS:

    \b
    Bash (≥4.4) - Add to ~/.bashrc:
        eval "$(obsidian-search-tool completion bash)"

    \b
    Zsh - Add to ~/.zshrc:
        eval "$(obsidian-search-tool completion zsh)"

    \b
    Fish (≥3.0) - Save to completions directory:
        obsidian-search-tool completion fish > ~/.config/fish/completions/obsidian-search-tool.fish

    \b
    For immediate effect without restarting shell:
        # Bash
        source ~/.bashrc

        # Zsh
        source ~/.zshrc

        # Fish (automatic on save)

    \b
    EXAMPLES:

    \b
        # Generate bash completion script
        obsidian-search-tool completion bash

    \b
        # Install bash completion temporarily (current session)
        eval "$(obsidian-search-tool completion bash)"

    \b
        # Install bash completion permanently
        echo 'eval "$(obsidian-search-tool completion bash)"' >> ~/.bashrc
        source ~/.bashrc

    \b
        # Install zsh completion permanently
        echo 'eval "$(obsidian-search-tool completion zsh)"' >> ~/.zshrc
        source ~/.zshrc

    \b
        # Install fish completion (persistent)
        mkdir -p ~/.config/fish/completions
        obsidian-search-tool completion fish > ~/.config/fish/completions/obsidian-search-tool.fish

    \b
    PERFORMANCE TIP:
        For better shell startup performance, save completion to a file
        instead of generating on every shell startup:

        # Bash
        obsidian-search-tool completion bash > ~/.obsidian-search-tool-complete.bash
        echo 'source ~/.obsidian-search-tool-complete.bash' >> ~/.bashrc

        # Zsh
        obsidian-search-tool completion zsh > ~/.obsidian-search-tool-complete.zsh
        echo 'source ~/.obsidian-search-tool-complete.zsh' >> ~/.zshrc

    \b
    WHAT GETS COMPLETED:
        - Command names (status, auth, search, completion)
        - Options (--json, --text, --verbose, etc.)
        - Choice values (--type dataview|jsonlogic)
        - File paths (where applicable)

    \b
    SUPPORTED SHELLS:
        - Bash (version 4.4 or higher)
        - Zsh (any recent version)
        - Fish (version 3.0 or higher)
        - PowerShell: Not supported by Click

    \b
    TROUBLESHOOTING:
        If completion doesn't work:
        1. Ensure shell version meets requirements (bash --version, zsh --version, fish --version)
        2. Verify installation by checking shell config file
        3. Restart shell or source config file
        4. Check that obsidian-search-tool is in PATH: which obsidian-search-tool
    """
    ctx = click.get_current_context()

    # Map shell names to their completion classes
    completion_classes = {
        "bash": BashComplete,
        "zsh": ZshComplete,
        "fish": FishComplete,
    }

    shell_lower = shell.lower()
    completion_class = completion_classes.get(shell_lower)

    if not completion_class:
        raise click.BadParameter(f"Unsupported shell: {shell}. Supported shells: bash, zsh, fish")

    # Get the root command (main group) for completion
    # Navigate up to the parent command if we're in a subcommand
    root_cmd = ctx.parent.command if ctx.parent else ctx.command

    # Create completer instance with CLI context
    completer = completion_class(
        cli=root_cmd,
        ctx_args={},
        prog_name="obsidian-search-tool",
        complete_var="_OBSIDIAN_SEARCH_TOOL_COMPLETE",
    )

    # Output the completion script
    click.echo(completer.source())
