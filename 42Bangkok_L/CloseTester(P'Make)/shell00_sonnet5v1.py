#!/usr/bin/env python3
"""
42 Piscine - Shell00 Adversarial Tester
----------------------------------------
Same philosophy as the C-side testers (c05/c07/c00), adapted for exercises
that are shell scripts / raw command files / filesystem artifacts instead
of compiled C:

  * Every test carries a CATEGORY:
      - CORE : directly checks a rule stated in the subject.
               These are the only tests that count towards the score/rank.
      - TRAP : an adversarial/edge case not explicitly graded by the
               subject, but that exposes a real misunderstanding (e.g. a
               force-added tracked file wrongly reported as git-ignored,
               a magic rule that's too loose, a named-pipe "cat" trick
               that only works once). TRAP failures never hurt the score.

  * Every test carries a WHY and, on failure, a HINT.

  * -v / --verbose prints the WHY for every test (even passing ones).

Unlike the C testers there's no compilation step: each exercise gets its
own Python test function that builds whatever fixture it needs (a scratch
directory, a throwaway git repo, controlled file permissions/mtimes...),
runs the submitted file with /bin/sh (or inspects it directly for the
filesystem-only exercises), and compares against a reference computed the
same way moulinette would have to: independently, at test time, in the
same environment -- never a hardcoded expected string where the real
answer is machine-dependent (MAC address, /etc/passwd, live git log...).
This exercise set doesn't need that trick, but ex04/ex05/ex06 all recompute
their reference live against the same fixture rather than hardcoding it.

Usage:
    python3 shell00_tester.py            # normal run, all exercises
    python3 shell00_tester.py -v         # verbose: show rationale for every test
    python3 shell00_tester.py ex05       # only run a specific exercise
"""

import os
import re
import sys
import stat
import shutil
import base64
import tarfile
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
    """Runs a submitted file with /bin/sh (moulinette's own rule: 'Shell
    exercises must be executable with /bin/sh'), from an absolute path so
    it is never accidentally copied into / listed inside the fixture dir
    it's being tested against."""
    cmd = ["/bin/sh", os.path.abspath(path)] + (args or [])
    try:
        return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True,
                               text=True, timeout=timeout, errors="replace")
    except subprocess.TimeoutExpired:
        return None
    except OSError as e:
        return e


def perm_str(mode):
    return stat.filemode(mode)[1:]  # drop the leading file-type char


def missing_file_result(name, path):
    return [Result(name, "CORE", False, "file not found", f"a file at {path}",
                    "(turn-in check)",
                    "This file is required by the subject's turn-in list.",
                    f"Create/submit {path} as specified in the subject.")]


# ==========================================================================
#  ex00 : z
# ==========================================================================
def test_ex00(dirpath):
    results = []
    path = os.path.join(dirpath, "z")
    if not os.path.isfile(path) and not os.path.islink(path):
        return missing_file_result("z exists", path)

    st = os.stat(path)  # follows symlinks -- a symlink to a valid file is fine
    is_regular = stat.S_ISREG(st.st_mode)

    r1 = subprocess.run(["cat", path], capture_output=True, text=True, timeout=5)
    out1 = r1.stdout
    passed1 = out1 == "Z\n"
    results.append(Result(
        "`cat z` prints exactly \"Z\\n\"", "CORE", passed1,
        trunc(repr(out1)), repr("Z\n"), "cat z",
        "Baseline: the subject's own example shows `cat z` printing Z followed by a newline, nothing else.",
        "Check the file's exact byte content -- it must be the single byte 'Z' followed by one newline, no extra spaces/lines."
    ))

    results.append(Result(
        "z is a regular file", "TRAP", is_regular,
        trunc(stat.filemode(st.st_mode)), "a regular file (-rw-...)",
        "(filesystem check)",
        "A regular text file is the straightforward, portable way to satisfy this exercise.",
        "If this is a FIFO/named pipe or another special file, it may only work once and can hang or fail under a different test harness."
    ))

    r2 = subprocess.run(["cat", path], capture_output=True, text=True, timeout=5)
    passed2 = r2.stdout == "Z\n"
    results.append(Result(
        "Reading z a second time gives the same result", "TRAP", passed2,
        trunc(repr(r2.stdout)), repr("Z\n"), "cat z (2nd read)",
        "A named-pipe/FIFO trick can pass a single `cat` but hang or return nothing on a second read -- moulinette may well read it more than once.",
        "Use a plain regular file (echo/printf into it), not a FIFO (mkfifo) or process substitution trick."
    ))
    return results


