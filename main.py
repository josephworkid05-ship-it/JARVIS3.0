"""
JARVIS - Personal AI Assistant (Version 0.1)
Main Entry Point & Interactive Terminal Interface
"""
import sys
import os
import json
import time

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.env_loader import load_dotenv, setup_windows_anaconda_paths
setup_windows_anaconda_paths()
load_dotenv()

from utils.logger import setup_logging
setup_logging()

from config.settings import settings
from core.agent import JarvisAgent
from tools import create_default_registry

# ANSI color codes for sleek terminal styling
CYAN = "\033[96m"
BLUE = "\033[94m"
GOLD = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Windows console encoding and ANSI color support check
if sys.platform == "win32":
    try:
        if sys.version_info >= (3, 7) and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        elif hasattr(sys.stdout, "buffer"):
            import codecs
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "replace")
            sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "replace")
    except Exception:
        pass

    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        CYAN = BLUE = GOLD = GREEN = RED = DIM = BOLD = RESET = ""

JARVIS_BANNER = f"""{CYAN}{BOLD}
   .--------------------------------------------------------------.
  /  +---+   STARK INDUSTRIES INTEGRATED NEURAL NETWORK           \\
 |   | O |   J.A.R.V.I.S. — PERSONAL AUTONOMOUS AGENT (PHASE 3)    |
 |   +---+   [VOICE INTERFACE, REASONING & MACHINE LEARNING]       |
  \\                                                               /
   '--------------------------------------------------------------'
{RESET}{DIM}  Just A Rather Very Intelligent System — ML & Neural Operations v0.3{RESET}
"""

def print_hud_status(agent: JarvisAgent):
    """Print the startup telemetry and system status."""
    provider = agent.provider_name.upper()
    tools_count = len(agent.registry.list_tools())
    tool_names = ", ".join(agent.registry.get_tool_names())
    voice_status = f"{GREEN}ACTIVE{RESET}" if (agent.voice and agent.voice.enabled) else f"{RED}MUTED{RESET}"

    from ml import get_ml_manager
    ml_models_count = len(get_ml_manager().list_models())

    border = "=" * 64
    print(f"{BLUE}+{border}+{RESET}")
    print(f"{BLUE}|{RESET}  {BOLD}STARK TELEMETRY HUD // SYSTEM DIAGNOSTICS{RESET}{' ' * 21}{BLUE}|{RESET}")
    print(f"{BLUE}+{border}+{RESET}")
    print(f"{BLUE}|{RESET}  * Status    : {GREEN}ONLINE // SYSTEMS NOMINAL{RESET}{' ' * 27}{BLUE}|{RESET}")
    print(f"{BLUE}|{RESET}  * Core Mode : {GOLD}{provider:<12}{RESET}{' ' * 36}{BLUE}|{RESET}")
    print(f"{BLUE}|{RESET}  * Identity  : {CYAN}{settings.ASSISTANT_NAME:<15}{RESET}{' ' * 33}{BLUE}|{RESET}")
    print(f"{BLUE}|{RESET}  * Operator  : {CYAN}{settings.USER_NAME:<15}{RESET}{' ' * 33}{BLUE}|{RESET}")
    print(f"{BLUE}|{RESET}  * ML Models : {GREEN}{ml_models_count} registered{RESET}{' ' * (37 - len(str(ml_models_count)))}{BLUE}|{RESET}")
    print(f"{BLUE}|{RESET}  * Vocalizer : {voice_status:<20}{' ' * 30}{BLUE}|{RESET}")
    print(f"{BLUE}|{RESET}  * Tools ({tools_count}) : {DIM}{tool_names[:43] + '...':<46}{RESET}{BLUE}|{RESET}")
    print(f"{BLUE}|{RESET}  * Web HUD   : {CYAN}http://{settings.WEB_HOST}:{settings.WEB_PORT:<28}{RESET}{BLUE}|{RESET}")
    print(f"{BLUE}+{border}+{RESET}\n")
    
    if agent.provider_name == "mock":
        print(f"{GOLD}[Notice] Running in Local Autonomous Simulation Mode.{RESET}")
        print(f"{DIM}To connect live LLM intelligence, add your OPENAI_API_KEY or GEMINI_API_KEY to .env{RESET}\n")
    else:
        print(f"{GREEN}[Uplink] Neural reasoning engine connected via {provider}.{RESET}\n")

