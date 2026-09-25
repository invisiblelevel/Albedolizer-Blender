import os
import subprocess
import json
import queue
import threading


CLI_TIMEOUT = 600
CREATE_NO_WINDOW = 0x08000000


def _run(cmd, timeout):
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


def _build_cmd(cli_path, albedo_path, output_dir, preset, correct_mode,
               ai_model, maps_string, engine, seamless, seamless_hipass,
               report_path):
    cmd = [
        cli_path,
        "-i", albedo_path,
        "-o", output_dir,
        "--preset", preset,
        "--maps", maps_string,
        "--json-report", report_path,
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

    return cmd


def run_generate(cli_path, albedo_path, output_dir, preset,
                 correct_mode, ai_model, maps_string, engine="",
                 seamless=False, seamless_hipass=True,
                 timeout=CLI_TIMEOUT, progress_callback=None):
    """Синхронная версия (оставлена на всякий случай)."""
    if not os.path.isfile(albedo_path):
        return False, f"Albedo not found: {albedo_path}"

    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        return False, f"Cannot create output dir: {e}"

    report_path = os.path.join(output_dir, "report.json")
    cmd = _build_cmd(cli_path, albedo_path, output_dir, preset, correct_mode,
                     ai_model, maps_string, engine, seamless, seamless_hipass,
                     report_path)

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=CREATE_NO_WINDOW if os.name == "nt" else 0,
            bufsize=1,
        )
    except FileNotFoundError:
        return False, f"Executable not found: {cli_path}"
    except PermissionError as e:
        return False, f"Permission denied (antivirus?): {e}"
    except OSError as e:
        return False, f"OS error: {e}"

    stderr_lines = []

    try:
        for line in proc.stdout:
            line = line.rstrip("\n")
            if line.startswith("PROGRESS:"):
                parts = line.split(":", 2)
                if len(parts) >= 2:
                    try:
                        pct = int(parts[1])
                        stage = parts[2] if len(parts) > 2 else ""
                        if progress_callback:
                            progress_callback(pct, stage)
                    except (ValueError, IndexError):
                        pass

        proc.wait(timeout=timeout)

        if proc.stderr:
            err_text = proc.stderr.read()
            if err_text:
                stderr_lines.append(err_text)

    except subprocess.TimeoutExpired:
        proc.kill()
        return False, f"CLI timeout after {timeout}s"
    except Exception as e:
        try:
            proc.kill()
        except Exception:
            pass
        return False, f"{type(e).__name__}: {e}"

    if os.path.isfile(report_path):
        try:
            with open(report_path, "r", encoding="utf-8") as f:
                report = json.load(f)
            if report.get("ok"):
                return True, report
            return False, report.get("message", "Unknown CLI error")
        except Exception as e:
            return False, f"Report parse error: {e}"

    err_preview = "".join(stderr_lines)[:300]
    return False, f"CLI exit {proc.returncode}: {err_preview}"


def run_generate_async(cli_path, albedo_path, output_dir, preset,
                       correct_mode, ai_model, maps_string, engine="",
                       seamless=False, seamless_hipass=True,
                       timeout=CLI_TIMEOUT, result_queue=None,
                       cancel_flag=None):
    """
    Асинхронная версия — CLI в отдельном потоке.
    result_queue получает:
      ("progress", pct, stage)
      ("done", ok, report_or_error)

    cancel_flag — опционально, threading.Event; если установлен — убивает процесс.
    """
    if result_queue is None:
        result_queue = queue.Queue()

    def worker():
        if not os.path.isfile(albedo_path):
            result_queue.put(("done", False, f"Albedo not found: {albedo_path}"))
            return

        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            result_queue.put(("done", False, f"Cannot create output dir: {e}"))
            return

        report_path = os.path.join(output_dir, "report.json")
        cmd = _build_cmd(cli_path, albedo_path, output_dir, preset, correct_mode,
                         ai_model, maps_string, engine, seamless, seamless_hipass,
                         report_path)

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=CREATE_NO_WINDOW if os.name == "nt" else 0,
                bufsize=1,
            )
        except FileNotFoundError:
            result_queue.put(("done", False, f"Executable not found: {cli_path}"))
            return
        except PermissionError as e:
            result_queue.put(("done", False, f"Permission denied (antivirus?): {e}"))
            return
        except OSError as e:
            result_queue.put(("done", False, f"OS error: {e}"))
            return

        stderr_lines = []

        try:
            # Читаем stdout в потоке — параллельно проверяем cancel_flag
            for line in proc.stdout:
                if cancel_flag is not None and cancel_flag.is_set():
                    proc.kill()
                    result_queue.put(("done", False, "Cancelled by user"))
                    return

                line = line.rstrip("\n")
                if line.startswith("PROGRESS:"):
                    parts = line.split(":", 2)
                    if len(parts) >= 2:
                        try:
                            pct = int(parts[1])
                            stage = parts[2] if len(parts) > 2 else ""
                            result_queue.put(("progress", pct, stage))
                        except (ValueError, IndexError):
                            pass

            proc.wait(timeout=timeout)

            if proc.stderr:
                err_text = proc.stderr.read()
                if err_text:
                    stderr_lines.append(err_text)

        except subprocess.TimeoutExpired:
            proc.kill()
            result_queue.put(("done", False, f"CLI timeout after {timeout}s"))
            return
        except Exception as e:
            try:
                proc.kill()
            except Exception:
                pass
            result_queue.put(("done", False, f"{type(e).__name__}: {e}"))
            return

        if os.path.isfile(report_path):
            try:
                with open(report_path, "r", encoding="utf-8") as f:
                    report = json.load(f)
                if report.get("ok"):
                    result_queue.put(("done", True, report))
                    return
                result_queue.put(("done", False, report.get("message", "Unknown CLI error")))
                return
            except Exception as e:
                result_queue.put(("done", False, f"Report parse error: {e}"))
                return

        err_preview = "".join(stderr_lines)[:300]
        result_queue.put(("done", False, f"CLI exit {proc.returncode}: {err_preview}"))

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    return thread, result_queue