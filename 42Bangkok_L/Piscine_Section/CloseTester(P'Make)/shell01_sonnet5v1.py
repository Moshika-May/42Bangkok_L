#!/usr/bin/env python3
"""
42 Piscine - Shell01 Adversarial Tester
------------------------------------------
Same philosophy as shell00_tester.py / c00_tester.py:

  * CORE  = tests a rule stated in the subject; counts toward score/rank.
  * TRAP  = adversarial/edge case; informational only, never affects score.
  * Every test carries a WHY and, on failure, a HINT.
  * -v / --verbose prints the WHY for every test (even passing ones).

Design notes specific to this set:

  - ex01/ex04/ex07 are inherently host-dependent (groups, MAC address,
    /etc/passwd content). Rather than hardcoding an expected string, the
    tester recomputes the reference live, on the same machine, at test
    time -- exactly the situation the subject describes with "Your script
    will be tested in our own environment."
  - ex01 and ex04 deliberately never create system users/groups or touch
    real network config: only pre-existing accounts (root, daemon, the
    user actually running the tester) and read-only /sys/class/net data
    are used, so running this tester never mutates your machine.
  - ex05's required filename is reconstructed programmatically (not typed
    as a literal Python string) to avoid any risk of a copy/paste mistake
    with a name built entirely out of shell metacharacters.
  - ex08's FT_NBR1/FT_NBR2 example values in the PDF are shown with heavy
    backslash-escaping that's ambiguous to reverse-engineer exactly as
    typed. Instead of guessing at that escaping, the tester derives its
    own values mathematically from the three custom-base alphabets the
    subject defines, verifies they independently decode to the subject's
    own worked answer ("Salut"), and tests against those -- see ex08 for
    details. This sidesteps shell-quoting ambiguity entirely since values
    are passed straight through Python's subprocess env, never typed at
    a shell prompt.

Usage:
    python3 shell01_tester.py            # normal run, all exercises
    python3 shell01_tester.py -v         # verbose: show rationale for every test
    python3 shell01_tester.py ex07       # only run a specific exercise
"""

import os
import re
import sys
import stat
import shutil
import tempfile
import subprocess
from dataclasses import dataclass

# --- ANSI COLORS ---
C_RESET = "\033[0m"
C_GREEN = "\033[32m"
C_RED = "\033[31m"
C_YELLOW = "\033[33m"
C_CYAN = "\033[36m"
C_WHITE = "\033[37m"
C_MAGENTA = "\033[35m"
C_DIM = "\033[2m"
C_BOLD = "\033[1m"

VERBOSE = "-v" in sys.argv or "--verbose" in sys.argv


@dataclass
class Result:
    name: str
    cat: str          # "CORE" or "TRAP"
    passed: bool
    got: str
    expected: str
    inputs: str
    why: str
    hint: str


def trunc(s, n=200):
    s = "" if s is None else str(s)
    s = s.replace("\n", "\\n")
    return s if len(s) <= n else s[: n - 15] + "...(truncated)"


def run_sh(path, cwd=None, env=None, timeout=5, args=None):
    """Runs a submitted file with /bin/sh, from an absolute path so it's
    never accidentally treated as part of the fixture directory it's
    being tested against (matches the general rule: 'Shell exercises must
    be executable with /bin/sh')."""
    cmd = ["/bin/sh", os.path.abspath(path)] + (args or [])
    try:
        return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True,
                               text=True, timeout=timeout, errors="replace")
    except subprocess.TimeoutExpired:
        return None
    except OSError as e:
        return e


def missing_file_result(name, path):
    return [Result(name, "CORE", False, "file not found", f"a file at {path}",
                    "(turn-in check)",
                    "This file is required by the subject's turn-in list.",
                    f"Create/submit {path} as specified in the subject.")]


def existing_user(candidates):
    """Returns the first username from `candidates` that actually exists
    on this machine, so tests never depend on an account that may not be
    present (e.g. a container without 'ubuntu')."""
    import pwd
    for name in candidates:
        try:
            pwd.getpwnam(name)
            return name
        except KeyError:
            continue
    return None