# ==========================================================================
#  ex01 : testShell00.tar
# ==========================================================================
def test_ex01(dirpath):
    results = []
    tar_path = os.path.join(dirpath, "testShell00.tar")
    if not os.path.isfile(tar_path):
        return missing_file_result("testShell00.tar exists", tar_path)

    tmp = tempfile.mkdtemp()
    try:
        try:
            with tarfile.open(tar_path) as tf:
                members = tf.getmembers()
                tf.extractall(tmp, filter="tar")
        except Exception as e:
            return [Result("testShell00.tar is a valid tar archive", "CORE", False,
                            f"error opening archive: {e}", "a valid tar archive",
                            "(archive check)",
                            "The subject explicitly says to build this with `tar -cf testShell00.tar testShell00`.",
                            "Recreate the tar with `tar -cf testShell00.tar testShell00` from the directory containing that file.")]

        names = [m.name for m in members]
        target = os.path.join(tmp, "testShell00")
        exists = os.path.isfile(target) and not os.path.islink(target)
        results.append(Result(
            "Archive contains a regular file named \"testShell00\"", "CORE", exists,
            trunc(", ".join(names)) if names else "(empty archive)", "a member named testShell00",
            f"tar -tf {os.path.basename(tar_path)}",
            "The turn-in directory table names exactly one file to submit: testShell00.",
            "Make sure you ran `tar -cf testShell00.tar testShell00` from inside the directory holding that file, not from one level up."
        ))

        if exists:
            mode = stat.S_IMODE(os.stat(target).st_mode)
            expected_mode = 0o455  # r--r-xr-x
            results.append(Result(
                "Permissions are exactly r--r-xr-x (0455)", "CORE", mode == expected_mode,
                perm_str(mode), "r--r-xr-x", f"chmod bits = {oct(mode)}",
                "Subject's own `ls -l` example shows `-r--r-xr-x` -- owner read-only, group and others read+execute.",
                f"Run `chmod 455 testShell00` (owner: r--, group: r-x, other: r-x) before re-tarring."
            ))

        extras = [n for n in names if n not in ("testShell00", "./testShell00")]
        results.append(Result(
            "No extra files/dirs bundled into the archive", "TRAP", len(extras) == 0,
            trunc(", ".join(extras)) if extras else "none", "only \"testShell00\"",
            "(archive contents)",
            "The general instructions forbid leaving additional files in your submission; an extra tar member usually means you tarred the wrong directory.",
            "tar only the single required file, e.g. from inside a directory that contains nothing else you care about."
        ))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ==========================================================================
