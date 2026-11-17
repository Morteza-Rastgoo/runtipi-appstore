#!/usr/bin/env python3
"""Operator dispatch command for the oz-agent-worker "command" backend.

Based on Warp's reference ``examples/command-backend/dispatch-oz-local.py``. The
worker hands this script a versioned ``DispatchPayload`` (JSON) on stdin for each
task; we run the host ``oz`` CLI for real, in our local project directory, so the
factory's first project is this box's ``~/projects/Phone-Projects`` (mounted into
the worker container at ``/workspace/phone-projects``).

What it does:
  1. reads the ``DispatchPayload`` on stdin,
  2. writes the full payload to ``OZ_LOCAL_RUN_LOG_DIR/payload-<run_id>.json`` for
     inspection,
  3. launches ``$OZ_BIN <base_args...>`` detached (fire-and-forget) with the
     payload's ``env`` overlaid on the worker's environment, in ``OZ_PROJECT_DIR``
     (our local project), writing the run's output to a per-task log; once the CLI
     exits, the same wrapper reports completion via
     ``$OZ_BIN harness-support --run-id <run_id> report-shutdown`` (the command
     backend contract),
  4. exits 0 once the run is launched. The agent reports its own terminal state to
     the server (``base_args`` already carries ``--task-id`` / ``--server-root-url``).

Required environment:
  OZ_BIN                Path to the oz/Warp binary to exec (base_args is appended).

Optional environment:
  OZ_PROJECT_DIR        Working directory for the agent run
                        (default: /workspace/phone-projects).
  OZ_LOCAL_RUN_LOG_DIR  Directory for per-task payload + run logs (default: /tmp).

Exit 0   => run launched (the worker treats the task as dispatched).
Exit !=0 => failed to launch; the worker marks the task failed.
"""

import json
import os
import shlex
import subprocess
import sys


def main():
    oz_bin = os.environ.get("OZ_BIN")
    if not oz_bin:
        sys.stderr.write("OZ_BIN must be set to the oz/Warp binary path\n")
        return 2

    # `or` (not the get() default) so an empty-string env var still falls back.
    project_dir = os.environ.get("OZ_PROJECT_DIR") or "/workspace/phone-projects"
    log_dir = os.environ.get("OZ_LOCAL_RUN_LOG_DIR") or "/tmp"

    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        sys.stderr.write("invalid dispatch payload on stdin: %s\n" % exc)
        return 1

    run_id = payload.get("run_id", "unknown")
    base_args = payload.get("base_args") or []
    env_overlay = payload.get("env") or {}

    if not base_args:
        sys.stderr.write("payload has no base_args; nothing to run\n")
        return 1

    try:
        os.makedirs(log_dir, exist_ok=True)
    except OSError as exc:
        sys.stderr.write("failed to create log dir %s: %s\n" % (log_dir, exc))
        return 1

    # Persist the full payload so the forwarded contents are easy to inspect.
    payload_path = os.path.join(log_dir, "payload-%s.json" % run_id)
    with open(payload_path, "w", encoding="utf-8") as payload_file:
        json.dump(payload, payload_file, indent=2, sort_keys=True)

    # Log a summary so the worker log shows exactly what was forwarded.
    sys.stderr.write(
        "[dispatch-oz] run_id=%s execution_id=%s image=%s\n"
        % (run_id, payload.get("execution_id", ""), payload.get("docker_image", ""))
    )
    sys.stderr.write(
        "[dispatch-oz] project_dir: %s\n" % project_dir
    )
    sys.stderr.write(
        "[dispatch-oz] base_args: %s\n"
        % " ".join(shlex.quote(arg) for arg in base_args)
    )
    sys.stderr.write(
        "[dispatch-oz] env keys: %s\n" % ", ".join(sorted(env_overlay))
    )
    sys.stderr.write("[dispatch-oz] full payload: %s\n" % payload_path)

    # Inherit the worker's environment (which carries our local LLM + Android SDK
    # config from worker.yaml's command.environment) and overlay the task env.
    child_env = dict(os.environ)
    child_env.update({str(key): str(value) for key, value in env_overlay.items()})

    run_log_path = os.path.join(log_dir, "oz-run-%s.log" % run_id)

    # The command backend contract: once the CLI exits, report completion by
    # running `oz harness-support report-shutdown` with the run ID. Chain the run
    # and the report inside one detached shell so this dispatch command can return
    # immediately (fire-and-forget).
    run_cmd = " ".join(shlex.quote(arg) for arg in [oz_bin, *base_args])
    report_cmd = " ".join(
        shlex.quote(arg)
        for arg in [oz_bin, "harness-support", "--run-id", str(run_id), "report-shutdown"]
    )
    wrapper = "%s; %s" % (run_cmd, report_cmd)

    try:
        run_log = open(run_log_path, "ab")
    except OSError as exc:
        sys.stderr.write("failed to open run log %s: %s\n" % (run_log_path, exc))
        return 1

    # Run the agent in our local project directory so the first project is this
    # box's Phone-Projects checkout (not a fresh server-side clone).
    try:
        proc = subprocess.Popen(
            ["/bin/sh", "-c", wrapper],
            env=child_env,
            cwd=project_dir,
            stdin=subprocess.DEVNULL,
            stdout=run_log,
            stderr=run_log,
            start_new_session=True,
        )
    except OSError as exc:
        sys.stderr.write("failed to launch oz run: %s\n" % exc)
        return 1
    finally:
        run_log.close()

    sys.stderr.write(
        "[dispatch-oz] launched pid=%s; run output -> %s\n" % (proc.pid, run_log_path)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
