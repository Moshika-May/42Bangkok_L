#!/usr/bin/env python3
"""
42 Piscine - C09 Adversarial Tester
------------------------------------
Same design as the c05/c07 testers:

  * Every test carries a CATEGORY:
      - CORE : directly checks a rule stated in the subject. Moulinette-relevant.
               These are the only tests that count towards the score/rank.
      - TRAP : an adversarial/edge test that is NOT explicitly graded by the
               subject, but exposes classic implementation bugs. TRAP failures
               are reported as insights and never hurt the score.

  * Every test carries a WHY and, on failure, a HINT.

  * -v / --verbose prints the WHY for every test (even passing ones).

C09 is different from C05/C07: ex00 and ex01 are build-system exercises
(a shell script that builds a .a, and a hand-written Makefile), not pure
"call this C function and check the return value" exercises. So instead of
one big self-contained C harness per exercise, this tester drives real
shell/make/nm/ar invocations against isolated temp copies of your work,
plus a small compiled C harness for functional checks against the
resulting libft.a. ex02 (ft_split) reuses the same C-harness style as the
other testers.

Usage:
    python3 c09_tester.py            # normal run
    python3 c09_tester.py -v         # verbose: show rationale for every test
    python3 c09_tester.py ex01       # only run a specific exercise
"""

import os
import sys
import re
import time
import shutil
import tempfile
import subprocess

US = "\x1f"

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

CC = "cc"
CFLAGS = ["-Wall", "-Wextra", "-Werror"]

# ==========================================================================
#  SHARED REPORTING
# ==========================================================================

def tag(category):
    if category == "TRAP":
        return f"{C_MAGENTA}[TRAP]{C_RESET}"
    return f"{C_DIM}[CORE]{C_RESET}"

def print_pass(msg):
    print(f"{C_GREEN}[PASS]{C_RESET} {msg}")

def print_fail(msg):
    print(f"{C_RED}[FAIL]{C_RESET} {msg}")

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

class Tally:
    def __init__(self):
        self.core_pass = 0
        self.core_total = 0
        self.trap_pass = 0
        self.trap_total = 0

    def report(self, name, category, passed, got, expected, inputs, why, hint):
        if category == "CORE":
            self.core_total += 1
        else:
            self.trap_total += 1
        if passed:
            print_pass(f"{tag(category)} {name}")
            if category == "CORE":
                self.core_pass += 1
            else:
                self.trap_pass += 1
            if VERBOSE:
                print(f"      {C_DIM}Inputs   : {inputs}{C_RESET}")
                print(f"      {C_DIM}Why      : {why}{C_RESET}")
        else:
            print_fail(f"{tag(category)} {name}")
            print(f"  ├── Inputs   : {inputs}")
            print(f"  ├── Got      : {C_RED}{got}{C_RESET}")
            print(f"  ├── Expected : {C_GREEN}{expected}{C_RESET}")
            print(f"  ├── Why      : {why}")
            print(f"  └── Hint     : {C_YELLOW}{hint}{C_RESET}")

    def score(self):
        return int((self.core_pass / self.core_total) * 100) if self.core_total > 0 else 0


def run(cmd, cwd, timeout=15):
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                               timeout=timeout, errors="replace")
    except subprocess.TimeoutExpired:
        class Fake:
            returncode = -1
            stdout = ""
            stderr = f"TIMEOUT after {timeout}s"
        return Fake()

def find_file(root, filename):
    for dirpath, _dirnames, filenames in os.walk(root):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None


# ==========================================================================
#  EX00 : libft (libft_creator.sh + 5 source files -> libft.a)
# ==========================================================================

EX00_REQUIRED_FILES = ["libft_creator.sh", "ft_putchar.c", "ft_swap.c",
                        "ft_putstr.c", "ft_strlen.c", "ft_strcmp.c"]
EX00_SYMBOLS = ["ft_putchar", "ft_swap", "ft_putstr", "ft_strlen", "ft_strcmp"]

EX00_HARNESS = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

void ft_putchar(char c);
void ft_swap(int *a, int *b);
void ft_putstr(char *str);
int  ft_strlen(char *str);
int  ft_strcmp(char *s1, char *s2);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"ft_putchar writes exactly one char to stdout",  "CORE"},
    {"ft_swap swaps two ints via pointers",            "CORE"},
    {"ft_putstr writes the exact string, no extras",   "CORE"},
    {"ft_strlen matches libc strlen",                  "CORE"},
    {"ft_strcmp sign matches libc strcmp",              "CORE"},
    {"ft_swap(&x, &x) with a==b leaves the value unchanged", "TRAP"},
};

/* Redirect stdout to a temp file, run fn, restore, and return captured bytes. */
static ssize_t capture_stdout(void (*fn_putchar)(char), char c,
                               void (*fn_putstr)(char *), char *str,
                               char *buf, size_t bufsize)
{
    char tmpl[] = "/tmp/c09_capXXXXXX";
    int fd = mkstemp(tmpl);
    int saved = dup(1);
    fflush(stdout);
    dup2(fd, 1);
    if (fn_putchar)
        fn_putchar(c);
    if (fn_putstr)
        fn_putstr(str);
    fflush(stdout);
    dup2(saved, 1);
    close(saved);
    lseek(fd, 0, SEEK_SET);
    ssize_t n = read(fd, buf, bufsize - 1);
    if (n < 0) n = 0;
    buf[n] = '\0';
    close(fd);
    unlink(tmpl);
    return n;
}