# ==========================================================================
#  ex01 : print_groups.sh
# ==========================================================================
def test_ex01(dirpath):
    results = []
    path = os.path.join(dirpath, "print_groups.sh")
    if not os.path.isfile(path):
        return missing_file_result("print_groups.sh exists", path)

    import pwd as pwdmod
    current_user = pwdmod.getpwuid(os.getuid()).pw_name
    candidates = ["root", "daemon", current_user]
    tested_any = False

    for user in candidates:
        if existing_user([user]) is None:
            continue
        tested_any = True
        ref = subprocess.run(["id", "-Gn", user], capture_output=True, text=True)
        if ref.returncode != 0:
            continue
        ref_str = ",".join(ref.stdout.split())

        env = dict(os.environ)
        env["FT_USER"] = user
        r = run_sh(path, env=env, timeout=5)
        out = (r.stdout or "").strip("\n") if r is not None else None

        results.append(Result(
            f"FT_USER={user}: correct comma-separated group list", "CORE", out == ref_str,
            trunc(out) if out is not None else "(timeout)", trunc(ref_str), f"FT_USER={user}",
            "Baseline: must reproduce the same groups `id -Gn` reports for this user, comma-joined.",
            "`id -Gn \"$FT_USER\"` gives a space-separated list -- pipe it through `tr ' ' ','` (or similar) to get commas."
        ))

    if not tested_any:
        results.append(Result(
            "At least one test account is available", "CORE", False, "none of root/daemon/<current user> found",
            "root or daemon to exist", "(environment check)",
            "Needed to evaluate this exercise at all.", "This is an environment issue, not your submission."
        ))
        return results

    # TRAP: output must contain no spaces at all (subject is explicit about this)
    env = dict(os.environ)
    env["FT_USER"] = "root"
    r = run_sh(path, env=env, timeout=5)
    out = (r.stdout or "") if r is not None else ""
    results.append(Result(
        "Output contains no spaces", "TRAP", " " not in out.strip("\n"),
        trunc(out), "no space characters anywhere in the output", "FT_USER=root",
        "Subject: 'The output should be comma-separated, without spaces.'",
        "If you used `tr ' ' ','` but your groups list itself never had spaces to begin with, this trap wouldn't catch much -- but a leftover `, ` (comma+space) join would."
    ))
    return results


# ==========================================================================
#  ex02 : find_sh.sh
# ==========================================================================
def test_ex02(dirpath):
    results = []
    path = os.path.join(dirpath, "find_sh.sh")
    if not os.path.isfile(path):
        return missing_file_result("find_sh.sh exists", path)

    tmp = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(tmp, "sub"))
        sh_files = ["top.sh", os.path.join("sub", "nested.sh")]
        other_files = ["notsh.txt", "readme.md"]
        for f in sh_files + other_files:
            open(os.path.join(tmp, f), "w").close()

        r = run_sh(path, cwd=tmp, timeout=5)
        out = (r.stdout or "") if r is not None else ""
        got_set = set(l for l in out.split("\n") if l)
        expected_set = {"top", "nested"}

        results.append(Result(
            "Finds every .sh file recursively, extension stripped", "CORE", got_set == expected_set,
            trunc(", ".join(sorted(got_set))) if got_set else "(no output)",
            trunc(", ".join(sorted(expected_set))), "top.sh, sub/nested.sh, notsh.txt, readme.md",
            "Baseline: subject asks for every .sh file in the current directory and subdirectories, name only (no .sh suffix).",
            "`find . -name \"*.sh\"` then strip the extension (basename ... .sh, or sed/cut) -- make sure the search isn't limited to the top level (-maxdepth)."
        ))

        wrongly_included = got_set - expected_set
        results.append(Result(
            "Does not include non-.sh files", "TRAP", len(wrongly_included) == 0,
            trunc(", ".join(wrongly_included)) if wrongly_included else "none", "no extras beyond top, nested",
            "(sanity check)", "A loose pattern (e.g. matching any file containing 'sh') would over-match.",
            "Double check your -name pattern is exactly \"*.sh\"."
        ))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ==========================================================================