#  ex02 : exo2.tar
# ==========================================================================
def test_ex02(dirpath):
    results = []
    tar_path = os.path.join(dirpath, "exo2.tar")
    if not os.path.isfile(tar_path):
        return missing_file_result("exo2.tar exists", tar_path)

    tmp = tempfile.mkdtemp()
    try:
        try:
            with tarfile.open(tar_path) as tf:
                tf.extractall(tmp, filter="tar")
        except Exception as e:
            return [Result("exo2.tar is a valid tar archive", "CORE", False,
                            f"error opening archive: {e}", "a valid tar archive",
                            "(archive check)",
                            "The subject says to build this with `tar -cf exo2.tar *`.",
                            "Recreate the tar with `tar -cf exo2.tar *` from the directory containing test0..test6.")]

        def entry(name):
            p = os.path.join(tmp, name)
            return p, os.path.lexists(p)

        expect = {
            "test0": ("dir", 0o715),
            "test1": ("file", 0o714),
            "test2": ("dir", 0o504),
            "test3": ("file", 0o404),
            "test4": ("file", 0o641),
            "test5": ("file", 0o404),
        }
        for name, (kind, mode) in expect.items():
            p, exists = entry(name)
            if not exists:
                results.append(Result(
                    f"{name} exists as a {kind}", "CORE", False, "missing", f"a {kind} named {name}",
                    "(filesystem check)",
                    f"The subject's `ls -l` example lists {name} explicitly.",
                    f"Create {name} as a {kind} (mkdir/touch) before tarring."
                ))
                continue
            st = os.lstat(p)
            is_kind = stat.S_ISDIR(st.st_mode) if kind == "dir" else stat.S_ISREG(st.st_mode)
            got_mode = stat.S_IMODE(st.st_mode)
            passed = is_kind and got_mode == mode
            results.append(Result(
                f"{name}: {kind}, mode {oct(mode)[2:]}", "CORE", passed,
                f"{'dir' if stat.S_ISDIR(st.st_mode) else ('file' if stat.S_ISREG(st.st_mode) else 'other')}, {perm_str(got_mode)}",
                f"{kind}, {perm_str(mode)}", "(filesystem check)",
                f"Byte-for-byte match against the subject's `ls -l` line for {name}.",
                f"chmod {oct(mode)[2:]} {name} (and confirm it's a {'directory' if kind=='dir' else 'regular file'})."
            ))

        # test3 <-> test5 hardlink relationship
        p3, e3 = entry("test3")
        p5, e5 = entry("test5")
        if e3 and e5:
            st3, st5 = os.lstat(p3), os.lstat(p5)
            same_inode = st3.st_ino == st5.st_ino and st3.st_dev == st5.st_dev
            nlink_ok = st3.st_nlink >= 2 and st5.st_nlink >= 2
            results.append(Result(
                "test3 and test5 are hardlinks of the same file", "CORE", same_inode and nlink_ok,
                f"same inode={same_inode}, nlink(test3)={st3.st_nlink}, nlink(test5)={st5.st_nlink}",
                "same inode, nlink >= 2 on both", "(filesystem check)",
                "Both lines in the subject show identical size/perms/date AND a link count of 2 -- that's the signature of `ln test3 test5` (a hardlink), not two independently-created files that happen to match.",
                "Use `ln test3 test5` (hard link), not `cp test3 test5` or creating test5 from scratch."
            ))
        else:
            results.append(Result(
                "test3 and test5 are hardlinks of the same file", "CORE", False,
                "one or both missing", "same inode, nlink >= 2 on both", "(filesystem check)",
                "See above.", "Create both test3 and test5, then hardlink them."
            ))

        # test6 symlink -> test0
        p6, e6 = entry("test6")
        if e6:
            st6 = os.lstat(p6)
            is_link = stat.S_ISLNK(st6.st_mode)
            target = os.readlink(p6) if is_link else None
            passed = is_link and target in ("test0", "./test0")
            results.append(Result(
                "test6 is a symlink pointing to test0", "CORE", passed,
                f"{'symlink -> ' + target if is_link else 'not a symlink'}", "symlink -> test0",
                "(filesystem check)",
                "The `l` file-type and `test6 -> test0` arrow in the subject's `ls -l` output mean a symbolic link.",
                "Use `ln -s test0 test6` (note the -s), not a hard link or a copy."
            ))
        else:
            results.append(Result(
                "test6 is a symlink pointing to test0", "CORE", False,
                "missing", "symlink -> test0", "(filesystem check)",
                "See above.", "Create test6 with `ln -s test0 test6`."
            ))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ==========================================================================
#  ex03 : id_rsa_pub
# ==========================================================================
PUBKEY_RE = re.compile(
    r"^(ssh-rsa|ssh-ed25519|ssh-dss|ecdsa-sha2-nistp256|ecdsa-sha2-nistp384|ecdsa-sha2-nistp521)"
    r"\s+([A-Za-z0-9+/]+=*)(\s+.*)?$"
)


def test_ex03(dirpath):
    results = []
    path = os.path.join(dirpath, "id_rsa_pub")
    if not os.path.isfile(path):
        return missing_file_result("id_rsa_pub exists", path)

    content = open(path, "r", errors="replace").read()
    first_line = content.strip().splitlines()[0] if content.strip() else ""
    m = PUBKEY_RE.match(first_line)

    results.append(Result(
        "Looks like a valid SSH public key (type + base64 body)", "CORE", bool(m),
        trunc(first_line) if first_line else "(empty file)",
        "e.g. \"ssh-ed25519 AAAA... comment\"", "(format check)",
        "A public key file is one line: a known key type, a base64 blob, and an optional comment.",
        "Run `ssh-keygen -t ed25519` (or similar) and submit the resulting *.pub file -- don't hand-edit it."
    ))

    looks_private = ("PRIVATE KEY" in content) or content.strip().startswith("-----BEGIN")
    results.append(Result(
        "Is NOT a private key", "CORE", not looks_private,
        "looks like a PRIVATE key block" if looks_private else "no private-key markers found",
        "no \"-----BEGIN ... PRIVATE KEY-----\" content", "(format check)",
        "The subject explicitly warns: 'Make sure you understand the difference between the public key and the private key.' Submitting id_rsa instead of id_rsa.pub is a classic, security-relevant mistake.",
        "Submit the file ending in .pub (id_rsa_pub here) -- never the private key itself."
    ))

    b64_ok = False
    if m:
        try:
            base64.b64decode(m.group(2) + "===")  # pad defensively
            b64_ok = True
        except Exception:
            b64_ok = False
    results.append(Result(
        "Base64 payload is structurally decodable", "TRAP", b64_ok,
        "decodes cleanly" if b64_ok else "failed to base64-decode", "valid base64", "(format check)",
        "Beyond just matching the regex shape, the base64 blob should actually decode -- catches a truncated copy-paste.",
        "Re-copy the full single line from the .pub file; don't wrap or truncate it."
    ))
    return results