def create_event_callback():
    """Create terminal event logger for agent reasoning steps."""
    def on_event(event_type: str, data: dict):
        if event_type == "thinking":
            print(f"{DIM}  [Reasoning cycle #{data.get('step', 1)}...]{RESET}")
        elif event_type == "tool_call":
            tool = data.get("tool")
            args = data.get("arguments", {})
            thought = data.get("thought", "")
            if thought:
                print(f"{DIM}  Thought: {thought}{RESET}")
            print(f"{CYAN}  [*] Invoking Tool: {BOLD}{tool}{RESET}{CYAN}({json.dumps(args)}){RESET}")
        elif event_type == "tool_result":
            success = data.get("success", False)
            out = data.get("output", "")
            preview = out if len(out) <= 120 else out[:117] + "..."
            status_color = GREEN if success else RED
            indicator = "[+]" if success else "[-]"
            print(f"{status_color}  {indicator} Result: {preview}{RESET}")
        elif event_type == "voice":
            print(f"{GOLD}  [~] Vocalizing response to speaker...{RESET}")
    return on_event

def handle_slash_command(cmd: str, agent: JarvisAgent) -> bool:
    """Handle special terminal commands. Returns True if handled, False otherwise."""
    parts = cmd.strip().split()
    root_cmd = parts[0].lower()

    if root_cmd in ("/help", "/?"):
        print(f"\n{BOLD}Available Commands:{RESET}")
        print(f"  {CYAN}/help{RESET}             - Display this command manual")
        print(f"  {CYAN}/voice [on|off]{RESET}   - Enable or mute vocalizer synthesis")
        print(f"  {CYAN}/web{RESET}              - Display Stark Industries Web HUD launcher info")
        print(f"  {CYAN}/ml [models|data]{RESET} - Inspect registered Machine Learning models and datasets")
        print(f"  {CYAN}/tools{RESET}            - Inspect registered tools and parameter specifications")
        print(f"  {CYAN}/status{RESET}           - Display active telemetry, model, and memory count")
        print(f"  {CYAN}/clear{RESET}            - Clear conversation memory history")
        print(f"  {CYAN}/save [file]{RESET}      - Save conversation memory to JSON (default: data/history.json)")
        print(f"  {CYAN}/load [file]{RESET}      - Load conversation memory from JSON")
        print(f"  {CYAN}/exit{RESET}             - Power down JARVIS and terminate session\n")
        return True

    elif root_cmd == "/ml":
        from ml import get_ml_manager
        ml_mgr = get_ml_manager()
        sub = parts[1].lower() if len(parts) > 1 else "models"

        if sub in ("models", "list"):
            models = ml_mgr.list_models()
            print(f"\n{BOLD}Registered Machine Learning Models ({len(models)}):{RESET}")
            if not models:
                print(f"  {DIM}No models currently registered. Train one using 'train model on <dataset>'.{RESET}")
            for m in models:
                metrics = m.get("evaluation_metrics", {})
                acc = metrics.get("accuracy") or metrics.get("r2") or metrics.get("silhouette_score") or "N/A"
                print(f"  • {CYAN}{m['model_name']}{RESET} [{GOLD}{m['version']}{RESET}] - {m['task_type'].upper()} ({m['model_type']}) | Metric: {acc}")
            print("")
        elif sub in ("data", "datasets"):
            ds_list = [f for f in os.listdir(settings.ML_DATASETS_DIR) if f.endswith((".csv", ".json"))]
            print(f"\n{BOLD}Available Datasets in ml/datasets/ ({len(ds_list)}):{RESET}")
            for d in ds_list:
                print(f"  • {CYAN}{d}{RESET}")
            print("")
        else:
            print(f"Usage: {CYAN}/ml [models|datasets]{RESET}\n")
        return True

    elif root_cmd == "/voice":
        if len(parts) > 1:
            state = parts[1].lower() in ("on", "true", "enable", "1")
            agent.voice.set_enabled(state)
        else:
            agent.voice.set_enabled(not agent.voice.enabled)
        status_text = f"{GREEN}ENABLED{RESET}" if agent.voice.enabled else f"{RED}MUTED{RESET}"
        print(f"Vocalizer status: {status_text}\n")
        return True

    elif root_cmd == "/web":
        print(f"\n{BOLD}Stark Industries Web HUD:{RESET}")
        print(f"  URL     : {CYAN}http://{settings.WEB_HOST}:{settings.WEB_PORT}{RESET}")
        print(f"  To start: {GOLD}py web/app.py{RESET}\n")
        return True

    elif root_cmd == "/tools":
        print(f"\n{BOLD}Registered Tools & Capabilities:{RESET}")
        for t in agent.registry.list_tools():
            print(f"  • {CYAN}{t.name}{RESET}: {t.description}")
            params = t.parameters.get("properties", {})
            if params:
                print(f"    {DIM}Parameters: {json.dumps(params)}{RESET}")
        print("")
        return True

    elif root_cmd == "/status":
        v_stat = "ENABLED" if (agent.voice and agent.voice.enabled) else "MUTED"
        print(f"\n{BOLD}Diagnostics:{RESET}")
        print(f"  Provider       : {agent.provider_name}")
        print(f"  Vocalizer      : {v_stat}")
        print(f"  Memory Entries : {len(agent.memory.messages)}")
        print(f"  Max Steps      : {agent.max_steps}")
        print(f"  Memory Limit   : {settings.MEMORY_WINDOW_SIZE * 2} messages\n")
        return True

    elif root_cmd == "/clear":
        agent.reset_conversation()
        print(f"{GREEN}Conversation memory wiped clean.{RESET}\n")
        return True

    elif root_cmd == "/save":
        target = parts[1] if len(parts) > 1 else os.path.join(settings.DATA_DIR, "conversation_history.json")
        if agent.memory.save_to_file(target):
            print(f"{GREEN}Memory successfully saved to {target}{RESET}\n")
        else:
            print(f"{RED}Failed to save memory to {target}{RESET}\n")
        return True

    elif root_cmd == "/load":
        target = parts[1] if len(parts) > 1 else os.path.join(settings.DATA_DIR, "conversation_history.json")
        if agent.memory.load_from_file(target):
            print(f"{GREEN}Memory loaded ({len(agent.memory.messages)} entries) from {target}{RESET}\n")
        else:
            print(f"{RED}Failed to load memory from {target}{RESET}\n")
        return True

    elif root_cmd in ("/exit", "/quit", "/q"):
        print(f"\n{CYAN}Powering down systems. Have a pleasant day, {settings.USER_NAME}.{RESET}\n")
        sys.exit(0)

    return False

def main():
    print(JARVIS_BANNER)
    
    # Initialize Agent
    agent = JarvisAgent()
    print_hud_status(agent)

    event_callback = create_event_callback()

    print(f"{DIM}Type your prompt below or use /help for commands. Press Ctrl+C to exit.{RESET}\n")

    while True:
        try:
            user_input = input(f"{BOLD}{settings.USER_NAME}>{RESET} ").strip()
            if not user_input:
                continue

            # Check for slash commands
            if user_input.startswith("/"):
                if handle_slash_command(user_input, agent):
                    continue

            # Run agent loop
            print(f"{DIM}{settings.ASSISTANT_NAME} is processing...{RESET}")
            response = agent.run(user_input, on_event=event_callback)

            # Display response
            print(f"\n{CYAN}{BOLD}{settings.ASSISTANT_NAME}:{RESET} {response}\n")

        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{CYAN}Standby mode engaged. Goodbye, {settings.USER_NAME}.{RESET}\n")
            break
        except Exception as e:
            print(f"\n{RED}[System Anomaly] {str(e)}{RESET}\n")

if __name__ == "__main__":
    main()