#  ex03 : count_files.sh
# ==========================================================================
def test_ex03(dirpath):
    results = []
    path = os.path.join(dirpath, "count_files.sh")
    if not os.path.isfile(path):
        return missing_file_result("count_files.sh exists", path)

    tmp = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(tmp, "sub1", "sub2"))
        for f in ("a", "b", os.path.join("sub1", "c")):
            open(os.path.join(tmp, f), "w").close()
        # entries: ".", "a", "b", "sub1", "sub1/c", "sub1/sub2" = 6
        r = run_sh(path, cwd=tmp, timeout=5)
        out = (r.stdout or "").strip() if r is not None else None
        results.append(Result(
            "Counts files+dirs recursively, including \".\"", "CORE", out == "6",
            trunc(out) if out is not None else "(timeout)", "6", "., a, b, sub1/, sub1/c, sub1/sub2/",
            "Subject: count regular files and directories in cwd and subdirectories, including \".\" itself.",
            "`find . | wc -l` does exactly this in one line; if you're off by one, check whether you're counting \".\" or not."
        ))

        tmp2 = tempfile.mkdtemp()
        try:
            r2 = run_sh(path, cwd=tmp2, timeout=5)
            out2 = (r2.stdout or "").strip() if r2 is not None else None
            results.append(Result(
                "Empty directory still counts as 1 (just \".\")", "TRAP", out2 == "1",
                trunc(out2) if out2 is not None else "(timeout)", "1", "empty directory",
                "Degenerate case: with nothing inside, the count should still include the starting directory itself.",
                "If this prints 0, you're probably not counting \".\" -- `find .` always lists it first."
            ))
        finally:
            shutil.rmtree(tmp2, ignore_errors=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ==========================================================================
#  ex04 : MAC.sh
# ==========================================================================
def _live_mac_addresses():
    macs = []
    net_dir = "/sys/class/net"
    if not os.path.isdir(net_dir):
        return macs
    for iface in os.listdir(net_dir):
        if iface == "lo":
            continue
        addr_path = os.path.join(net_dir, iface, "address")
        if os.path.isfile(addr_path):
            try:
                with open(addr_path) as f:
                    macs.append(f.read().strip().lower())
            except OSError:
                continue
    return macs


def test_ex04(dirpath):
    results = []
    path = os.path.join(dirpath, "MAC.sh")
    if not os.path.isfile(path):
        return missing_file_result("MAC.sh exists", path)

    ref = _live_mac_addresses()
    if not ref:
        return [Result("Machine has a non-loopback network interface", "CORE", False,
                        "no interfaces found under /sys/class/net (besides lo)", "at least one",
                        "(environment check)", "Needed to evaluate this exercise at all.",
                        "This is an environment issue, not your submission.")]

    r = run_sh(path, timeout=5)
    out = (r.stdout or "") if r is not None else ""
    got = set(l.strip().lower() for l in out.split("\n") if l.strip())
    ref_set = set(ref)

    results.append(Result(
        "Prints this machine's MAC address(es), one per line", "CORE", got == ref_set,
        trunc(", ".join(sorted(got))) if got else "(no output)", trunc(", ".join(sorted(ref_set))),
        "(live network interfaces)",
        "Baseline: must match this machine's real MAC address(es) -- computed live since it's obviously machine-specific.",
        "`ifconfig` (look for 'ether') or `ip link show` (look for 'link/ether') both expose this; make sure you're not also printing the loopback interface (which has no real MAC)."
    ))

    all_zero = any(re.fullmatch(r"(00:){5}00", a) for a in got)
    results.append(Result(
        "Does not report the loopback's all-zero address", "TRAP", not all_zero,
        "an all-zero address was included" if all_zero else "none found", "no 00:00:00:00:00:00 entries",
        "(sanity check)",
        "The loopback interface has no real MAC; a solution that naively lists every interface without filtering would include it.",
        "Filter out 'lo' explicitly, or rely on a tool (ifconfig/ip) that already only shows 'ether'-type interfaces."
    ))
    return results


# ==========================================================================
#  ex05 : Can you create it ?
# ==========================================================================
def _marvin_filename():
    # Built character-by-character (never typed as one literal Python
    # string) to eliminate any risk of a copy/paste slip with a name
    # made entirely of shell metacharacters: " \ ? $ * '
    chars = ['"', '\\', '?', '$', '*', "'", 'M', 'a', 'R', 'V', 'i', 'N',
             "'", '*', '$', '?', '\\', '"']
    return "".join(chars)


def test_ex05(dirpath):
    results = []
    target = _marvin_filename()
    matches = [n for n in os.listdir(dirpath)] if os.path.isdir(dirpath) else []
    found = target in matches
    path = os.path.join(dirpath, target)

    results.append(Result(
        "A file with the exact required name exists", "CORE", found,
        trunc(repr(matches)) if not found else f"found: {target!r}",
        f"a file named {target!r}", "(turn-in check)",
        "The subject's turn-in filename is deliberately built from shell metacharacters (\" \\ ? $ * ') to force you to actually understand quoting/escaping when creating it.",
        "Something like: touch -- \"\\\\?\\$*'MaRViN'*\\$?\\\\\" (escape each special character, or build it with printf/mkdir tricks) -- verify with `ls -b` which shows escape sequences for special characters in names."
    ))

    if found:
        with open(path, "rb") as f:
            content = f.read()
        results.append(Result(
            "File contains exactly \"42\", nothing else", "CORE", content == b"42",
            trunc(repr(content)), repr(b"42"), "(content check)",
            "The subject's own `ls -lRa` example shows a file size of exactly 2 bytes -- i.e. \"42\" with no trailing newline.",
            "Use `printf '42' > filename` (not `echo`, which appends a newline) when creating the file."
        ))
    return results


# ==========================================================================
#  ex06 : skip.sh
# ==========================================================================
def test_ex06(dirpath):
    results = []
    path = os.path.join(dirpath, "skip.sh")
    if not os.path.isfile(path):
        return missing_file_result("skip.sh exists", path)

    tmp = tempfile.mkdtemp()
    try:
        for name in ("tata", "titi", "toto", "tutu"):
            open(os.path.join(tmp, name), "w").close()

        real_ls = subprocess.run(["ls", "-l"], cwd=tmp, capture_output=True, text=True).stdout.split("\n")
        real_ls = [l for l in real_ls if l]
        expected = "\n".join(real_ls[0::2])  # every second line, starting from the first (1-indexed odd lines)

        r = run_sh(path, cwd=tmp, timeout=5)
        out = (r.stdout or "").rstrip("\n") if r is not None else None

        results.append(Result(
            "Keeps every second line of `ls -l`, starting from the first", "CORE", out == expected,
            trunc(out) if out is not None else "(timeout)", trunc(expected), "4 files: tata, titi, toto, tutu",
            "Baseline: subject's own example keeps lines 1,3,5 of `ls -l` (the total line + every other file).",
            "`ls -l | awk 'NR % 2'` (odd record numbers) is the direct translation of 'every second line starting from the first'."
        ))

        got_lines = (out or "").count("\n") + (1 if out else 0)
        exp_lines = expected.count("\n") + 1
        results.append(Result(
            "Line count matches (ceil(N/2) of the original)", "TRAP", got_lines == exp_lines,
            f"{got_lines} lines", f"{exp_lines} lines", "(format check)",
            "A common off-by-one is keeping even lines instead of odd, which would still 'alternate' but starting from the wrong line.",
            "Double check you keep line 1 (the 'total' line) -- if it's missing, you're likely filtering even lines instead of odd."
        ))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ==========================================================================
#  ex07 : r_dwssap.sh
# ==========================================================================
def _passwd_reference(ft_line1, ft_line2):
    with open("/etc/passwd") as f:
        lines = [l.rstrip("\n") for l in f if l.strip()]
    lines = [l for l in lines if not l.startswith("#")]
    kept = lines[1::2]  # every other line, starting from the SECOND line
    logins = [l.split(":")[0] for l in kept]
    reversed_logins = [l[::-1] for l in logins]
    sorted_desc = sorted(reversed_logins, reverse=True)
    sliced = sorted_desc[ft_line1 - 1: ft_line2]
    return ", ".join(sliced) + ".", len(sorted_desc)


def test_ex07(dirpath):
    results = []
    path = os.path.join(dirpath, "r_dwssap.sh")
    if not os.path.isfile(path):
        return missing_file_result("r_dwssap.sh exists", path)

    if not os.path.isfile("/etc/passwd"):
        return [Result("/etc/passwd is readable", "CORE", False, "not found", "a readable /etc/passwd",
                        "(environment check)", "Needed to evaluate this exercise at all.",
                        "This is an environment issue, not your submission.")]

    _, total = _passwd_reference(1, 1)
    if total < 2:
        return [Result("/etc/passwd has enough entries to test with", "CORE", False,
                        f"only {total} usable login(s) after filtering", "at least 2",
                        "(environment check)", "Needed a non-trivial range to exercise the slicing logic.",
                        "This is an environment issue, not your submission.")]

    line1, line2 = 1, min(5, total)
    ref, _ = _passwd_reference(line1, line2)
    env = dict(os.environ)
    env["FT_LINE1"] = str(line1)
    env["FT_LINE2"] = str(line2)
    r = run_sh(path, env=env, timeout=5)
    out = (r.stdout or "").strip("\n") if r is not None else None

    results.append(Result(
        f"FT_LINE1={line1} FT_LINE2={line2}: exact match against the reference pipeline", "CORE", out == ref,
        trunc(out) if out is not None else "(timeout)", trunc(ref), f"live /etc/passwd, FT_LINE1={line1}, FT_LINE2={line2}",
        "Comprehensive check of the whole pipeline: strip comments, keep every other line from line 2, reverse each login, sort descending, slice by position, join with ', ', end with '.'.",
        "Build it up one stage at a time and check intermediate output -- the most common mistakes are keeping the wrong half of the 'every other line' split, or slicing before vs. after the sort."
    ))

    ends_with_dot = (out or "").endswith(".")
    results.append(Result(
        "Output ends with a period", "TRAP", ends_with_dot,
        trunc(out) if out is not None else "(timeout)", "output ending in \".\"", "(format check)",
        "Subject: 'End the output with a \".\"'.",
        "Append a literal '.' after the joined list, e.g. with `printf '.'` or `sed`."
    ))

    if total >= 8:
        line1b, line2b = 2, min(8, total)
        refb, _ = _passwd_reference(line1b, line2b)
        envb = dict(os.environ)
        envb["FT_LINE1"] = str(line1b)
        envb["FT_LINE2"] = str(line2b)
        rb = run_sh(path, env=envb, timeout=5)
        outb = (rb.stdout or "").strip("\n") if rb is not None else None
        results.append(Result(
            f"FT_LINE1={line1b} FT_LINE2={line2b}: different slice also matches", "TRAP", outb == refb,
            trunc(outb) if outb is not None else "(timeout)", trunc(refb), f"live /etc/passwd, FT_LINE1={line1b}, FT_LINE2={line2b}",
            "A second, different line range rules out a solution that happens to work only for one hardcoded range.",
            "Make sure FT_LINE1/FT_LINE2 are actually read from the environment and used in a `sed -n \"${FT_LINE1},${FT_LINE2}p\"`-style range, not hardcoded."
        ))
    return results


# ==========================================================================
#  ex08 : add_chelou.sh
# ==========================================================================
# The subject's FT_NBR1/FT_NBR2 examples are shown with heavy backslash
# escaping that's genuinely ambiguous to reverse-engineer character-for-
# character from the PDF. Rather than guess, this test derives its own
# operands directly from the three custom-base alphabets the subject
# defines, and confirms (independently, via a plain Python implementation
# of the same positional-numeral-system logic) that they decode to the
# subject's own worked answer, "Salut" -- which is strong evidence the
# alphabet/ordering interpretation below is the intended one.
_ALPHA_NBR1 = "'\"?!"          # base 4: ' " ? !
_ALPHA_NBR2 = "mrdoc"          # base 5: m r d o c
_ALPHA_OUT = "gtaioluSnemf"    # base 12: g t a i o l u S n e m f


def _decode_base(s, alphabet):
    base = len(alphabet)
    v = 0
    for ch in s:
        v = v * base + alphabet.index(ch)
    return v


def _encode_base(v, alphabet):
    base = len(alphabet)
    if v == 0:
        return alphabet[0]
    digits = []
    while v > 0:
        digits.append(alphabet[v % base])
        v //= base
    return "".join(reversed(digits))


def test_ex08(dirpath):
    results = []
    path = os.path.join(dirpath, "add_chelou.sh")
    if not os.path.isfile(path):
        return missing_file_result("add_chelou.sh exists", path)

    # Self-derived FT_NBR1 (reverse-engineered so that, together with the
    # subject's own FT_NBR2="rcrdmddd", the sum encodes to "Salut" -- see
    # module docstring. Passed straight through the env dict, so there is
    # no shell-quoting step for these special characters to survive.
    ft_nbr1 = "\"''!!'!"   # 7 chars: " ' ' ! ! ' !
    ft_nbr2 = "rcrdmddd"
    v1 = _decode_base(ft_nbr1, _ALPHA_NBR1)
    v2 = _decode_base(ft_nbr2, _ALPHA_NBR2)
    expected = _encode_base(v1 + v2, _ALPHA_OUT)

    self_check = (expected == "Salut")
    results.append(Result(
        "(self-check) reconstructed operands decode to the subject's own \"Salut\" answer", "TRAP", self_check,
        expected, "Salut", f"FT_NBR1={ft_nbr1!r} (derived) FT_NBR2={ft_nbr2!r} (from subject)",
        "Sanity check on the tester's own reverse-engineered alphabet ordering, not on your script -- if this fails, the CORE test below is built on a bad assumption and its result should be discounted.",
        "N/A -- this doesn't test your submission."
    ))

    env = dict(os.environ)
    env["FT_NBR1"] = ft_nbr1
    env["FT_NBR2"] = ft_nbr2
    r = run_sh(path, env=env, timeout=5)
    out = (r.stdout or "").strip("\n") if r is not None else None

    results.append(Result(
        "Computes the sum correctly across the three custom bases", "CORE", out == expected,
        trunc(out) if out is not None else "(timeout)", trunc(expected),
        f"FT_NBR1 in \"'?! base, FT_NBR2 in mrdoc base -> gtaio luSnemf base",
        "Baseline correctness, using operands independently verified (see the TRAP test above) to reproduce the subject's own worked example.",
        "Classic approach: `tr` each input's custom digits to 0-9/a-z, feed through `bc` with the right `ibase`, then `tr`/format the result through the output alphabet -- getting the digit *order* right in each alphabet is the easiest place to slip."
    ))

    # Informational only: not confident enough in the exact escaping of the
    # subject's second (overflow / "Segmentation fault") example to assert
    # a specific expected string, but a well-behaved script shouldn't hang
    # forever on a long input -- so just check it terminates.
    long_nbr2 = "dcrcmcmooododmrrrmorcmcrmomo"
    env2 = dict(os.environ)
    env2["FT_NBR1"] = ft_nbr1
    env2["FT_NBR2"] = long_nbr2
    r2 = run_sh(path, env=env2, timeout=5)
    terminates = r2 is not None
    results.append(Result(
        "(informational) Doesn't hang on a very large FT_NBR2", "TRAP", terminates,
        "timed out (>5s)" if not terminates else f"terminated (exit {r2.returncode})",
        "terminates one way or another", f"FT_NBR2={long_nbr2!r} (28 digits -- overflow territory)",
        "The subject's own second example for this input produces 'Segmentation fault' -- this test only checks your script doesn't hang; it deliberately does not assert that exact crash text, since the tester can't be fully certain it reproduced the PDF's escaping for that example byte-for-byte.",
        "If your script hangs here, check for unbounded recursion or a loop that doesn't terminate on very long inputs."
    ))
    return results


# ==========================================================================
#  RUNNER
# ==========================================================================

EXERCISES = {
    "ex01": test_ex01,
    "ex02": test_ex02,
    "ex03": test_ex03,
    "ex04": test_ex04,
    "ex05": test_ex05,
    "ex06": test_ex06,
    "ex07": test_ex07,
    "ex08": test_ex08,
}


def print_pass(msg):
    print(f"{C_GREEN}[PASS]{C_RESET} {msg}")


def print_fail(msg):
    print(f"{C_RED}[FAIL]{C_RESET} {msg}")


def tag(cat):
    if cat == "TRAP":
        return f"{C_MAGENTA}[TRAP]{C_RESET}"
    return f"{C_DIM}[CORE]{C_RESET}"


def calculate_rank(score):
    if score == 100:
        return "S"
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 50:
        return "C"
    return "F"


def run_exercise(ex_id, test_fn):
    print(f"\n{C_CYAN}{C_BOLD}============ Evaluating {ex_id} ============{C_RESET}")

    if not os.path.isdir(ex_id):
        print_fail(f"Turn-in directory '{ex_id}' missing.")
        return 0, (0, 0)

    try:
        results = test_fn(ex_id)
    except Exception as e:
        print_fail(f"Tester crashed while evaluating {ex_id}: {type(e).__name__}: {e}")
        return 0, (0, 0)

    core_pass = core_total = 0
    trap_pass = trap_total = 0

    for r in results:
        if r.cat == "CORE":
            core_total += 1
        else:
            trap_total += 1

        if r.passed:
            print_pass(f"{tag(r.cat)} {r.name}")
            if r.cat == "CORE":
                core_pass += 1
            else:
                trap_pass += 1
            if VERBOSE:
                print(f"      {C_DIM}Inputs   : {r.inputs}{C_RESET}")
                print(f"      {C_DIM}Why      : {r.why}{C_RESET}")
        else:
            print_fail(f"{tag(r.cat)} {r.name}")
            print(f"  ├── Inputs   : {r.inputs}")
            print(f"  ├── Got      : {C_RED}{r.got}{C_RESET}")
            print(f"  ├── Expected : {C_GREEN}{r.expected}{C_RESET}")
            print(f"  ├── Why      : {r.why}")
            print(f"  └── Hint     : {C_YELLOW}{r.hint}{C_RESET}")

    score = int((core_pass / core_total) * 100) if core_total > 0 else 0
    return score, (trap_pass, trap_total)


def main():
    print(f"{C_WHITE}{C_BOLD}=========================================================")
    print("       42 PISCINE SHELL01 - ADVERSARIAL / VERBOSE TESTER  ")
    print("=========================================================")
    print(f"{C_RESET}{C_DIM}CORE  = tests a rule stated in the subject; counts toward score/rank.")
    print(f"TRAP  = adversarial edge case; informational only, never affects score.")
    print(f"ex00 (Exam registration) has no deliverable file and isn't tested here.{C_RESET}")

    if shutil.which("/bin/sh") is None:
        print_fail("/bin/sh not found -- shell exercises can't be evaluated on this machine.")
        return

    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    sorted_exercises = sorted(EXERCISES.keys())
    if args:
        sorted_exercises = [a for a in sorted_exercises if a in args]
        if not sorted_exercises:
            print_fail(f"No matching exercises for: {args}")
            return

    results = []
    for ex in sorted_exercises:
        score, (tpass, ttotal) = run_exercise(ex, EXERCISES[ex])
        rank = calculate_rank(score)
        results.append((ex, score, rank, tpass, ttotal))

    print(f"\n{C_WHITE}{C_BOLD}+-------------------------------------------------------+")
    print("|                   FINAL SCOREBOARD                     |")
    print(f"+-------------------------------------------------------+{C_RESET}")
    print(f"| {'Exercise':<10} | {'CORE score':<12} | {'Rank':<6} | {'Trap insights':<14}|")
    print("+------------+--------------+--------+----------------+")

    for ex, score, rank, tpass, ttotal in results:
        c_status = C_GREEN if rank in ["S", "A"] else (C_YELLOW if rank in ["B", "C"] else C_RED)
        trap_str = f"{tpass}/{ttotal}" if ttotal else "n/a"
        trap_color = C_GREEN if (ttotal == 0 or tpass == ttotal) else C_MAGENTA
        print(f"| {ex:<10} | {score:>3}/100      | {c_status}{rank:<6}{C_RESET} | {trap_color}{trap_str:<14}{C_RESET} |")

    print("+------------+--------------+--------+----------------+")
    print(f"{C_DIM}Rank is computed from CORE tests only (the rules the subject actually states).")
    print(f"Trap insights are adversarial bonus checks; a low trap score is a learning signal,")
    print(f"not a grading penalty -- read the [TRAP] failure messages above for what to fix.{C_RESET}")


if __name__ == "__main__":
    main()