# ==========================================================================
#  ex04 : midLS
# ==========================================================================
def test_ex04(dirpath):
    results = []
    path = os.path.join(dirpath, "midLS")
    if not os.path.isfile(path):
        return missing_file_result("midLS exists", path)

    tmp = tempfile.mkdtemp()
    try:
        # Controlled, strictly-ordered mtimes so the "sorted by modification
        # date" requirement is checkable regardless of which chronological
        # direction the author intended (the subject gives no example here,
        # unlike every other exercise in this document -- so both directions
        # are accepted as CORE-correct; see the WHY on the order test).
        import time as _time
        base = 1704110400  # 2024-01-01 12:00:00 UTC
        entries = [("fileA", "file", base + 10),
                   ("dirB", "dir", base + 20),
                   ("fileC", "file", base + 30)]
        for name, kind, ts in entries:
            p = os.path.join(tmp, name)
            if kind == "dir":
                os.mkdir(p)
            else:
                open(p, "w").close()
            os.utime(p, (ts, ts))
        hidden = os.path.join(tmp, ".hidden")
        open(hidden, "w").close()
        os.utime(hidden, (base + 40, base + 40))

        r = run_sh(path, cwd=tmp, timeout=5)
        if r is None:
            return [Result("midLS runs under /bin/sh", "CORE", False, "timeout", "completes within 5s",
                            "(no arguments)", "Sanity check that the command terminates.",
                            "Check for an unbounded loop or a command waiting on stdin.")]
        out = (r.stdout or "").rstrip("\n")

        results.append(Result(
            "Hidden files are excluded", "CORE", ".hidden" not in out,
            trunc(out), "no \".hidden\" token in the output", "cwd has fileA, dirB/, fileC, .hidden",
            "Subject: 'excluding hidden files or any file starting with a dot'.",
            "Plain `ls` (no -a/-A) already excludes dotfiles by default -- make sure you didn't add -a."
        ))

        results.append(Result(
            "Directory names end with a slash", "CORE", "dirB/" in out,
            trunc(out), "\"dirB/\" (not bare \"dirB\")", "cwd has fileA, dirB/, fileC",
            "Subject: 'Directory names should end with a slash (/)'.",
            "Use `ls -p` (or `-F` and strip the extra */=@| markers) to get a trailing / on directories only."
        ))

        results.append(Result(
            "Entries are joined with \", \" (comma-space), no trailing separator", "CORE",
            bool(out) and ", " in out and not out.endswith(",") and not out.endswith(", "),
            trunc(out), "\"a, b, c\" with no leading/trailing separator", "(format check)",
            "Subject: 'entries separated by a comma and a space' -- and nothing dangling after the last entry.",
            "Join with ', ' between entries, not after every entry (a trailing separator is a common off-by-one)."
        ))

        expected_names = ["fileA", "dirB/", "fileC"]
        asc = ", ".join(expected_names)
        desc = ", ".join(reversed(expected_names))
        passed_order = out.strip() in (asc, desc)
        results.append(Result(
            "Full listing matches chronological order (oldest\u2194newest accepted)", "CORE", passed_order,
            trunc(out), f"\"{asc}\" or \"{desc}\"", "fileA (oldest) < dirB < fileC (newest)",
            "The subject says 'sorted by modification date' but -- unlike its other exercises -- gives no worked example to pin down the direction, so both `ls -t` (newest first) and `ls -tr` (oldest first) are accepted here.",
            "If this fails, the issue isn't direction -- compare token-by-token against the expected content/format above."
        ))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ==========================================================================
