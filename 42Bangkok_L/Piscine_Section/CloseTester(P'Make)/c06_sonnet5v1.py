#!/usr/bin/env python3
"""
C06 Tester - ft_print_program_name / ft_print_params / ft_rev_params / ft_sort_params

Design philosophy (matches your C02/C03/C04 testers):
  - MANDATORY tests  -> things the real moulinette almost certainly checks
                        (spec-explicit behavior). These drive your score.
  - TRAP tests       -> UB / adversarial / "did you cheat" checks that the
                        official grader probably does NOT run, but that
                        reveal real bugs or forbidden-function usage.
                        Reported separately, never tank your S-rank.

Key subject constraint for C06: "Allowed functions: write" -- ONLY write.
No printf/puts/strlen/exit/malloc/etc. That's checked statically AND
exploited dynamically (format-string trap args like "%s%n").

Usage:
    python3 c06_tester.py [path_to_piscine_root]

Expected layout:
    <root>/ex00/ft_print_program_name.c
    <root>/ex01/ft_print_params.c
    <root>/ex02/ft_rev_params.c
    <root>/ex03/ft_sort_params.c
"""

import os
import re
import sys
import shutil
import subprocess
import tempfile

# ---------------------------------------------------------------------------
# Cosmetics
# ---------------------------------------------------------------------------

class C:
    G = "\033[92m"
    R = "\033[91m"
    Y = "\033[93m"
    B = "\033[94m"
    M = "\033[95m"
    CY = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    END = "\033[0m"


def ok(s):   return f"{C.G}{s}{C.END}"
def bad(s):  return f"{C.R}{s}{C.END}"
def warn(s): return f"{C.Y}{s}{C.END}"
def info(s): return f"{C.CY}{s}{C.END}"


RANKS = [
    (100, "S — flawless. Moulinette has nothing on you."),
    (90,  "A — very solid, minor gaps."),
    (75,  "B — works, but check the mandatory failures."),
    (50,  "C — functional core, missing edge cases."),
    (25,  "D — partially working."),
    (0,   "F — not there yet."),
]


def rank_for(pct):
    for threshold, label in RANKS:
        if pct >= threshold:
            return label
    return RANKS[-1][1]


# ---------------------------------------------------------------------------
# Forbidden function static check
# ---------------------------------------------------------------------------

# Only `write` is allowed for this whole module. Anything below is a cheat
# signal if it appears as a real call (best-effort: strips comments/strings
# first, then looks for identifier( )).
FORBIDDEN_FUNCS = [
    "printf", "fprintf", "sprintf", "snprintf", "vprintf", "vfprintf",
    "puts", "putchar", "fputs", "fputc",
    "exit", "_exit", "abort",
    "malloc", "calloc", "realloc", "free",
    "strlen", "strcpy", "strncpy", "strcat", "strncat", "strcmp", "strncmp",
    "memcpy", "memset", "memmove", "memcmp",
    "read", "open", "close", "fopen", "fclose",
    "scanf", "fscanf", "gets",
    "system", "execve", "execvp",
]


def strip_comments_and_strings(src):
    # crude but effective: remove /* */ and // comments, and "..." / '...' contents
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    src = re.sub(r"//.*", " ", src)
    src = re.sub(r'"(?:\\.|[^"\\])*"', '""', src)
    src = re.sub(r"'(?:\\.|[^'\\])*'", "''", src)
    return src


def find_forbidden_calls(source_path):
    with open(source_path, "r", errors="replace") as f:
        raw = f.read()
    cleaned = strip_comments_and_strings(raw)
    hits = []
    for fn in FORBIDDEN_FUNCS:
        if re.search(rf"(?<![A-Za-z0-9_]){fn}\s*\(", cleaned):
            hits.append(fn)
    return hits


# ---------------------------------------------------------------------------
# Compilation
# ---------------------------------------------------------------------------

def compile_source(source_path, out_path):
    cmd = ["cc", "-Wall", "-Wextra", "-Werror", "-o", out_path, source_path]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode == 0, proc.stdout, proc.stderr


# ---------------------------------------------------------------------------
# Test case definitions
# ---------------------------------------------------------------------------
# Each test: (name, category, argv_list_after_prog_name, expected_fn)
# category is "MANDATORY" or "TRAP"

BIG = "A" * 100_000

COMMON_ARG_SETS = {
    "basic":        ["hello", "world"],
    "single":       ["onlyone"],
    "no_args":      [],
    "empty_str":    [""],
    "with_spaces":  ["hello world", "second one"],
    "embedded_nl":  ["foo\nbar", "baz"],
    "dupes":        ["same", "same", "same"],
    "long_arg":     [BIG, "short"],
    "many_args":    [f"arg{i}" for i in range(200)],
    "dash_args":    ["-", "--", "-x"],
    "nonprintable": ["\x01\x02\x03", "\x7f"],
    "fmt_string":   ["%s%s%s%n", "%x%x%x%x"],
    "mixed_empty":  ["a", "", "b", ""],
    "tabs":         ["a\tb", "\t\t"],
}


def build_tests_ex01():
    tests = []
    for name, argv in COMMON_ARG_SETS.items():
        cat = "TRAP" if name in ("fmt_string", "nonprintable", "long_arg", "many_args") else "MANDATORY"
        expected = "".join(a + "\n" for a in argv)
        tests.append((name, cat, argv, expected))
    return tests


def build_tests_ex02():
    tests = []
    for name, argv in COMMON_ARG_SETS.items():
        cat = "TRAP" if name in ("fmt_string", "nonprintable", "long_arg", "many_args") else "MANDATORY"
        expected = "".join(a + "\n" for a in reversed(argv))
        tests.append((name, cat, argv, expected))
    return tests


def build_tests_ex03():
    tests = []
    sort_sets = {
        "basic":         ["banana", "apple", "cherry"],
        "case_sensitive": ["banana", "Apple", "cherry"],           # ASCII: uppercase < lowercase
        "numeric_strings": ["10", "9", "2"],                        # lexicographic, not numeric
        "dupes":          ["b", "a", "b", "a"],
        "prefix_order":   ["app", "apple", "ap"],                   # shorter prefix sorts first
        "punctuation":    ["a1", "!x", "$y", "1z", "Az"],
        "negative_look":  ["-5", "5", "-1", "1"],
        "single":         ["onlyone"],
        "no_args":        [],
        "empty_included": ["b", "", "a"],
        "already_sorted": ["1", "2", "3"],
        "reverse_sorted": ["c", "b", "a"],
        "many_random":    ["kiwi", "fig", "date", "banana", "apple", "elderberry",
                            "grape", "honeydew", "jackfruit", "lemon"] * 5,
        "nonprintable":   ["\x02b", "\x01a"],
        "fmt_string":     ["%s%n", "%x"],
    }
    tests = []
    for name, argv in sort_sets.items():
        cat = "TRAP" if name in ("fmt_string", "nonprintable", "many_random") else "MANDATORY"
        expected = "".join(a + "\n" for a in sorted(argv))
        tests.append((name, cat, argv, expected))
    return tests


def build_tests_ex00():
    # ex00 tests different invocation paths/names to make sure the program
    # doesn't hardcode its own name or strip the path -- it must print
    # argv[0] EXACTLY as invoked.
    return [
        ("dot_slash_name",  "MANDATORY"),
        ("renamed_binary",  "MANDATORY"),
        ("subdir_path",     "MANDATORY"),
        ("extra_argv_ignored", "TRAP"),
    ]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_bin(bin_path, argv, argv0=None, cwd=None):
    """Run bin_path with the given argv (excluding argv[0]) and return raw stdout bytes."""
    full_argv0 = argv0 if argv0 is not None else bin_path
    args = [bin_path] + argv
    try:
        proc = subprocess.run(args, capture_output=True, timeout=5, cwd=cwd)
        return proc.stdout, proc.returncode, None
    except subprocess.TimeoutExpired:
        return b"", None, "TIMEOUT"
    except Exception as e:  # noqa: BLE001
        return b"", None, str(e)


def test_exercise_argv(ex_name, source_file, tests):
    print(f"\n{C.BOLD}{C.M}=== {ex_name}: {source_file} ==={C.END}")

    if not os.path.isfile(source_file):
        print(bad(f"  ✗ FILE NOT FOUND: {source_file}"))
        return {"mandatory_total": 0, "mandatory_pass": 0, "trap_total": 0, "trap_pass": 0, "compiled": False}

    # forbidden function scan
    forbidden = find_forbidden_calls(source_file)
    if forbidden:
        print(bad(f"  ✗ FORBIDDEN FUNCTIONS DETECTED: {', '.join(forbidden)}"))
        print(warn("    -> Only `write` is allowed for this module. This is a -42 in real moulinette."))
    else:
        print(ok("  ✓ No forbidden functions detected (only `write` used)"))

    with tempfile.TemporaryDirectory() as tmp:
        bin_path = os.path.join(tmp, "prog")
        success, out, err = compile_source(source_file, bin_path)
        if not success:
            print(bad("  ✗ COMPILATION FAILED (-Wall -Wextra -Werror)"))
            print(C.DIM + err.strip() + C.END)
            return {"mandatory_total": len(tests), "mandatory_pass": 0,
                     "trap_total": 0, "trap_pass": 0, "compiled": False}
        print(ok("  ✓ Compiles cleanly with -Wall -Wextra -Werror"))

        results = {"mandatory_total": 0, "mandatory_pass": 0,
                   "trap_total": 0, "trap_pass": 0, "compiled": True}

        for name, cat, argv, expected in tests:
            out_bytes, rc, err_msg = run_bin(bin_path, argv)
            expected_bytes = expected.encode("utf-8", errors="surrogateescape")
            passed = (out_bytes == expected_bytes) and err_msg is None

            bucket_total = "mandatory_total" if cat == "MANDATORY" else "trap_total"
            bucket_pass = "mandatory_pass" if cat == "MANDATORY" else "trap_pass"
            results[bucket_total] += 1
            if passed:
                results[bucket_pass] += 1

            tag = f"[{cat}]"
            if passed:
                print(f"  {ok('✓')} {tag:<11} {name}")
            else:
                print(f"  {bad('✗')} {tag:<11} {name}")
                if err_msg:
                    print(warn(f"      runtime error: {err_msg}"))
                else:
                    print(f"      expected: {expected_bytes[:120]!r}{'...' if len(expected_bytes) > 120 else ''}")
                    print(f"      got:      {out_bytes[:120]!r}{'...' if len(out_bytes) > 120 else ''}")
                print(hint_for(ex_name, name))

    return results


def hint_for(ex_name, test_name):
    hints = {
        "no_args": "  Hint: with argc == 1 you should print nothing at all -- no stray newline, no crash.",
        "empty_str": "  Hint: an empty argv string still needs to be printed (as an empty line).",
        "embedded_nl": "  Hint: don't special-case '\\n' inside an argument -- print raw bytes, then your own trailing \\n.",
        "long_arg": "  Hint: classic off-by-one/buffer bug -- make sure your write() covers the FULL length, no truncation.",
        "many_args": "  Hint: check your loop bound is `i < argc`, not `i <= argc` (that reads argv[argc], which is NULL).",
        "fmt_string": "  Hint: if this fails only when you (secretly) use printf(argv[i]) directly, that's a format-string bug -- and forbidden anyway.",
        "case_sensitive": "  Hint: ASCII sort is case-SENSITIVE. Uppercase letters (65-90) sort before lowercase (97-122).",
        "numeric_strings": "  Hint: sort is lexicographic on bytes, not numeric. '10' < '9' because '1' < '9'.",
        "prefix_order": "  Hint: when one string is a prefix of another, the shorter one sorts first (like strcmp).",
        "negative_look": "  Hint: '-' (0x2D) sorts before digits (0x30+), so '-5' < '5'.",
        "dot_slash_name": "  Hint: print argv[0] EXACTLY as given -- don't strip './' or any path component.",
        "alt_invocation_name": "  Hint: don't hardcode your own filename -- always print argv[0], whatever it is.",
        "subdir_path": "  Hint: argv[0] can contain a full path; print it verbatim.",
        "extra_argv_ignored": "  Hint: ft_print_program_name must ignore argv[1..] entirely.",
    }
    return C.DIM + hints.get(test_name, "  Hint: re-check the exact spec for this case.") + C.END


def test_ex00(source_file):
    ex_name = "ex00 - ft_print_program_name"
    print(f"\n{C.BOLD}{C.M}=== {ex_name}: {source_file} ==={C.END}")

    if not os.path.isfile(source_file):
        print(bad(f"  ✗ FILE NOT FOUND: {source_file}"))
        return {"mandatory_total": 0, "mandatory_pass": 0, "trap_total": 0, "trap_pass": 0, "compiled": False}

    forbidden = find_forbidden_calls(source_file)
    if forbidden:
        print(bad(f"  ✗ FORBIDDEN FUNCTIONS DETECTED: {', '.join(forbidden)}"))
    else:
        print(ok("  ✓ No forbidden functions detected (only `write` used)"))

    results = {"mandatory_total": 0, "mandatory_pass": 0, "trap_total": 0, "trap_pass": 0, "compiled": True}

    with tempfile.TemporaryDirectory() as tmp:
        bin_path = os.path.join(tmp, "compiled_original")
        success, out, err = compile_source(source_file, bin_path)
        if not success:
            print(bad("  ✗ COMPILATION FAILED (-Wall -Wextra -Werror)"))
            print(C.DIM + err.strip() + C.END)
            results["mandatory_total"] = 4
            results["compiled"] = False
            return results
        print(ok("  ✓ Compiles cleanly with -Wall -Wextra -Werror"))

        # 1. dot_slash_name : invoke as "./ft_print_program_name"
        local_name = os.path.join(tmp, "ft_print_program_name")
        shutil.copy(bin_path, local_name)
        os.chmod(local_name, 0o755)
        expected = f"{local_name}\n".encode()
        out_bytes, rc, err_msg = run_bin(local_name, [])
        _record(results, "MANDATORY", "dot_slash_name", out_bytes == expected,
                expected, out_bytes, err_msg, "ex00")

        # 2. alt_invocation_name : copy to a different, unremarkable name
        renamed = os.path.join(tmp, "a.out")
        shutil.copy(bin_path, renamed)
        os.chmod(renamed, 0o755)
        expected2 = f"{renamed}\n".encode()
        out2, rc2, err2 = run_bin(renamed, [])
        _record(results, "MANDATORY", "alt_invocation_name", out2 == expected2,
                expected2, out2, err2, "ex00")

        # 3. subdir_path : invoke via a nested relative path
        subdir = os.path.join(tmp, "bin", "release")
        os.makedirs(subdir, exist_ok=True)
        nested_bin = os.path.join(subdir, "myprog")
        shutil.copy(bin_path, nested_bin)
        os.chmod(nested_bin, 0o755)
        expected3 = f"{nested_bin}\n".encode()
        out3, rc3, err3 = run_bin(nested_bin, [])
        _record(results, "MANDATORY", "subdir_path", out3 == expected3,
                expected3, out3, err3, "ex00")

        # 4. extra_argv_ignored : pass garbage args, should be ignored
        expected4 = f"{local_name}\n".encode()
        out4, rc4, err4 = run_bin(local_name, ["ignored1", "ignored2"])
        _record(results, "TRAP", "extra_argv_ignored", out4 == expected4,
                expected4, out4, err4, "ex00")

    return results


def _record(results, cat, name, passed, expected, got, err_msg, ex_name):
    bucket_total = "mandatory_total" if cat == "MANDATORY" else "trap_total"
    bucket_pass = "mandatory_pass" if cat == "MANDATORY" else "trap_pass"
    results[bucket_total] += 1
    if passed:
        results[bucket_pass] += 1
    tag = f"[{cat}]"
    if passed:
        print(f"  {ok('✓')} {tag:<11} {name}")
    else:
        print(f"  {bad('✗')} {tag:<11} {name}")
        if err_msg:
            print(warn(f"      runtime error: {err_msg}"))
        else:
            print(f"      expected: {expected[:150]!r}")
            print(f"      got:      {got[:150]!r}")
        print(hint_for(ex_name, name))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    root = os.path.abspath(root)

    print(f"{C.BOLD}{C.CY}C06 Piscine Tester{C.END}  {C.DIM}(root: {root}){C.END}")

    exercises = [
        ("ex00", os.path.join(root, "ex00", "ft_print_program_name.c"), None),
        ("ex01", os.path.join(root, "ex01", "ft_print_params.c"), build_tests_ex01),
        ("ex02", os.path.join(root, "ex02", "ft_rev_params.c"), build_tests_ex02),
        ("ex03", os.path.join(root, "ex03", "ft_sort_params.c"), build_tests_ex03),
    ]

    all_results = {}
    for ex_name, source_file, builder in exercises:
        if ex_name == "ex00":
            res = test_ex00(source_file)
        else:
            res = test_exercise_argv(ex_name, source_file, builder())
        all_results[ex_name] = res

    # -----------------------------------------------------------------
    print(f"\n{C.BOLD}{C.CY}{'='*60}{C.END}")
    print(f"{C.BOLD}{C.CY}SUMMARY{C.END}")
    print(f"{C.BOLD}{C.CY}{'='*60}{C.END}")

    total_mand = total_mand_pass = 0
    total_trap = total_trap_pass = 0

    for ex_name, res in all_results.items():
        m_t, m_p = res["mandatory_total"], res["mandatory_pass"]
        t_t, t_p = res["trap_total"], res["trap_pass"]
        total_mand += m_t
        total_mand_pass += m_p
        total_trap += t_t
        total_trap_pass += t_p

        if not res["compiled"]:
            print(f"{ex_name}: {bad('DOES NOT COMPILE')}")
            continue

        pct = (m_p / m_t * 100) if m_t else 100
        color = ok if pct == 100 else (warn if pct >= 50 else bad)
        print(f"{ex_name}: {color(f'{m_p}/{m_t} mandatory')}"
              + (f"  {C.DIM}({t_p}/{t_t} trap){C.END}" if t_t else ""))

    overall_pct = (total_mand_pass / total_mand * 100) if total_mand else 0
    print(f"\n{C.BOLD}Overall (mandatory only): {total_mand_pass}/{total_mand} "
          f"({overall_pct:.0f}%){C.END}")
    print(f"{C.DIM}Trap/adversarial: {total_trap_pass}/{total_trap} "
          f"(informational, not part of moulinette-equivalent score){C.END}")
    print(f"\n{C.BOLD}Rank: {rank_for(overall_pct)}{C.END}")

    if total_trap_pass < total_trap:
        print(warn(f"\nNote: {total_trap - total_trap_pass} trap test(s) failed. These probably won't "
                    "cost you moulinette points, but they usually point at real bugs or "
                    "forbidden-function shortcuts worth fixing before defense."))


if __name__ == "__main__":
    main()