int main(int argc, char **argv)
{
    if (argc < 2)
        return 1;
    if (strcmp(argv[1], "list") == 0) {
        for (size_t i = 0; i < sizeof(META) / sizeof(META[0]); i++)
            printf("%zu" US "%s" US "%s\n", i, META[i].cat, META[i].name);
        return 0;
    }
    int id = atoi(argv[1]);

    const char *why_arr[] = {
        "Subject: 'void ft_putchar(char c);'. Must output the character itself and nothing else -- no newline, no extra bytes.",
        "Subject: 'void ft_swap(int *a, int *b);'. Baseline correctness: the two pointed-to values must be exchanged.",
        "Subject: 'void ft_putstr(char *str);'. Must output the string's bytes exactly, with no added newline or truncation.",
        "Subject: 'int ft_strlen(char *str);'. Must return the same count as the standard strlen for arbitrary strings.",
        "Subject: 'int ft_strcmp(char *s1, char *s2);'. The SIGN of the result (negative/zero/positive) must match strcmp's, even if the exact magnitude differs.",
        "TRAP: a classic swap implemented via XOR (a ^= b; b ^= a; a ^= b;) silently zeroes the value when a and b are the SAME address -- a real bug class, not covered by the subject's basic two-variable example."
    };
    const char *hint_arr[] = {
        "Make sure you write() (or equivalent) exactly 1 byte -- the character itself, with no trailing '\\n'.",
        "Use a temporary variable to hold *a while assigning *a = *b and *b = tmp.",
        "Compute the length yourself (or rely on write of the whole buffer) and make sure you don't write a terminating '\\0' or an extra newline.",
        "Walk the string counting bytes until you hit '\\0', just like the standard strlen.",
        "Compare byte by byte and return a difference with the correct sign at the first mismatch (or 0 if the strings are identical).",
        "If you implement ft_swap with XOR tricks instead of a temp variable, calling ft_swap(&x, &x) zeroes x. Prefer a plain temporary-variable swap -- it's simpler AND safe under aliasing."
    };

    char got[128] = "matches expected";
    char expected[64] = "";
    char inputs[64] = "";
    int passed = 1;

    if (id == 0) {
        char buf[8];
        capture_stdout(ft_putchar, 'A', NULL, NULL, buf, sizeof(buf));
        strcpy(inputs, "ft_putchar('A')");
        strcpy(expected, "stdout == \"A\"");
        if (strcmp(buf, "A") != 0) { passed = 0; snprintf(got, sizeof(got), "stdout == \"%s\"", buf); }
    } else if (id == 1) {
        int a = 10, b = 20;
        ft_swap(&a, &b);
        strcpy(inputs, "a=10 b=20");
        strcpy(expected, "a=20 b=10");
        if (a != 20 || b != 10) { passed = 0; snprintf(got, sizeof(got), "a=%d b=%d", a, b); }
    } else if (id == 2) {
        char buf[64];
        char str[] = "Hello, 42!";
        capture_stdout(NULL, 0, ft_putstr, str, buf, sizeof(buf));
        snprintf(inputs, sizeof(inputs), "ft_putstr(\"%s\")", str);
        snprintf(expected, sizeof(expected), "stdout == \"%s\"", str);
        if (strcmp(buf, str) != 0) { passed = 0; snprintf(got, sizeof(got), "stdout == \"%s\"", buf); }
    } else if (id == 3) {
        char *tests[] = {"", "a", "Hello, 42!", "a long-ish test string here"};
        for (int i = 0; i < 4 && passed; i++) {
            int r = ft_strlen(tests[i]);
            int e = (int)strlen(tests[i]);
            if (r != e) {
                passed = 0;
                snprintf(inputs, sizeof(inputs), "str=\"%.20s\"", tests[i]);
                snprintf(expected, sizeof(expected), "%d", e);
                snprintf(got, sizeof(got), "%d", r);
            }
        }
        if (passed) { strcpy(inputs, "several strings, including empty"); strcpy(expected, "matches strlen()"); }
    } else if (id == 4) {
        struct { char *a; char *b; } tests[] = {
            {"abc", "abc"}, {"abc", "abd"}, {"abd", "abc"}, {"ab", "abc"}, {"", ""}
        };
        for (int i = 0; i < 5 && passed; i++) {
            int r = ft_strcmp(tests[i].a, tests[i].b);
            int e = strcmp(tests[i].a, tests[i].b);
            int rs = (r > 0) - (r < 0);
            int es = (e > 0) - (e < 0);
            if (rs != es) {
                passed = 0;
                snprintf(inputs, sizeof(inputs), "s1=\"%s\" s2=\"%s\"", tests[i].a, tests[i].b);
                snprintf(expected, sizeof(expected), "sign %d", es);
                snprintf(got, sizeof(got), "sign %d (raw %d)", rs, r);
            }
        }
        if (passed) { strcpy(inputs, "equal / less / greater / prefix / empty pairs"); strcpy(expected, "sign matches strcmp()"); }
    } else if (id == 5) {
        int x = 42;
        ft_swap(&x, &x);
        strcpy(inputs, "ft_swap(&x, &x), x=42 beforehand");
        strcpy(expected, "x == 42 (unchanged)");
        if (x != 42) { passed = 0; snprintf(got, sizeof(got), "x == %d", x); }
    } else {
        return 1;
    }

    printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, passed ? "PASS" : "FAIL", got, expected, inputs, why_arr[id], hint_arr[id]);
    return 0;
}
"""

FORBIDDEN_PATTERNS = [
    r"\bprintf\s*\(", r"\bmalloc\s*\(", r"\bfree\s*\(", r"\bmemcpy\s*\(",
    r"\bmemset\s*\(", r"\bstrlen\s*\(", r"\bstrcpy\s*\(", r"\bstrcmp\s*\(",
    r"\bstrcat\s*\(", r"\bputchar\s*\(", r"\bputs\s*\(", r"\bfputs\s*\(",
    r"\bsystem\s*\(",
]

def run_ex00(ex_dir, tally):
    print(f"\n{C_CYAN}{C_BOLD}============ Evaluating ex00 (libft_creator.sh) ============{C_RESET}")

    if not os.path.isdir(ex_dir):
        tally.report("Turn-in directory present", "CORE", False, "missing", "ex00/ present",
                      "ex00/", "The turn-in directory must exist.", "Create the ex00/ directory with the required files.")
        return

    missing = [f for f in EX00_REQUIRED_FILES if not os.path.isfile(os.path.join(ex_dir, f))]
    tally.report("All required files present", "CORE", not missing,
                  f"missing: {missing}" if missing else "all present",
                  "libft_creator.sh + 5 .c files", ", ".join(EX00_REQUIRED_FILES),
                  "Subject lists exactly these files to turn in.",
                  "Check filenames and extensions match exactly (case-sensitive).")
    if missing:
        return

    tmp_dir = tempfile.mkdtemp()
    try:
        for f in EX00_REQUIRED_FILES:
            shutil.copy(os.path.join(ex_dir, f), tmp_dir)

        script_res = run(["sh", "libft_creator.sh"], cwd=tmp_dir, timeout=20)
        libft_path = find_file(tmp_dir, "libft.a")
        ok = script_res.returncode == 0 and libft_path is not None
        tally.report("Running `sh libft_creator.sh` produces libft.a", "CORE", ok,
                      f"return={script_res.returncode}, libft.a {'found' if libft_path else 'NOT found'}"
                      + (f"\n         stderr: {script_res.stderr.strip()[:300]}" if script_res.returncode != 0 else ""),
                      "return=0, libft.a present", "sh libft_creator.sh",
                      "Subject: 'A shell script called libft_creator.sh will compile the source files appropriately and will create your library.'",
                      "Check the script actually runs cc on all 5 .c files and then `ar rc libft.a *.o` (+ ranlib), and that it doesn't rely on a working directory other than where it's invoked from.")
        if not ok:
            return

        ar_res = run(["ar", "t", libft_path], cwd=tmp_dir)
        nm_res = run(["nm", libft_path], cwd=tmp_dir)
        nm_out = nm_res.stdout
        symbol_missing = [s for s in EX00_SYMBOLS if not re.search(rf"\b[TtDdBb]\s+_?{re.escape(s)}\b", nm_out)]
        tally.report("libft.a contains all 5 required symbols", "CORE", not symbol_missing,
                      f"missing symbols: {symbol_missing}" if symbol_missing else "all 5 symbols defined",
                      f"nm {os.path.basename(libft_path)}", ", ".join(EX00_SYMBOLS),
                      "Subject: the library 'should contain all of the following functions'.",
                      "Make sure every .c file is actually compiled into a .o and archived -- a common bug is the script silently skipping a file (typo in a filename, or the wildcard used doesn't match one of them).")

        # Functional harness against the produced libft.a
        harness_path = os.path.join(tmp_dir, "harness.c")
        bin_path = os.path.join(tmp_dir, "test_runner")
        with open(harness_path, "w") as f:
            f.write(EX00_HARNESS)
        comp = run([CC] + CFLAGS + [harness_path, libft_path, "-o", bin_path], cwd=tmp_dir)
        if comp.returncode != 0:
            tally.report("Functions link and behave correctly", "CORE", False,
                          "compilation against libft.a failed", "clean compile",
                          "cc harness.c libft.a -o test_runner",
                          "The functional tests link a small harness directly against your libft.a.",
                          f"Compiler said:\n{comp.stderr.strip()[:500]}")
        else:
            list_res = run([bin_path, "list"], cwd=tmp_dir)
            tests = []
            for line in list_res.stdout.strip().split("\n"):
                if US in line:
                    t_id, t_cat, t_name = line.split(US, 2)
                    tests.append((t_id, t_cat, t_name))
            for t_id, t_cat, t_name in tests:
                res = run([bin_path, t_id], cwd=tmp_dir, timeout=5)
                if res.returncode != 0:
                    tally.report(t_name, t_cat, False, f"crashed (exit {res.returncode})",
                                 "clean run", f"test id {t_id}",
                                 "See META/why in the harness for this test.",
                                 "A crash here usually means a segfault or an aliasing bug (e.g. XOR-swap on a==b).")
                    continue
                out = res.stdout.strip()
                if not out.startswith("RESULT" + US):
                    tally.report(t_name, t_cat, False, "invalid harness output", "RESULT line",
                                 f"test id {t_id}", "-", "-")
                    continue
                parts = out.split(US)
                if len(parts) < 9:
                    tally.report(t_name, t_cat, False, "malformed harness output", "9 fields",
                                 f"test id {t_id}", "-", "-")
                    continue
                _, name, category, status, got, expected, inputs, why, hint = parts[:9]
                tally.report(name, category, status == "PASS", got, expected, inputs, why, hint)

        # TRAP: forbidden-function grep across the submitted sources.
        offenders = []
        for f in EX00_REQUIRED_FILES:
            if not f.endswith(".c"):
                continue
            content = open(os.path.join(tmp_dir, f)).read()
            for pat in FORBIDDEN_PATTERNS:
                if re.search(pat, content):
                    offenders.append(f"{f}: {pat.strip(chr(92)+'b(')}")
        tally.report("No obviously forbidden libc calls (only write() allowed)", "TRAP", not offenders,
                      "; ".join(offenders) if offenders else "no forbidden calls found",
                      "no forbidden calls", ", ".join(EX00_REQUIRED_FILES[1:]),
                      "TRAP: subject says 'Allowed functions: write'. This is a simple grep, not the real moulinette/norminette forbidden-function checker, but it catches the obvious cases (printf, malloc, strlen, etc. used instead of writing your own).",
                      "Replace the flagged call with your own loop/logic, or with write() directly. Using standard-library helpers here is exactly what 'Allowed functions' is meant to prevent.")

        # TRAP: idempotent re-run of the build script.
        script_res2 = run(["sh", "libft_creator.sh"], cwd=tmp_dir, timeout=20)
        libft_path2 = find_file(tmp_dir, "libft.a")
        ok2 = script_res2.returncode == 0 and libft_path2 is not None
        tally.report("Script can be re-run without failing (idempotent build)", "TRAP", ok2,
                      f"return={script_res2.returncode}, libft.a {'still present' if libft_path2 else 'missing'}",
                      "return=0, libft.a still present", "sh libft_creator.sh (run a second time)",
                      "TRAP: not explicitly required by the subject, but a script that only works once (e.g. `ar rc` failing on a stale .o, or crashing if libft.a already exists) is fragile and a common real-world gotcha.",
                      "Make sure repeated runs of the script don't error out -- e.g. avoid assuming libft.a doesn't already exist, or clean stale artifacts before rebuilding.")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# ==========================================================================
#  EX01 : Makefile (build system rules -- tested against OUR reference
#          srcs/ and includes/, mirroring "we'll only fetch your Makefile
#          and test it with our files")
# ==========================================================================

FT_H = r"""#ifndef FT_H
# define FT_H