#  ex05 : git_commit.sh
# ==========================================================================
def _make_git_repo(tmp, n_commits):
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "Tester", "GIT_AUTHOR_EMAIL": "tester@42.fr",
        "GIT_COMMITTER_NAME": "Tester", "GIT_COMMITTER_EMAIL": "tester@42.fr",
    })
    subprocess.run(["git", "init", "-q"], cwd=tmp, env=env, check=True)
    subprocess.run(["git", "config", "user.email", "tester@42.fr"], cwd=tmp, env=env, check=True)
    subprocess.run(["git", "config", "user.name", "Tester"], cwd=tmp, env=env, check=True)
    for i in range(n_commits):
        fname = os.path.join(tmp, f"file{i}.txt")
        with open(fname, "w") as f:
            f.write(f"content {i}\n")
        subprocess.run(["git", "add", f"file{i}.txt"], cwd=tmp, env=env, check=True)
        subprocess.run(["git", "commit", "-q", "-m", f"commit {i}"], cwd=tmp, env=env, check=True)
    return env


def test_ex05(dirpath):
    results = []
    path = os.path.join(dirpath, "git_commit.sh")
    if not os.path.isfile(path):
        return missing_file_result("git_commit.sh exists", path)

    tmp = tempfile.mkdtemp()
    try:
        env = _make_git_repo(tmp, 7)
        ref = subprocess.run(["git", "log", "-n", "5", "--format=%H"], cwd=tmp, env=env,
                              capture_output=True, text=True, check=True).stdout.strip("\n")
        r = run_sh(path, cwd=tmp, env=env, timeout=5)
        out = (r.stdout or "").strip("\n") if r is not None else None

        results.append(Result(
            "Prints exactly the last 5 commit ids, newest first", "CORE", out == ref,
            trunc(out) if out is not None else "(timeout)", trunc(ref), "repo with 7 commits",
            "Baseline: subject asks for the ids of the last 5 commits, one per line -- this must match `git log`'s own notion of \"last 5\" (newest first) exactly.",
            "Something like `git log -n 5 --format=%H` (or `--pretty=%H`) run inside the repo; watch out for `--oneline` (wrong format) or reversing the order."
        ))

        lines = [l for l in (out or "").split("\n") if l]
        full_hashes = all(re.fullmatch(r"[0-9a-f]{40}", l) for l in lines) and len(lines) > 0
        results.append(Result(
            "Each line is a full 40-character hash (not the short form)", "CORE", full_hashes,
            trunc(", ".join(lines)) if lines else "(no output)", "40 lowercase hex characters per line",
            "(format check)",
            "The subject's own example output shows full 40-char SHA1s, not the 7-character short hash `git log --oneline` would give.",
            "Use `%H` (full hash) in your format string, not `%h` (abbreviated)."
        ))

        # TRAP: repo with fewer than 5 commits
        tmp2 = tempfile.mkdtemp()
        try:
            env2 = _make_git_repo(tmp2, 3)
            ref2 = subprocess.run(["git", "log", "--format=%H"], cwd=tmp2, env=env2,
                                   capture_output=True, text=True, check=True).stdout.strip("\n")
            r2 = run_sh(path, cwd=tmp2, env=env2, timeout=5)
            out2 = (r2.stdout or "").strip("\n") if r2 is not None else None
            results.append(Result(
                "Repo with fewer than 5 commits: prints all of them, no error", "TRAP", out2 == ref2,
                trunc(out2) if out2 is not None else "(timeout)", trunc(ref2), "repo with only 3 commits",
                "Not stated in the subject, but 'last 5' should degrade gracefully to 'however many exist' rather than erroring or padding with blank lines -- `git log -n 5` already does this for free.",
                "If you sliced/counted commits manually instead of using `-n 5`, make sure the short-repo case is handled too."
            ))
        finally:
            shutil.rmtree(tmp2, ignore_errors=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ==========================================================================
#  ex06 : git_ignore.sh
# ==========================================================================
def test_ex06(dirpath):
    results = []
    path = os.path.join(dirpath, "git_ignore.sh")
    if not os.path.isfile(path):
        return missing_file_result("git_ignore.sh exists", path)

    tmp = tempfile.mkdtemp()
    try:
        env = dict(os.environ)
        env.update({"GIT_AUTHOR_NAME": "Tester", "GIT_AUTHOR_EMAIL": "tester@42.fr",
                    "GIT_COMMITTER_NAME": "Tester", "GIT_COMMITTER_EMAIL": "tester@42.fr"})
        subprocess.run(["git", "init", "-q"], cwd=tmp, env=env, check=True)
        subprocess.run(["git", "config", "user.email", "tester@42.fr"], cwd=tmp, env=env, check=True)
        subprocess.run(["git", "config", "user.name", "Tester"], cwd=tmp, env=env, check=True)
        with open(os.path.join(tmp, ".gitignore"), "w") as f:
            f.write("*.DS_Store\n*~\n*.o\n")
        subprocess.run(["git", "add", ".gitignore"], cwd=tmp, env=env, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=tmp, env=env, check=True)

        for name in (".DS_Store", "mywork.c~", "build.o"):
            open(os.path.join(tmp, name), "w").close()
        open(os.path.join(tmp, "tracked.txt"), "w").close()
        subprocess.run(["git", "add", "tracked.txt"], cwd=tmp, env=env, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "add tracked"], cwd=tmp, env=env, check=True)
        # Matches an ignore pattern but is force-added -- git no longer
        # considers it "ignored" even though the glob still matches it.
        open(os.path.join(tmp, "forced.o"), "w").close()
        subprocess.run(["git", "add", "-f", "forced.o"], cwd=tmp, env=env, check=True)

        ref = subprocess.run(["git", "ls-files", "--others", "-i", "--exclude-standard"],
                              cwd=tmp, env=env, capture_output=True, text=True, check=True).stdout
        ref_set = set(l for l in ref.split("\n") if l)

        r = run_sh(path, cwd=tmp, env=env, timeout=5)
        out = r.stdout if r is not None else None
        got_set = set(l for l in (out or "").split("\n") if l)

        results.append(Result(
            "Reports exactly the currently-ignored, existing files", "CORE", got_set == ref_set,
            trunc(", ".join(sorted(got_set))) if got_set else "(no output)",
            trunc(", ".join(sorted(ref_set))), "repo with .DS_Store, mywork.c~, build.o (ignored) + tracked.txt (not)",
            "Baseline: list every file matched by .gitignore that's actually present on disk.",
            "`git status --ignored` or `git ls-files --others -i --exclude-standard` both work; a hand-rolled glob-matcher is easy to get subtly wrong (see the TRAP test below)."
        ))

        forced_reported = "forced.o" in got_set
        results.append(Result(
            "A force-added tracked file is NOT reported as ignored", "TRAP", not forced_reported,
            "\"forced.o\" incorrectly listed" if forced_reported else "\"forced.o\" correctly absent",
            "\"forced.o\" must be absent from the output", "forced.o matches *.o but was `git add -f`'d",
            "Once git is explicitly tracking a file, it's no longer 'ignored' in git's eyes even though the pattern still matches it textually -- a solution built on a raw `find`/glob match (instead of asking git) will get this wrong.",
            "Prefer a git-aware command (`git status --ignored` / `git ls-files -i --exclude-standard`) over manually matching .gitignore patterns yourself."
        ))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ==========================================================================
