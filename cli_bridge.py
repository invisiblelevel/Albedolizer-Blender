import os
import subprocess
import json


CLI_TIMEOUT = 600
CREATE_NO_WINDOW = 0x08000000


def _run(cmd, timeout):
    """Обёртка для subprocess с флагами Windows и обработкой ошибок."""
    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=CREATE_NO_WINDOW if os.name == "nt" else 0,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        raise RuntimeError(f"Executable not found: {cmd[0]}")
    except PermissionError as e:
        raise RuntimeError(f"Permission denied (antivirus?): {e}")
    except OSError as e:
        raise RuntimeError(f"OS error: {e}")


def check_cli(cli_path):
    if not cli_path or not os.path.isfile(cli_path):
        return False, f"CLI not found: {cli_path}"

    try:
        result = _run([cli_path, "--version"], timeout=10)
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, f"CLI returned code {result.returncode}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def run_generate(cli_path, albedo_path, output_dir, preset,
                 correct_mode, ai_model, maps_string, engine="",
                 seamless=False, seamless_hipass=True,
                 timeout=CLI_TIMEOUT):
    if not os.path.isfile(albedo_path):
        return False, f"Albedo not found: {albedo_path}"

    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        return False, f"Cannot create output dir: {e}"

    report_path = os.path.join(output_dir, "report.json")

    cmd = [
        cli_path,
        "-i", albedo_path,
        "-o", output_dir,
        "--preset", preset,
        "--maps", maps_string,
        "--json-report", report_path,
        "--silent",
    ]

    if correct_mode == "none":
        cmd += ["--correct", "none"]
    elif correct_mode == "ai":
        cmd += ["--correct", "ai", "--ai-model", ai_model]
    elif correct_mode == "math":
        cmd += ["--correct", "math"]

    if seamless:
        cmd += ["--seamless"]
        if not seamless_hipass:
            cmd += ["--seamless-no-hipass"]

    cmd += ["--pbr"]

    if engine:
        cmd += ["--engine", engine]

    try:
        result = _run(cmd, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f"CLI timeout after {timeout}s"
    except Exception as e:
        return False, str(e)

    if os.path.isfile(report_path):
        try:
            with open(report_path, "r", encoding="utf-8") as f:
                report = json.load(f)
            if report.get("ok"):
                return True, report
            return False, report.get("message", "Unknown CLI error")
        except Exception as e:
            return False, f"Report parse error: {e}"

    return False, f"CLI exit {result.returncode}: {result.stderr[:300]}"