void	ft_putchar(char c);
void	ft_swap(int *a, int *b);
void	ft_putstr(char *str);
int		ft_strlen(char *str);
int		ft_strcmp(char *s1, char *s2);

#endif
"""

REF_SRCS = {
    "ft_putchar.c": r"""#include <unistd.h>
#include "ft.h"

void	ft_putchar(char c)
{
	write(1, &c, 1);
}
""",
    "ft_swap.c": r"""#include "ft.h"

void	ft_swap(int *a, int *b)
{
	int	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}
""",
    "ft_putstr.c": r"""#include <unistd.h>
#include "ft.h"

void	ft_putstr(char *str)
{
	int	i;

	i = 0;
	while (str[i])
		i++;
	write(1, str, i);
}
""",
    "ft_strlen.c": r"""#include "ft.h"

int	ft_strlen(char *str)
{
	int	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}
""",
    "ft_strcmp.c": r"""#include "ft.h"

int	ft_strcmp(char *s1, char *s2)
{
	int	i;

	i = 0;
	while (s1[i] && s1[i] == s2[i])
		i++;
	return ((unsigned char)s1[i] - (unsigned char)s2[i]);
}
""",
}


def fresh_ex01_env(makefile_path):
    tmp_dir = tempfile.mkdtemp()
    shutil.copy(makefile_path, os.path.join(tmp_dir, "Makefile"))
    os.makedirs(os.path.join(tmp_dir, "srcs"), exist_ok=True)
    os.makedirs(os.path.join(tmp_dir, "includes"), exist_ok=True)
    for name, content in REF_SRCS.items():
        with open(os.path.join(tmp_dir, "srcs", name), "w") as f:
            f.write(content)
    with open(os.path.join(tmp_dir, "includes", "ft.h"), "w") as f:
        f.write(FT_H)
    return tmp_dir

def count_cc_lines(output):
    return len([l for l in output.split("\n") if l.strip().split(" ")[0].split("\t")[0] in ("cc", "$(CC)")])

def obj_mtimes(tmp_dir):
    d = {}
    srcs_dir = os.path.join(tmp_dir, "srcs")
    if os.path.isdir(srcs_dir):
        for f in os.listdir(srcs_dir):
            if f.endswith(".o"):
                d[f] = os.path.getmtime(os.path.join(srcs_dir, f))
    lib = os.path.join(tmp_dir, "libft.a")
    if os.path.isfile(lib):
        d["libft.a"] = os.path.getmtime(lib)
    return d

def run_ex01(ex_dir, tally):
    print(f"\n{C_CYAN}{C_BOLD}============ Evaluating ex01 (Makefile) ============{C_RESET}")

    makefile_path = os.path.join(ex_dir, "Makefile")
    if not os.path.isfile(makefile_path):
        tally.report("Makefile present", "CORE", False, "missing", "ex01/Makefile present",
                      "ex01/Makefile", "The turn-in directory must contain a Makefile.",
                      "Create ex01/Makefile.")
        return

    # --- Test 1: bare `make` builds libft.a -------------------------------
    tmp1 = fresh_ex01_env(makefile_path)
    res1 = run(["make"], cwd=tmp1)
    lib1 = os.path.isfile(os.path.join(tmp1, "libft.a"))
    tally.report("`make` (bare) builds libft.a", "CORE", res1.returncode == 0 and lib1,
                  f"return={res1.returncode}, libft.a {'present' if lib1 else 'missing'}"
                  + (f"\n         stderr: {res1.stderr.strip()[:300]}" if res1.returncode != 0 else ""),
                  "return=0, libft.a present at root",
                  "make (in a fresh checkout of your Makefile + our srcs/includes)",
                  "Subject: 'Running just make should be equivalent to make all.'",
                  "Your default (first) rule must build libft.a -- usually by making 'all' the first rule and having 'all' depend on libft.a.")
    shutil.rmtree(tmp1, ignore_errors=True)

    # --- Test 2: make / make all / make libft.a are equivalent ------------
    variants = [[], ["all"], ["libft.a"]]
    fails = []
    for args in variants:
        t = fresh_ex01_env(makefile_path)
        r = run(["make"] + args, cwd=t)
        ok = r.returncode == 0 and os.path.isfile(os.path.join(t, "libft.a"))
        if not ok:
            fails.append(f"make {' '.join(args) or '(bare)'}")
        shutil.rmtree(t, ignore_errors=True)
    tally.report("`make` == `make all` == `make libft.a`", "CORE", not fails,
                  f"failed variant(s): {fails}" if fails else "all three variants succeed",
                  "all three succeed and produce libft.a", "make | make all | make libft.a",
                  "Subject: 'The all rule should be equivalent to make libft.a.'",
                  "Make 'all:' depend on libft.a (e.g. 'all: libft.a') rather than duplicating the build logic.")

    # --- Test 3: Makefile prints the commands it runs ----------------------
    tmp3 = fresh_ex01_env(makefile_path)
    res3 = run(["make"], cwd=tmp3)
    cc_lines = count_cc_lines(res3.stdout)
    tally.report("Makefile prints the compiler commands it runs", "CORE", cc_lines >= 5,
                  f"{cc_lines} visible compiler invocation line(s) in `make` output",
                  "at least 5 (one per source file)",
                  "make (fresh build, stdout inspected)",
                  "Subject: 'Your Makefile should print all the commands it's running.'",
                  "Don't prefix your compile/link recipe lines with '@' (or use .SILENT) -- that's exactly what suppresses command echoing.")
    shutil.rmtree(tmp3, ignore_errors=True)

    # --- Test 4: .o files live next to their .c files ----------------------
    tmp4 = fresh_ex01_env(makefile_path)
    run(["make"], cwd=tmp4)
    objs_in_srcs = [f for f in os.listdir(os.path.join(tmp4, "srcs")) if f.endswith(".o")]
    objs_at_root = [f for f in os.listdir(tmp4) if f.endswith(".o")]
    ok4 = len(objs_in_srcs) == 5 and not objs_at_root
    tally.report(".o files are placed next to their .c files (in srcs/)", "CORE", ok4,
                  f"{len(objs_in_srcs)} .o in srcs/, {len(objs_at_root)} .o at root",
                  "5 .o files in srcs/, 0 at root",
                  "make (fresh build)",
                  "Subject: '.o files should be near their corresponding .c files.'",
                  "Your object-file rule's target path should mirror the source's directory (srcs/%.o: srcs/%.c), not dump every .o at the project root.")
    shutil.rmtree(tmp4, ignore_errors=True)

    # --- Test 5: libft.a is at the exercise root ----------------------------
    tmp5 = fresh_ex01_env(makefile_path)
    run(["make"], cwd=tmp5)
    at_root = os.path.isfile(os.path.join(tmp5, "libft.a"))
    in_srcs = os.path.isfile(os.path.join(tmp5, "srcs", "libft.a"))
    tally.report("libft.a is built at the root of the exercise", "CORE", at_root and not in_srcs,
                  f"at root: {at_root}, in srcs/: {in_srcs}", "at root, not inside srcs/",
                  "make (fresh build)", "Subject: 'The lib should be at the root of the exercise.'",
                  "Set the archive target/output path to the Makefile's own directory, not srcs/.")
    shutil.rmtree(tmp5, ignore_errors=True)

    # --- Test 6: make clean removes .o, keeps libft.a -----------------------
    tmp6 = fresh_ex01_env(makefile_path)
    run(["make"], cwd=tmp6)
    run(["make", "clean"], cwd=tmp6)
    objs_left = [f for f in os.listdir(os.path.join(tmp6, "srcs")) if f.endswith(".o")]
    lib_left = os.path.isfile(os.path.join(tmp6, "libft.a"))
    tally.report("`make clean` removes .o files but keeps libft.a", "CORE", not objs_left and lib_left,
                  f".o remaining: {objs_left}, libft.a present: {lib_left}",
                  "0 .o files remaining, libft.a still present",
                  "make && make clean",
                  "Subject: 'The clean rule should remove all the temporary generated files.'",
                  "clean should remove intermediate .o files only -- it must NOT remove libft.a (that's fclean's job).")
    shutil.rmtree(tmp6, ignore_errors=True)

    # --- Test 7: make fclean removes .o AND libft.a -------------------------
    tmp7 = fresh_ex01_env(makefile_path)
    run(["make"], cwd=tmp7)
    run(["make", "fclean"], cwd=tmp7)
    objs_left7 = [f for f in os.listdir(os.path.join(tmp7, "srcs")) if f.endswith(".o")]
    lib_left7 = os.path.isfile(os.path.join(tmp7, "libft.a"))
    tally.report("`make fclean` removes .o files AND libft.a", "CORE", not objs_left7 and not lib_left7,
                  f".o remaining: {objs_left7}, libft.a present: {lib_left7}",
                  "no .o files, no libft.a", "make && make fclean",
                  "Subject: 'The fclean rule should be like a make clean, plus removing all the binaries generated with make all.'",
                  "fclean should do everything clean does, plus rm the final libft.a.")
    shutil.rmtree(tmp7, ignore_errors=True)

    # --- Test 8: make re == fclean + all ------------------------------------
    tmp8 = fresh_ex01_env(makefile_path)
    run(["make"], cwd=tmp8)
    res8 = run(["make", "re"], cwd=tmp8)
    lib8 = os.path.isfile(os.path.join(tmp8, "libft.a"))
    objs8 = [f for f in os.listdir(os.path.join(tmp8, "srcs")) if f.endswith(".o")]
    tally.report("`make re` rebuilds cleanly (fclean + all)", "CORE",
                  res8.returncode == 0 and lib8 and len(objs8) == 5,
                  f"return={res8.returncode}, libft.a present: {lib8}, .o count: {len(objs8)}",
                  "return=0, libft.a present, 5 .o files freshly rebuilt",
                  "make && make re",
                  "Subject: 'The re rule should be like a make fclean followed by make all.'",
                  "re should chain fclean then all, e.g. 're: fclean all'.")
    shutil.rmtree(tmp8, ignore_errors=True)

    # --- Test 9: no unnecessary recompilation on a redundant `make` --------
    tmp9 = fresh_ex01_env(makefile_path)
    run(["make"], cwd=tmp9)
    before9 = obj_mtimes(tmp9)
    run(["make"], cwd=tmp9)
    after9 = obj_mtimes(tmp9)
    changed9 = [k for k in before9 if before9.get(k) != after9.get(k)]
    tally.report("A redundant second `make` recompiles nothing", "CORE", not changed9,
                  f"file(s) with a changed mtime: {changed9}" if changed9 else "no file's mtime changed",
                  "no .o or libft.a mtime changes",
                  "make && make (again, nothing modified)",
                  "Subject: 'Your Makefile should not run any unnecessary commands.' / 'should not compile any file unnecessarily.'",
                  "Check your dependency rules use real prerequisites (the .c and .h files), not a phony/always-rebuild target -- otherwise make can't tell anything is up to date.")
    shutil.rmtree(tmp9, ignore_errors=True)

    # --- Test 10: touching ONE source recompiles only that file ------------
    tmp10 = fresh_ex01_env(makefile_path)
    run(["make"], cwd=tmp10)
    before10 = obj_mtimes(tmp10)
    future = time.time() + 5
    touched_src = os.path.join(tmp10, "srcs", "ft_strlen.c")
    os.utime(touched_src, (future, future))
    run(["make"], cwd=tmp10)
    after10 = obj_mtimes(tmp10)
    changed10 = sorted([k for k in before10 if before10.get(k) != after10.get(k)])
    expected10 = sorted(["ft_strlen.o", "libft.a"])
    tally.report("Touching one .c file only recompiles that file", "CORE", changed10 == expected10,
                  f"recompiled: {changed10}", f"recompiled: {expected10}",
                  "touch srcs/ft_strlen.c && make",
                  "Confirms per-file dependency rules exist (each .o depends on its own .c/.h), rather than one rule that rebuilds everything whenever anything changes.",
                  "If every .o's mtime changed, you likely have one big recipe (or a single .o target with all .c files as prerequisites) instead of a pattern rule like 'srcs/%.o: srcs/%.c'.")
    shutil.rmtree(tmp10, ignore_errors=True)

    # --- TRAP: "Watch out for wildcards!" -- clean/fclean must not nuke ----
    #           unrelated files via an overly broad rm pattern.
    tmp11 = fresh_ex01_env(makefile_path)
    run(["make"], cwd=tmp11)
    sentinel_root = os.path.join(tmp11, "keepme.txt")
    sentinel_src = os.path.join(tmp11, "srcs", "keepme_src.txt")
    with open(sentinel_root, "w") as f: f.write("do not delete me\n")
    with open(sentinel_src, "w") as f: f.write("do not delete me either\n")
    run(["make", "fclean"], cwd=tmp11)
    header_ok = os.path.isfile(os.path.join(tmp11, "includes", "ft.h"))
    sentinels_ok = os.path.isfile(sentinel_root) and os.path.isfile(sentinel_src)
    tally.report("clean/fclean don't delete unrelated files (wildcard safety)", "TRAP",
                  header_ok and sentinels_ok,
                  f"sentinel files survived: {sentinels_ok}, includes/ft.h survived: {header_ok}",
                  "unrelated files untouched by fclean",
                  "place sentinel files, then run make fclean",
                  "TRAP: the subject explicitly warns 'Watch out for wildcards!'. An overly broad rm (e.g. 'rm -f *' at the project root, or 'rm -f *.o' run from the wrong directory) can delete files it was never meant to touch.",
                  "Scope your rm commands precisely: remove exactly the .o paths and exactly libft.a by name/path, never a bare '*' or a wildcard evaluated from the wrong working directory.")
    shutil.rmtree(tmp11, ignore_errors=True)


# ==========================================================================
#  EX02 : ft_split (same subject as C07's ft_split)
# ==========================================================================

EX02_HARNESS = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char **ft_split(char *str, char *charset);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Basic space-separated",                                     "CORE"},
    {"Consecutive separators collapse (no empty strings)",         "CORE"},
    {"Leading/trailing separators stripped",                       "CORE"},
    {"Multiple different separator characters",                    "CORE"},
    {"No separator present in string",                             "CORE"},
    {"Empty input string -> empty array",                          "CORE"},
    {"Empty charset -> no separators at all",                      "CORE"},
    {"Does not write through str (input must stay untouched)",     "TRAP"},
};

int main(int argc, char **argv)
{
    if (argc < 2)
        return 1;
    if (strcmp(argv[1], "list") == 0) {
        for (size_t i = 0; i < sizeof(META) / sizeof(META[0]); i++)
            printf("%zu" US "%s" US "%s\n", i, META[i].cat, META[i].name);
        return 0;
    }
    int id = atoi(argv[1]);

    const char *why_arr[] = {
        "Baseline correctness: splits on the given charset characters into an array of tokens, NULL-terminated as the subject states.",
        "Subject: 'There should be no empty strings in your array.' Consecutive separators must collapse into a single split point.",
        "Leading and trailing separator characters must not produce leading/trailing empty tokens in the result.",
        "charset can contain several distinct separator characters at once -- any of them should trigger a split.",
        "If charset never appears in str, the whole string is exactly one token.",
        "An empty input string has no tokens to produce.",
        "An empty charset means there are no separator characters at all -- the entire input is one token.",
        "TRAP: Subject states 'The string provided as an argument cannot be modified.' Writing through str (e.g. inserting '\\0' in place instead of allocating real substrings) corrupts the caller's buffer even though C won't stop you from doing it."
    };
    const char *hint_arr[] = {
        "Make sure your array is NULL-terminated and every token is a proper malloc'd copy, not a pointer into the original str.",
        "When scanning, treat a run of separator characters as a single boundary instead of splitting on each one individually.",
        "Skip leading separators before reading the first token, and don't emit a token for a trailing separator run.",
        "Check membership with something like strchr(charset, c) rather than comparing against one hardcoded separator.",
        "This should behave as if there were zero separators: one token containing the whole input.",
        "Guard against producing a single bogus empty token for an empty str; the result should have zero tokens.",
        "If charset is empty, your separator-membership check must correctly return 'not found' for every character.",
        "If this fails, you're likely writing separators as '\\0' directly into str to fake tokenization instead of malloc'ing and copying each token into its own buffer."
    };

    if (id == 7) {
        const char *original = "a,b,c";
        size_t len = strlen(original);
        char *buf = malloc(len + 2);
        memcpy(buf, original, len + 1);
        buf[len + 1] = (char)0x7A;

        char **ret = ft_split(buf, ",");

        int passed = 1;
        char got[128] = "str left byte-for-byte unchanged";
        if (memcmp(buf, original, len + 1) != 0) {
            passed = 0;
            snprintf(got, sizeof(got), "str content changed to \"%.60s\"", buf);
        } else if ((unsigned char)buf[len + 1] != 0x7A) {
            passed = 0;
            strcpy(got, "guard byte after str was overwritten (out-of-bounds write)");
        }

        int cnt = 0;
        if (ret) { while (ret[cnt]) { free(ret[cnt]); cnt++; } free(ret); }
        free(buf);

        char inputs[64];
        snprintf(inputs, sizeof(inputs), "str=\"%s\" charset=\",\"", original);

        printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s\n",
            META[id].name, META[id].cat, passed ? "PASS" : "FAIL", got,
            "str and the byte after it unchanged", inputs, why_arr[id], hint_arr[id]);
        return 0;
    }

    char *strs[] = {"Hello World Foo", "a,,b,,,c", ",,a,b,,", "a,b;c d", "Hello", "", "abc"};
    char *charsets[] = {" ", ",", ",", ",; ", ",", ",", ""};

    char *exp0[] = {"Hello", "World", "Foo", NULL};
    char *exp1[] = {"a", "b", "c", NULL};
    char *exp2[] = {"a", "b", NULL};
    char *exp3[] = {"a", "b", "c", "d", NULL};
    char *exp4[] = {"Hello", NULL};
    char *exp5[] = {NULL};
    char *exp6[] = {"abc", NULL};
    char **exps[] = {exp0, exp1, exp2, exp3, exp4, exp5, exp6};

    char *str = strs[id], *charset = charsets[id];
    char **exp = exps[id];
    char **ret = ft_split(str, charset);

    int passed = 1;
    char got[160] = "matches expected tokens";
    int got_count = 0, exp_count = 0;

    if (!ret) {
        if (id == 5) {
            strcpy(got, "NULL (acceptable for an empty result)");
        } else {
            passed = 0;
            strcpy(got, "NULL");
        }
    } else {
        while (exp[exp_count]) exp_count++;
        while (ret[got_count]) got_count++;
        if (got_count != exp_count) {
            passed = 0;
            snprintf(got, sizeof(got), "%d token(s)", got_count);
        } else {
            for (int i = 0; i < exp_count && passed; i++) {
                if (!ret[i] || strcmp(ret[i], exp[i]) != 0) {
                    passed = 0;
                    snprintf(got, sizeof(got), "token[%d] = \"%s\"", i, ret[i] ? ret[i] : "(null)");
                }
            }
        }
        for (int i = 0; i < got_count; i++) free(ret[i]);
        free(ret);
    }

    char expjoined[128] = "";
    for (int i = 0; exp[i]; i++) { strcat(expjoined, "\""); strcat(expjoined, exp[i]); strcat(expjoined, "\" "); }
    char inputs[128];
    snprintf(inputs, sizeof(inputs), "str=\"%s\" charset=\"%s\"", str, charset);

    printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "[%s]" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, passed ? "PASS" : "FAIL", got, expjoined, inputs, why_arr[id], hint_arr[id]);
    return 0;
}
"""