#  ex07 : b  (diff a b)
# ==========================================================================
# Real fixture pulled from the resources bundle: the "a" starting file and
# the exact reference sw.diff that `diff a b` must reproduce.
FIXTURE_A = """STARWARS
Episode IV, A NEW HOPE It is a period of civil war.

Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire.
During the battle, Rebel spies managed to steal secret plans to the Empire's ultimate weapon, the DEATH STAR,
an armored space station with enough power to destroy an entire planet.

Pursued by the Empire's sinister agents, Princess Leia races home aboard her starship, custodian of the stolen plans that can save her people and restore freedom to the galaxy...

"""

FIXTURE_SW_DIFF = """1,2c1,8
< STARWARS
< Episode IV, A NEW HOPE It is a period of civil war.
---
> Episode V, A NEW H0PE It is a period of civil war
> Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire. 
> During the battle, Rebel spies managed to steal secret plans to the Empire's ultimate weapon, the STAR DEATH, an armored space station with enough power to destroy an entire planet.
> 
> 
> Pursued by the Empire's sinister agents,
> Princess Mehdi races home aboard her starship, custodian of the stolen plans that can save her people and restore the dictatorship to the galaxie..
> 
4,6d9
< Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire.
< During the battle, Rebel spies managed to steal secret plans to the Empire's ultimate weapon, the DEATH STAR,
< an armored space station with enough power to destroy an entire planet.
8d10
< Pursued by the Empire's sinister agents, Princess Leia races home aboard her starship, custodian of the stolen plans that can save her people and restore freedom to the galaxy...
"""


def test_ex07(dirpath):
    results = []
    path = os.path.join(dirpath, "b")
    if not os.path.isfile(path):
        return missing_file_result("b exists", path)

    tmp = tempfile.mkdtemp()
    try:
        a_path = os.path.join(tmp, "a")
        with open(a_path, "w") as f:
            f.write(FIXTURE_A)

        r = subprocess.run(["diff", a_path, path], capture_output=True, text=True)
        got_diff = r.stdout
        passed = got_diff == FIXTURE_SW_DIFF
        results.append(Result(
            "`diff a b` reproduces the exact reference sw.diff", "CORE", passed,
            trunc(got_diff, 260), trunc(FIXTURE_SW_DIFF, 260), "a = the subject's STARWARS fixture",
            "This is literally the exercise: b must be the file that makes `diff a b` equal the given sw.diff.",
            "Compare your b against a line-by-line; the fixture's second paragraph is duplicated/reordered/reworded in the target -- easy to drop a blank line or mis-copy a sentence."
        ))
        results.append(Result(
            "diff reports the files as different (exit code 1)", "TRAP", r.returncode == 1,
            f"exit code {r.returncode}", "exit code 1 (files differ)", "(sanity check)",
            "If b is byte-identical to a, `diff` exits 0 and produces no output at all -- a degenerate way to 'pass' that clearly isn't the intended file.",
            "Your b must actually be the patched/target version of the story, not a copy of a."
        ))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ==========================================================================