def run_ex02(ex_dir, tally):
    print(f"\n{C_CYAN}{C_BOLD}============ Evaluating ex02 (ft_split.c) ============{C_RESET}")

    src = os.path.abspath(os.path.join(ex_dir, "ft_split.c"))
    if not os.path.isfile(src):
        tally.report("ft_split.c present", "CORE", False, "missing", "ex02/ft_split.c present",
                      "ex02/ft_split.c", "The turn-in directory must contain ft_split.c.",
                      "Create ex02/ft_split.c.")
        return

    tmp_dir = tempfile.mkdtemp()
    try:
        harness_path = os.path.join(tmp_dir, "harness.c")
        bin_path = os.path.join(tmp_dir, "test_runner")
        with open(harness_path, "w") as f:
            f.write(EX02_HARNESS)
        comp = run([CC] + CFLAGS + [harness_path, src, "-o", bin_path], cwd=tmp_dir)
        if comp.returncode != 0:
            tally.report("Compiles cleanly (-Wall -Wextra -Werror)", "CORE", False,
                          "compilation error", "clean compile", "cc -Wall -Wextra -Werror ft_split.c",
                          "Moulinette compiles with -Wall -Wextra -Werror; any warning is a hard failure.",
                          f"Compiler said:\n{comp.stderr.strip()[:600]}")
            return

        list_res = run([bin_path, "list"], cwd=tmp_dir)
        tests = []
        for line in list_res.stdout.strip().split("\n"):
            if US in line:
                t_id, t_cat, t_name = line.split(US, 2)
                tests.append((t_id, t_cat, t_name))

        for t_id, t_cat, t_name in tests:
            res = run([bin_path, t_id], cwd=tmp_dir, timeout=5)
            if res.returncode != 0:
                tally.report(t_name, t_cat, False, f"crashed (exit {res.returncode})", "clean run",
                             f"test id {t_id}", "-", "A crash usually means an out-of-bounds access or NULL-array indexing bug.")
                continue
            out = res.stdout.strip()
            if not out.startswith("RESULT" + US):
                tally.report(t_name, t_cat, False, "invalid harness output", "RESULT line", f"test id {t_id}", "-", "-")
                continue
            parts = out.split(US)
            if len(parts) < 9:
                tally.report(t_name, t_cat, False, "malformed harness output", "9 fields", f"test id {t_id}", "-", "-")
                continue
            _, name, category, status, got, expected, inputs, why, hint = parts[:9]
            tally.report(name, category, status == "PASS", got, expected, inputs, why, hint)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# ==========================================================================
#  MAIN
# ==========================================================================

RUNNERS = {"ex00": run_ex00, "ex01": run_ex01, "ex02": run_ex02}

def main():
    print(f"{C_WHITE}{C_BOLD}=========================================================")
    print("        42 PISCINE C09 - ADVERSARIAL / VERBOSE TESTER    ")
    print("=========================================================")
    print(f"{C_RESET}{C_DIM}CORE  = tests a rule stated in the subject; counts toward score/rank.")
    print(f"TRAP  = adversarial edge case (wildcard damage, forbidden calls,")
    print(f"        pointer self-aliasing, etc); informational only, never affects score.{C_RESET}")

    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    exercises = sorted(RUNNERS.keys())
    if args:
        exercises = [a for a in exercises if a in args]
        if not exercises:
            print_fail(f"No matching exercises for: {args}")
            return

    results = []
    for ex in exercises:
        tally = Tally()
        RUNNERS[ex](ex, tally)
        score = tally.score()
        rank = calculate_rank(score)
        results.append((ex, score, rank, tally.trap_pass, tally.trap_total))

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