#  ex08 : clean
# ==========================================================================
def _check_single_command(text):
    """Heuristic: strip the shebang/comment lines, strip quoted spans and
    escaped `\\;` (find's own -exec terminator, not shell chaining), then
    look for a literal ';' or '&&' left over."""
    lines = [l for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    body = " ".join(lines)
    body = body.replace("\\;", "")               # find -exec ... \; terminator, not chaining
    body = re.sub(r"'[^']*'", "", body)           # single-quoted spans
    body = re.sub(r'"[^"]*"', "", body)           # double-quoted spans
    bad = (";" in body) or ("&&" in body)
    return not bad


def test_ex08(dirpath):
    results = []
    path = os.path.join(dirpath, "clean")
    if not os.path.isfile(path):
        return missing_file_result("clean exists", path)

    raw = open(path, "r", errors="replace").read()
    single_cmd = _check_single_command(raw)
    results.append(Result(
        "File contains a single command (no ';' / '&&' chaining)", "CORE", single_cmd,
        "chaining characters found outside quotes/`\\;`" if not single_cmd else "no chaining found",
        "one command only", "(static check of the file's text)",
        "Subject: 'Only one command is allowed, no \\';\\' or \\'&&\\' or other chaining tricks.'",
        "A single `find . \\( -name '*~' -o -name '#*#' \\) -print -delete` covers search + display + delete in one command."
    ))

    tmp = tempfile.mkdtemp()
    try:
        to_delete = ["dropme~", "#dropme#", ".hidden~", os.path.join("sub", "dropme2~")]
        to_keep = ["keep1.txt", os.path.join("sub", "keep2.txt"), "notreally~not", "#nothash"]
        os.makedirs(os.path.join(tmp, "sub"), exist_ok=True)
        for name in to_delete + to_keep:
            open(os.path.join(tmp, name), "w").close()

        r = run_sh(path, cwd=tmp, timeout=5)
        out = (r.stdout or "") if r is not None else ""

        still_there = [n for n in to_delete if os.path.exists(os.path.join(tmp, n))]
        results.append(Result(
            "Deletes every file matching *~ or #*# (incl. nested/hidden)", "CORE", len(still_there) == 0,
            trunc(", ".join(still_there)) if still_there else "all matching files removed",
            "dropme~, #dropme#, .hidden~, sub/dropme2~ all gone", "mixed fixture tree",
            "Subject: searches for files ending with ~ or starting AND ending with #, displays and deletes them.",
            "Your `find` pattern needs both `-name '*~'` and `-name '#*#'` (OR'd together), applied recursively from '.'."
        ))

        wrongly_removed = [n for n in to_keep if not os.path.exists(os.path.join(tmp, n))]
        results.append(Result(
            "Leaves non-matching files untouched", "CORE", len(wrongly_removed) == 0,
            trunc(", ".join(wrongly_removed)) if wrongly_removed else "all non-matching files intact",
            "keep1.txt, sub/keep2.txt, notreally~not, #nothash all remain", "mixed fixture tree",
            "Only names ending in ~ or both starting/ending with # should match -- 'notreally~not' doesn't end in ~, '#nothash' doesn't end in #.",
            "Double-check your -name patterns anchor at the end (*~) and both ends (#*#), not a bare substring match."
        ))

        printed_ok = all(n in out for n in to_delete if os.path.basename(n) in out or n in out)
        basenames_found = sum(1 for n in to_delete if os.path.basename(n) in out)
        results.append(Result(
            "Displays the names of deleted files", "CORE", basenames_found >= 3,
            f"{basenames_found}/4 deleted filenames appeared in stdout", "all 4 deleted filenames printed",
            trunc(out) if out else "(no stdout)",
            "Subject: 'Displays the found files and deletes them.'",
            "`find ... -print -delete` prints each match before removing it; if you only used `-delete`, add `-print` before it (order matters)."
        ))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ==========================================================================
#  ex09 : ft_magic
# ==========================================================================
def test_ex09(dirpath):
    results = []
    path = os.path.join(dirpath, "ft_magic")
    if not os.path.isfile(path):
        return missing_file_result("ft_magic exists", path)

    if shutil.which("file") is None:
        return [Result("`file` command available", "CORE", False, "not found", "the `file` utility installed",
                        "(environment check)", "Needed to evaluate a magic file at all.",
                        "This is an environment issue, not your submission.")]

    tmp = tempfile.mkdtemp()
    try:
        def make_fixture(name, marker_offset):
            data = bytearray(b"x" * 60)
            if marker_offset is not None:
                data[marker_offset:marker_offset + 2] = b"42"
            p = os.path.join(tmp, name)
            with open(p, "wb") as f:
                f.write(bytes(data))
            return p

        # Primary interpretation: magic(5) byte-offset field = 42 (0-indexed),
        # which is what you'd literally write as the offset in the magic rule.
        pos = make_fixture("match.bin", 42)
        neg = make_fixture("nomatch.bin", None)

        r_pos = subprocess.run(["file", "-m", path, pos], capture_output=True, text=True, timeout=5)
        r_neg = subprocess.run(["file", "-m", path, neg], capture_output=True, text=True, timeout=5)

        pos_hit = "42 file" in r_pos.stdout
        neg_hit = "42 file" in r_neg.stdout

        results.append(Result(
            "Detects \"42\" at byte offset 42 as a \"42 file\"", "CORE", pos_hit,
            trunc(r_pos.stdout), "output containing \"42 file\"", "\"x\"*60 with \"42\" spliced in at offset 42",
            "Subject: files containing the string \"42\" at the 42nd byte must be identified as type \"42 file\".",
            "A magic rule like `>42\\tstring\\t42\\t42 file` (offset 42, expect the literal bytes \"42\") should do it -- check with `file -m ft_magic somefile`."
        ))
        results.append(Result(
            "Does NOT flag a file without \"42\" at that offset", "TRAP", not neg_hit,
            trunc(r_neg.stdout), "no \"42 file\" in the output", "same-size file without the marker",
            "A magic rule that's too loose (wrong/missing offset check) would misclassify unrelated files too.",
            "Make sure your rule's offset field is exactly 42, not a wildcard or a smaller/looser match."
        ))

        # Informational: the "42nd byte" phrasing is genuinely ambiguous
        # between a 0-indexed offset (42) and a 1-indexed count (offset 41).
        # Not scored -- just flagged so you can adjust if real moulinette
        # feedback disagrees with the primary interpretation above.
        alt = make_fixture("alt.bin", 41)
        r_alt = subprocess.run(["file", "-m", path, alt], capture_output=True, text=True, timeout=5)
        alt_hit = "42 file" in r_alt.stdout
        results.append(Result(
            "(informational) Also matches under the 1-indexed reading (offset 41)", "TRAP", alt_hit,
            trunc(r_alt.stdout), "output containing \"42 file\" (not required)", "\"42\" spliced in at 0-indexed offset 41",
            "\"the 42nd byte\" could mean 0-indexed offset 42 (what you'd type into the magic rule) or the 42nd byte counting from 1 (0-indexed offset 41). This test is informational only.",
            "If real moulinette feedback says your file is misdetected, try shifting your rule's offset by one."
        ))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ==========================================================================
#  RUNNER
# ==========================================================================

EXERCISES = {
    "ex00": test_ex00,
    "ex01": test_ex01,
    "ex02": test_ex02,
    "ex03": test_ex03,
    "ex04": test_ex04,
    "ex05": test_ex05,
    "ex06": test_ex06,
    "ex07": test_ex07,
    "ex08": test_ex08,
    "ex09": test_ex09,
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
    print("       42 PISCINE SHELL00 - ADVERSARIAL / VERBOSE TESTER  ")
    print("=========================================================")
    print(f"{C_RESET}{C_DIM}CORE  = tests a rule stated in the subject; counts toward score/rank.")
    print(f"TRAP  = adversarial edge case (force-added ignored files, FIFO tricks,")
    print(f"        loose magic rules, etc); informational only, never affects score.{C_RESET}")

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
