#!/usr/bin/env python3
"""
42 Piscine - C08 Adversarial Tester
-----------------------------------
C08 is different from C05/C07: most exercises are header files with no
behaviour of their own (ft.h, ft_boolean.h, ft_abs.h, ft_point.h). There is
nothing to "fuzz" inside a bare prototype. So instead of inventing fake
edge cases, this tester checks the things that are genuinely gradable here:

  * Does your header compile with EXACTLY the signatures/types/fields the
    subject demands? (checked by compiling real code that uses them the
    way the subject's own examples use them -- a mismatch means a real
    compile error, not a guess)
  * Does it compile the EXACT main() the subject provides, verbatim?
  * Does a missing header guard actually break something (for structs,
    it reliably does -- verified empirically before writing this test)?
  * Is the ABS macro correctly parenthesised (both around its argument
    AND around the whole expansion)? This is a classic, well known macro
    bug with an objectively right/wrong answer.
  * For ex04/ex05 (real .c files), does the behaviour match the subject,
    AND does the source avoid functions outside the allowed list (only
    'malloc, free' for ex04, only 'write' for ex05) -- since using a
    forbidden function is an automatic -42 per the subject's own rules.

Same reporting conventions as the C05/C07 testers:
  CORE = tests a rule stated in the subject; counts toward score/rank.
  TRAP = adversarial/edge case, not explicitly graded, but flags a real
         bug class (missing header guards, macro hygiene, etc). Never
         affects the score.

Usage:
    python3 c08_tester.py            # normal run
    python3 c08_tester.py -v         # verbose: show rationale for every test
    python3 c08_tester.py ex04       # only run a specific exercise
"""

import os
import re
import sys
import subprocess
import tempfile
import shutil

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


def print_pass(msg):
    print(f"{C_GREEN}[PASS]{C_RESET} {msg}")


def print_fail(msg):
    print(f"{C_RED}[FAIL]{C_RESET} {msg}")


def tag(category):
    if category == "TRAP":
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


class Reporter:
    def __init__(self):
        self.core_pass = 0
        self.core_total = 0
        self.trap_pass = 0
        self.trap_total = 0

    def record(self, name, category, passed, why, hint=None, got=None, expected=None):
        if category == "CORE":
            self.core_total += 1
        else:
            self.trap_total += 1
        if passed:
            if category == "CORE":
                self.core_pass += 1
            else:
                self.trap_pass += 1
            print_pass(f"{tag(category)} {name}")
            if VERBOSE:
                print(f"      {C_DIM}Why      : {why}{C_RESET}")
        else:
            print_fail(f"{tag(category)} {name}")
            if got is not None or expected is not None:
                print(f"  ├── Got      : {C_RED}{got}{C_RESET}")
                print(f"  ├── Expected : {C_GREEN}{expected}{C_RESET}")
            print(f"  ├── Why      : {why}")
            print(f"  └── Hint     : {C_YELLOW}{hint}{C_RESET}")

    def score(self):
        return int((self.core_pass / self.core_total) * 100) if self.core_total > 0 else 0


# ==========================================================================
#  GENERIC HELPERS
# ==========================================================================

def compile_sources(tmp_dir, files, out_name="test_runner", extra_flags=None):
    """files: dict of {filename: content} to write into tmp_dir before compiling.
    Any filename not ending in .c is written but not passed to cc directly
    (e.g. headers included by the .c files)."""
    for fname, content in files.items():
        with open(os.path.join(tmp_dir, fname), "w") as f:
            f.write(content)
    c_files = [f for f in files if f.endswith(".c")]
    cmd = ["cc", "-Wall", "-Wextra", "-Werror"] + (extra_flags or []) + c_files + ["-o", out_name]
    return subprocess.run(cmd, cwd=tmp_dir, capture_output=True, text=True)


def run_bin(tmp_dir, out_name="test_runner", args=None, timeout=10):
    exe = os.path.join(tmp_dir, out_name)
    try:
        return subprocess.run([exe] + (args or []), capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None


def copy_student_file(ex_dir, filename, tmp_dir):
    src = os.path.join(ex_dir, filename)
    if not os.path.exists(src):
        return False
    shutil.copy(src, tmp_dir)
    return True


def grep_forbidden(ex_dir, filename, forbidden, allowed_note):
    """Heuristic text scan for calls to functions outside the allowed list.
    Not a real parser (won't understand comments/strings perfectly), but
    catches the common real-world case: a call like 'foo(' appearing in
    the source. Returns list of matches found."""
    path = os.path.join(ex_dir, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", errors="ignore") as f:
        text = f.read()
    # crude comment/string stripping to reduce false positives
    text = re.sub(r"//.*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r'"(\\.|[^"\\])*"', '""', text)
    found = []
    for fn in forbidden:
        if re.search(r"\b" + re.escape(fn) + r"\s*\(", text):
            found.append(fn)
    return found


STOCK_STR_H = """#ifndef FT_STOCK_STR_H
# define FT_STOCK_STR_H

typedef struct s_stock_str
{
	int		size;
	char	*str;
	char	*copy;
}	t_stock_str;

#endif
"""

# ==========================================================================
#  EX00 : ft.h
# ==========================================================================

def test_ex00(ex_dir, rep):
    header = "ft.h"
    if not os.path.exists(os.path.join(ex_dir, header)):
        rep.record("ft.h exists", "CORE", False,
                   "The subject requires a single file, ft.h, containing five prototypes.",
                   f"Create {ex_dir}/{header}.")
        return

    rep.record("ft.h exists", "CORE", True,
               "The subject requires a single file, ft.h, containing five prototypes.")

    harness = """
#include "ft.h"
#include <unistd.h>

void	ft_putchar(char c)
{
	write(1, &c, 1);
}

void	ft_swap(int *a, int *b)
{
	int	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}

void	ft_putstr(char *str)
{
	while (*str)
		write(1, str++, 1);
}

int	ft_strlen(char *str)
{
	int	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

int	ft_strcmp(char *s1, char *s2)
{
	while (*s1 && *s1 == *s2)
	{
		s1++;
		s2++;
	}
	return (*(unsigned char *)s1 - *(unsigned char *)s2);
}

int	main(void)
{
	return (0);
}
"""
    tmp_dir = tempfile.mkdtemp()
    try:
        copy_student_file(ex_dir, header, tmp_dir)
        res = compile_sources(tmp_dir, {"harness.c": harness})
        why = ("Every prototype in ft.h must match EXACTLY what the subject shows: same "
               "return type, same parameter types, same parameter order (void ft_putchar(char), "
               "void ft_swap(int*, int*), void ft_putstr(char*), int ft_strlen(char*), "
               "int ft_strcmp(char*, char*)). This harness defines each function itself with "
               "the exact expected signature -- if your header's prototype disagrees on even "
               "one type, the compiler will refuse with a 'conflicting types' error.")
        hint = ("Check each prototype character by character against the subject: a missing "
               "'char *' vs 'char*' won't matter, but 'const char *' vs 'char *', or a missing "
               "pointer '*', or int vs void, will. If ft.h also contains actual function BODIES "
               "(not just prototypes), that's also wrong -- the subject only asks for prototypes "
               "here, and this harness supplies its own bodies, so any bodies in ft.h would clash.")
        rep.record("All five prototypes match exactly", "CORE", res.returncode == 0, why, hint,
                   got=(res.stderr.strip()[:300] if res.returncode != 0 else "compiled cleanly"),
                   expected="clean compile")
    finally:
        shutil.rmtree(tmp_dir)


# ==========================================================================
#  EX01 : ft_boolean.h
# ==========================================================================

def test_ex01(ex_dir, rep):
    header = "ft_boolean.h"
    if not os.path.exists(os.path.join(ex_dir, header)):
        rep.record("ft_boolean.h exists", "CORE", False,
                   "The subject requires ft_boolean.h to define t_bool, TRUE, FALSE, EVEN, "
                   "EVEN_MSG, ODD_MSG and SUCCESS.",
                   f"Create {ex_dir}/{header}.")
        return
    rep.record("ft_boolean.h exists", "CORE", True,
               "The subject requires ft_boolean.h to define t_bool, TRUE, FALSE, EVEN, "
               "EVEN_MSG, ODD_MSG and SUCCESS.")

    # The EXACT main from the subject, verbatim -- including the fact that it
    # only #includes "ft_boolean.h" and still calls write(). If your header
    # doesn't pull in unistd.h itself, this deliberately won't compile --
    # exactly like the real grading would behave.
    harness = """
#include "ft_boolean.h"

void	ft_putstr(char *str){
	while (*str)
		write(1, str++, 1);
}

t_bool	ft_is_even(int nbr)
{
	return ((EVEN(nbr)) ? TRUE : FALSE);
}

int	main(int argc, char **argv)
{
	(void)argv;
	if (ft_is_even(argc - 1) == TRUE)
		ft_putstr(EVEN_MSG);
	else
		ft_putstr(ODD_MSG);
	return (SUCCESS);
}
"""
    tmp_dir = tempfile.mkdtemp()
    try:
        copy_student_file(ex_dir, header, tmp_dir)
        res = compile_sources(tmp_dir, {"harness.c": harness})
        why = ("This is the EXACT main() printed in the subject, copy-pasted verbatim. Notice it "
               "only does '#include \"ft_boolean.h\"' and yet calls write() directly -- the "
               "subject's own instructions warn 'carefully examine the examples, they may contain "
               "crucial details not explicitly stated'. This is that detail: your ft_boolean.h "
               "must #include <unistd.h> itself, or this won't compile at all.")
        hint = "Add '#include <unistd.h>' inside ft_boolean.h itself (behind your header guard)."
        compiled = res.returncode == 0
        rep.record("Compiles the exact subject-provided main()", "CORE", compiled, why, hint,
                   got=(res.stderr.strip()[:400] if not compiled else "compiled cleanly"),
                   expected="clean compile")
        if not compiled:
            return  # can't run further checks

        cases = [
            (0, "I have an even number of arguments.\n", "0 extra arguments (even)"),
            (1, "I have an odd number of arguments.\n", "1 extra argument (odd)"),
            (4, "I have an even number of arguments.\n", "4 extra arguments (even, rules out a hardcoded 0-case)"),
            (7, "I have an odd number of arguments.\n", "7 extra arguments (odd, rules out a hardcoded 1-case)"),
        ]
        for n_args, expected, label in cases:
            proc = run_bin(tmp_dir, args=["x"] * n_args)
            got = proc.stdout if proc else "(timeout)"
            passed = proc is not None and got == expected
            why2 = (f"Runs the compiled program with {label}: argc-1 = {n_args}. "
                    f"EVEN({n_args}) must select the right message and EVEN_MSG/ODD_MSG must "
                    f"print byte-for-byte as shown in the subject (including the trailing newline).")
            hint2 = ("Check the EVEN(nbr) macro's parity logic (nbr % 2 == 0, and make sure it's "
                    "wrapped in parentheses -- see the ABS macro trap in ex02 for why that matters "
                    "here too), and check EVEN_MSG/ODD_MSG include the exact wording and a trailing '\\n'.")
            rep.record(f"Program output for {label}", "CORE", passed, why2, hint2,
                       got=repr(got), expected=repr(expected))

        proc0 = run_bin(tmp_dir, args=[])
        exit_ok = proc0 is not None and proc0.returncode == 0
        rep.record("SUCCESS is defined as 0 (process exit code)", "CORE", exit_ok,
                   "main() returns (SUCCESS); a shell/CI checking the exit code expects the "
                   "conventional 0-for-success value.",
                   "Check '#define SUCCESS' evaluates to 0.",
                   got=(proc0.returncode if proc0 else "timeout"), expected=0)
    finally:
        shutil.rmtree(tmp_dir)

    # TRAP: double inclusion. Whether this matters depends on HOW t_bool was
    # implemented (typedef int vs typedef enum) -- verified empirically:
    # 'typedef int t_bool;' survives double-inclusion fine even with no guard,
    # but 'typedef enum {...} t_bool;' does not. So this is informative, not
    # a hard grading rule, hence TRAP rather than CORE.
    tmp_dir2 = tempfile.mkdtemp()
    try:
        copy_student_file(ex_dir, header, tmp_dir2)
        dbl = """
#include "ft_boolean.h"
#include "ft_boolean.h"

int	main(void)
{
	t_bool	b;

	b = TRUE;
	return ((b == TRUE) ? 0 : 1);
}
"""
        res2 = compile_sources(tmp_dir2, {"double_include.c": dbl}, out_name="dbl_runner")
        why = ("TRAP: includes ft_boolean.h twice in the same file (this can genuinely happen in "
              "a real project via nested includes). Whether this breaks depends on how you wrote "
              "t_bool: 'typedef int t_bool;' happens to survive re-inclusion even without a guard, "
              "but 'typedef enum {...} t_bool;' does NOT (confirmed empirically) -- it's a real "
              "compile error, not just a style nitpick. Either way, a header guard costs nothing "
              "and removes the risk entirely.")
        hint = "Wrap the whole file in '#ifndef FT_BOOLEAN_H' / '#define FT_BOOLEAN_H' / '#endif'."
        rep.record("Survives being #included twice", "TRAP", res2.returncode == 0, why, hint,
                  got=(res2.stderr.strip()[:300] if res2.returncode != 0 else "compiled cleanly"),
                  expected="compiles regardless of typedef style")
    finally:
        shutil.rmtree(tmp_dir2)


# ==========================================================================
#  EX02 : ft_abs.h
# ==========================================================================

def test_ex02(ex_dir, rep):
    header = "ft_abs.h"
    if not os.path.exists(os.path.join(ex_dir, header)):
        rep.record("ft_abs.h exists", "CORE", False,
                   "The subject requires an ABS(Value) macro.",
                   f"Create {ex_dir}/{header}.")
        return
    rep.record("ft_abs.h exists", "CORE", True, "The subject requires an ABS(Value) macro.")

    harness = """
#include "ft_abs.h"
#include <stdio.h>

int	g_calls;

int	side_effect(void)
{
	g_calls++;
	return (-4);
}

int	main(void)
{
	int		i;
	double	d;

	printf("0=%d\\n", ABS(5));
	printf("1=%d\\n", ABS(-5));
	printf("2=%d\\n", ABS(0));
	printf("3=%d\\n", ABS(2 - 5));
	printf("4=%d\\n", ABS(-2 - 5));
	i = -7;
	printf("5=%d\\n", ABS(i));
	d = -3.5;
	printf("6=%.1f\\n", ABS(d));
	printf("7=%d\\n", 10 + ABS(-3));
	i = ABS(side_effect());
	printf("8=%d,%d\\n", i, g_calls);
	return (0);
}
"""
    tmp_dir = tempfile.mkdtemp()
    try:
        copy_student_file(ex_dir, header, tmp_dir)
        res = compile_sources(tmp_dir, {"harness.c": harness})
        if res.returncode != 0:
            rep.record("ABS(Value) compiles", "CORE", False,
                       "A macro can still fail to compile (mismatched parens, stray semicolons).",
                       "Check the macro definition compiles standalone; count your parentheses.",
                       got=res.stderr.strip()[:400], expected="clean compile")
            return
        proc = run_bin(tmp_dir)
        if not proc:
            rep.record("ABS(Value) runs", "CORE", False, "Harness timed out.",
                       "Check for an infinite loop hidden inside the macro (unlikely, but check).")
            return
        values = {}
        for line in proc.stdout.strip().split("\n"):
            if "=" in line:
                k, v = line.split("=", 1)
                values[k] = v

        checks = [
            ("0", "5", "CORE", "ABS(5) = 5", "Positive input stays the same."),
            ("1", "5", "CORE", "ABS(-5) = 5", "Basic negative-to-positive flip."),
            ("2", "0", "CORE", "ABS(0) = 0", "Zero has no sign to flip."),
            ("5", "7", "CORE", "ABS(i) with i=-7, a variable rather than a literal",
             "Confirms the macro works on variables too, not just constant literals the "
             "compiler might fold at compile time."),
        ]
        for key, expected, cat, name, why in checks:
            got = values.get(key, "(missing)")
            rep.record(name, cat, got == expected, why,
                      "Check the sign-flip branch of your ternary (Value<0 ? -(Value) : (Value)).",
                      got=got, expected=expected)

        got3 = values.get("3", "(missing)")
        why3 = ("TRAP-class bug promoted to CORE because it's a hard requirement of a correct "
               "macro: ABS(2 - 5) must evaluate the WHOLE expression '2 - 5' first, then take its "
               "absolute value (|-3| = 3). If ABS(Value) expands 'Value' without wrapping it in "
               "its own parentheses, e.g. '#define ABS(Value) (Value < 0 ? -Value : Value)', this "
               "expands to '(2 - 5 < 0 ? -2 - 5 : 2 - 5)' -- operator precedence makes '-2 - 5' "
               "equal -7, not 3.")
        rep.record("ABS(2 - 5) == 3 (argument parenthesisation)", "CORE", got3 == "3", why3,
                  "Wrap every occurrence of Value in its own parentheses inside the macro body: "
                  "((Value) < 0 ? -(Value) : (Value)).", got=got3, expected="3")

        got4 = values.get("4", "(missing)")
        rep.record("ABS(-2 - 5) == 7 (same trap, different numbers)", "CORE", got4 == "7", why3,
                  "Same fix as above; this test exists to make sure the previous one wasn't a "
                  "coincidence.", got=got4, expected="7")

        got6 = values.get("6", "(missing)")
        rep.record("ABS(-3.5) == 3.5 (works generically on double, not just int)", "CORE",
                  got6 == "3.5",
                  "A macro (unlike a function) has no fixed parameter type, so ABS should work "
                  "for int, float or double alike -- that's the whole reason to implement this "
                  "as a macro instead of a typed function.",
                  "If you compare against a hardcoded '0' (int) inside the macro, that's fine "
                  "(0 promotes correctly), but make sure you're not casting Value to int anywhere.",
                  got=got6, expected="3.5")

        got7 = values.get("7", "(missing)")
        why7 = ("This is the OTHER classic macro trap, and it's arguably more important than the "
               "previous one: the entire macro expansion must be wrapped in its own outer "
               "parentheses too. '#define ABS(Value) (Value) < 0 ? -(Value) : (Value)' -- note, "
               "no parens around the whole ternary -- looks fine in isolation, but breaks the "
               "moment it's used inside a bigger expression. '10 + ABS(-3)' expands to "
               "'10 + (-3) < 0 ? -(-3) : (-3)', and because '+' binds tighter than the bare "
               "ternary here, this parses as '(10 + (-3)) < 0 ? 3 : -3' = (7 < 0) ? 3 : -3 = -3, "
               "not 13.")
        rep.record("10 + ABS(-3) == 13 (outer parenthesisation of the whole macro)", "CORE",
                  got7 == "13", why7,
                  "Wrap the ENTIRE macro body in one more set of parentheses: "
                  "'#define ABS(Value) (((Value) < 0) ? -(Value) : (Value))'.",
                  got=got7, expected="13")

        got8 = values.get("8", "0,0")
        try:
            abs_part, count_part = got8.split(",")
            count = int(count_part)
        except ValueError:
            abs_part, count = got8, -1
        why8 = ("TRAP, informational only: macros re-evaluate their argument every time it "
               "appears in the macro body. A typical ternary implementation mentions Value twice "
               "(once in the condition, once in the chosen branch), so an argument with a side "
               "effect -- like a function call that increments a counter -- runs twice, not once. "
               "This isn't something the subject asks you to prevent (it's a fundamental "
               "limitation of object-like/function-like macros in standard C), but it's worth "
               "knowing: never pass ABS(i++) or ABS(some_call_with_side_effects()) in real code.")
        hint8 = (f"Your side-effecting argument was evaluated {count} time(s). 1-2 is normal for "
                f"a plain macro and isn't a bug to fix; it's just something macros can't avoid "
                f"without non-standard tricks. Prefer a real function over a macro when the "
                f"argument might have side effects.")
        rep.record("Side-effect argument evaluation count (informational)", "TRAP",
                  count in (1, 2), why8, hint8, got=f"{count} call(s), abs={abs_part}",
                  expected="1-2 calls (inherent to macros, not a bug)")
    finally:
        shutil.rmtree(tmp_dir)


# ==========================================================================
#  EX03 : ft_point.h
# ==========================================================================

def test_ex03(ex_dir, rep):
    header = "ft_point.h"
    if not os.path.exists(os.path.join(ex_dir, header)):
        rep.record("ft_point.h exists", "CORE", False,
                   "The subject requires a t_point struct with x and y fields.",
                   f"Create {ex_dir}/{header}.")
        return
    rep.record("ft_point.h exists", "CORE", True,
               "The subject requires a t_point struct with x and y fields.")

    harness = """
#include "ft_point.h"
#include <stdio.h>

void	set_point(t_point *point)
{
	point->x = 42;
	point->y = 21;
}

int	main(void)
{
	t_point	point;

	set_point(&point);
	printf("0=%d,%d\\n", point.x, point.y);
	return (0);
}
"""
    tmp_dir = tempfile.mkdtemp()
    try:
        copy_student_file(ex_dir, header, tmp_dir)
        res = compile_sources(tmp_dir, {"harness.c": harness})
        why = ("This is the exact main() from the subject (with one added printf to actually "
              "verify the values, since the original just returns 0). t_point must have fields "
              "named exactly 'x' and 'y', accessible via '->' through a pointer.")
        hint = "Check your typedef is 'typedef struct { int x; int y; } t_point;' (field names matter)."
        compiled = res.returncode == 0
        rep.record("Compiles the exact subject-provided main()", "CORE", compiled, why, hint,
                  got=(res.stderr.strip()[:400] if not compiled else "compiled cleanly"),
                  expected="clean compile")
        if not compiled:
            return
        proc = run_bin(tmp_dir)
        got = proc.stdout.strip() if proc else "(timeout)"
        rep.record("set_point() correctly sets x=42, y=21", "CORE", got == "0=42,21",
                  "Directly checks the values the subject's own set_point() function assigns.",
                  "Make sure point->x and point->y are plain int fields (not, say, mixed up "
                  "or aliased).", got=got, expected="0=42,21")
    finally:
        shutil.rmtree(tmp_dir)

    # This one IS reliable (verified empirically): a struct typedef, tagged or
    # anonymous, always fails to recompile identically without a guard. So
    # unlike ft_boolean.h's t_bool, this is promoted to CORE.
    tmp_dir2 = tempfile.mkdtemp()
    try:
        copy_student_file(ex_dir, header, tmp_dir2)
        dbl = """
#include "ft_point.h"
#include "ft_point.h"

int	main(void)
{
	t_point	p;

	p.x = 1;
	p.y = 2;
	return ((p.x == 1 && p.y == 2) ? 0 : 1);
}
"""
        res2 = compile_sources(tmp_dir2, {"double_include.c": dbl}, out_name="dbl_runner")
        why = ("Includes ft_point.h twice in one file -- something that can genuinely happen via "
              "nested includes in a real project. Confirmed empirically: redefining the same "
              "struct typedef a second time (anonymous or tagged) is ALWAYS a hard compile error "
              "in C, regardless of how you wrote it -- unlike ft_boolean.h's t_bool, there's no "
              "implementation choice that dodges this. A missing header guard here is a real, "
              "reliable bug.")
        hint = "Wrap the whole file in '#ifndef FT_POINT_H' / '#define FT_POINT_H' / '#endif'."
        rep.record("Header guard: survives being #included twice", "CORE", res2.returncode == 0,
                  why, hint,
                  got=(res2.stderr.strip()[:300] if res2.returncode != 0 else "compiled cleanly"),
                  expected="clean compile")
    finally:
        shutil.rmtree(tmp_dir2)


# ==========================================================================
#  EX04 : ft_strs_to_tab.c
# ==========================================================================

def test_ex04(ex_dir, rep):
    src = "ft_strs_to_tab.c"
    if not os.path.exists(os.path.join(ex_dir, src)):
        rep.record(f"{src} exists", "CORE", False,
                   "The subject requires ft_strs_to_tab.c implementing struct s_stock_str "
                   "*ft_strs_to_tab(int ac, char **av).",
                   f"Create {ex_dir}/{src}.")
        return
    rep.record(f"{src} exists", "CORE", True,
              "The subject requires ft_strs_to_tab.c implementing the prototyped function.")

    forbidden = ["strdup", "strlen", "strcpy", "strncpy", "strcat", "memcpy", "sprintf",
                 "printf", "puts", "write", "calloc", "realloc"]
    found = grep_forbidden(ex_dir, src, forbidden, "malloc, free")
    why_forbidden = ("Subject: 'Allowed functions: malloc, free'. This is a text-based scan (not "
                    "a real parser, so it can rarely misfire on comments/strings) for common "
                    "standard-library calls outside that list -- notably strlen()/strdup()/"
                    "strcpy(), which are exactly the functions this exercise expects you to "
                    "reimplement by hand instead of calling.")
    hint_forbidden = (f"Found calls to: {', '.join(found)}. Per the subject's own rules, using a "
                      f"forbidden function is treated as cheating (grade -42, non-negotiable). "
                      f"Replace these with your own hand-written loops.") if found else None
    rep.record("Only uses allowed functions (malloc, free)", "CORE", not found, why_forbidden,
              hint_forbidden, got=(found if found else "none found"), expected="none")

    harness = """
#include "ft_stock_str.h"
#include <stdio.h>
#include <string.h>

t_stock_str	*ft_strs_to_tab(int ac, char **av);

int	main(void)
{
	char		*av1[3];
	t_stock_str	*tab1;
	t_stock_str	*tab0;
	int			i;

	av1[0] = "Hello";
	av1[1] = "World!";
	av1[2] = "";

	tab1 = ft_strs_to_tab(3, av1);
	if (!tab1)
	{
		printf("FATAL=NULL\\n");
		return (0);
	}
	i = 0;
	while (i < 3)
	{
		printf("str%d=%s\\n", i, tab1[i].str ? tab1[i].str : "(null)");
		printf("size%d=%d\\n", i, tab1[i].size);
		printf("copy%d=%s\\n", i, tab1[i].copy ? tab1[i].copy : "(null)");
		printf("diff%d=%d\\n", i, (tab1[i].copy != tab1[i].str) ? 1 : 0);
		i++;
	}
	printf("sentinel=%s\\n", tab1[3].str ? "NOTNULL" : "NULL");

	tab0 = ft_strs_to_tab(0, av1);
	if (!tab0)
		printf("ac0=NULLRETURN\\n");
	else
		printf("ac0=%s\\n", tab0[0].str ? "NOTNULL" : "NULL");
	return (0);
}
"""
    tmp_dir = tempfile.mkdtemp()
    try:
        copy_student_file(ex_dir, src, tmp_dir)
        res = compile_sources(tmp_dir, {"harness.c": harness, "ft_stock_str.h": STOCK_STR_H, src: open(os.path.join(ex_dir, src)).read()})
        if res.returncode != 0:
            rep.record("Compiles against the subject's t_stock_str layout", "CORE", False,
                      "The struct is supplied by us here exactly as the subject defines it "
                      "(int size; char *str; char *copy;) -- your function must build/return "
                      "this type as-is.",
                      "Check your #include \"ft_stock_str.h\" and field usage match exactly.",
                      got=res.stderr.strip()[:500], expected="clean compile")
            return
        rep.record("Compiles against the subject's t_stock_str layout", "CORE", True,
                  "Sanity check before behavioural tests.")
        proc = run_bin(tmp_dir)
        if not proc:
            rep.record("ft_strs_to_tab runs without hanging", "CORE", False,
                      "Timed out.", "Check for an infinite loop, e.g. a copy loop missing its "
                      "null-terminator check.")
            return
        vals = {}
        for line in proc.stdout.strip().split("\n"):
            if "=" in line:
                k, v = line.split("=", 1)
                vals[k] = v

        if vals.get("FATAL") == "NULL":
            rep.record("Returns a non-NULL array for valid input", "CORE", False,
                      "Subject: NULL should only be returned 'if an error occurs'; this is 3 "
                      "perfectly valid strings, not an error case.",
                      "Check your malloc calls aren't failing or being mis-sized.",
                      got="NULL", expected="a valid pointer")
            return

        av_orig = ["Hello", "World!", ""]
        str_ok = all(vals.get(f"str{i}") == av_orig[i] for i in range(3))
        rep.record("str field matches original strings, in order", "CORE", str_ok,
                  "Subject: 'It should keep the order of av' and 'str being the string'.",
                  "Double check you're iterating av in order and not swapping/skipping elements.",
                  got=[vals.get(f"str{i}") for i in range(3)], expected=av_orig)

        size_ok = vals.get("size0") == "5" and vals.get("size1") == "6" and vals.get("size2") == "0"
        rep.record("size field matches each string's real length", "CORE", size_ok,
                  "Subject: 'size being the length of the string' -- including the length-0 "
                  "empty-string edge case.",
                  "Recheck your length-counting loop, especially for the empty string (size2).",
                  got=[vals.get(f"size{i}") for i in range(3)], expected=["5", "6", "0"])

        copy_ok = all(vals.get(f"copy{i}") == av_orig[i] for i in range(3))
        rep.record("copy field contains the same text as the original string", "CORE", copy_ok,
                  "Subject: 'copy being a copy of the string' -- the content must match.",
                  "Check your copy loop writes the same characters (and null-terminates).",
                  got=[vals.get(f"copy{i}") for i in range(3)], expected=av_orig)

        diff_ok = all(vals.get(f"diff{i}") == "1" for i in range(3))
        rep.record("copy is a genuinely separate allocation from str (not the same pointer)",
                  "CORE", diff_ok,
                  "The subject lists 'str' and 'copy' as two distinct fields on purpose -- copy "
                  "must be its own malloc'd buffer, not just str assigned to both fields.",
                  "If this fails, you likely wrote 'tab[i].copy = tab[i].str;' (or similar) "
                  "instead of allocating a fresh buffer and copying characters into it.",
                  got=[vals.get(f"diff{i}") for i in range(3)], expected=["1", "1", "1"])

        sentinel_ok = vals.get("sentinel") == "NULL"
        rep.record("Last element's str is set to 0 (sentinel)", "CORE", sentinel_ok,
                  "Subject: 'its last element's str set to 0, this will mark the end of the "
                  "array' -- this is how ft_show_tab (and moulinette) knows where the array ends.",
                  "Make sure you allocate ac+1 elements and explicitly set tab[ac].str = 0.",
                  got=vals.get("sentinel"), expected="NULL")

        ac0 = vals.get("ac0", "(missing)")
        ac0_ok = ac0 in ("NULLRETURN", "NULL")
        rep.record("ac=0 edge case behaves sanely (informational)", "TRAP", ac0_ok,
                  "TRAP: the subject doesn't explicitly define behaviour for ac=0. Returning NULL "
                  "or returning an allocated array containing only the sentinel are both "
                  "defensible readings -- this just checks you handled it deliberately rather "
                  "than crashing or reading uninitialised memory.",
                  "Either returning NULL for ac=0, or an array of just {str=0}, is reasonable; "
                  "just make sure it's intentional, not an accident of undefined behaviour.",
                  got=ac0, expected="NULLRETURN or NULL (either is fine)")
    finally:
        shutil.rmtree(tmp_dir)

    # TRAP: larger input, just a robustness/perf sanity check.
    tmp_dir2 = tempfile.mkdtemp()
    try:
        copy_student_file(ex_dir, src, tmp_dir2)
        stress = """
#include "ft_stock_str.h"
#include <stdio.h>

t_stock_str	*ft_strs_to_tab(int ac, char **av);

int	main(void)
{
	char	*av[200];
	int		i;
	t_stock_str	*tab;

	i = 0;
	while (i < 200)
	{
		av[i] = "stress_test_string";
		i++;
	}
	tab = ft_strs_to_tab(200, av);
	printf("%s\\n", tab ? "OK" : "NULL");
	return (0);
}
"""
        res2 = compile_sources(tmp_dir2, {"stress.c": stress, "ft_stock_str.h": STOCK_STR_H, src: open(os.path.join(ex_dir, src)).read()}, out_name="stress_runner")
        if res2.returncode != 0:
            rep.record("Handles 200 strings without crashing (stress test)", "TRAP", False,
                      "TRAP: not a subject requirement, just a robustness sanity check with a "
                      "larger ac than the hand-written examples above.",
                      "Compile error on the stress harness -- unusual, check for name clashes.",
                      got=res2.stderr.strip()[:300], expected="clean compile")
        else:
            proc2 = run_bin(tmp_dir2, out_name="stress_runner", timeout=5)
            ok = proc2 is not None and proc2.returncode == 0 and "OK" in proc2.stdout
            rep.record("Handles 200 strings without crashing (stress test)", "TRAP", ok,
                      "TRAP: not a subject requirement, just a robustness sanity check with a "
                      "larger ac than the hand-written examples above.",
                      "A crash here usually means a fixed-size buffer somewhere, or an "
                      "off-by-one in the allocation size for the array itself (should be ac+1).",
                      got=(proc2.stdout.strip() if proc2 else "crash/timeout"), expected="OK")
    finally:
        shutil.rmtree(tmp_dir2)


# ==========================================================================
#  EX05 : ft_show_tab.c
# ==========================================================================

def capture_show_tab_output(tmp_dir, extra_sources_c, extra_sources_content):
    """Builds and runs a harness that calls ft_show_tab (from wherever it's
    linked from) on a hand-built array, capturing raw stdout bytes via a
    temp-file redirect around just the call."""
    harness = """
#include "ft_stock_str.h"
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

void	ft_show_tab(t_stock_str *par);

int	main(void)
{
	t_stock_str	arr[5];
	int			stdout_backup;
	char		tmp_path[] = "/tmp/showtab_out_XXXXXX";
	int			fd;
	FILE		*f;
	static char	buf[8192];
	size_t		n;

	arr[0].str = "Hello"; arr[0].size = 5; arr[0].copy = "Hello";
	arr[1].str = "World!"; arr[1].size = 6; arr[1].copy = "WORLD!";
	arr[2].str = ""; arr[2].size = 0; arr[2].copy = "";
	arr[3].str = "BigSize"; arr[3].size = 12345; arr[3].copy = "BigSize";
	arr[4].str = 0; arr[4].size = 0; arr[4].copy = 0;

	fd = mkstemp(tmp_path);
	fflush(stdout);
	stdout_backup = dup(1);
	dup2(fd, 1);
	close(fd);

	ft_show_tab(arr);

	fflush(stdout);
	dup2(stdout_backup, 1);
	close(stdout_backup);

	f = fopen(tmp_path, "r");
	n = 0;
	if (f)
	{
		n = fread(buf, 1, sizeof(buf) - 1, f);
		fclose(f);
	}
	unlink(tmp_path);

	printf("LEN=%zu\\n", n);
	printf("RAW_START\\n");
	fwrite(buf, 1, n, stdout);
	printf("RAW_END\\n");
	return (0);
}
"""
    files = {"harness.c": harness, "ft_stock_str.h": STOCK_STR_H}
    files.update(extra_sources_content)
    res = compile_sources(tmp_dir, files, out_name="test_runner")
    if res.returncode != 0:
        return None, res.stderr.strip()
    proc = run_bin(tmp_dir, out_name="test_runner")
    if not proc:
        return None, "(timeout)"
    out = proc.stdout
    try:
        len_line, rest = out.split("\n", 1)
        n = int(len_line.split("=", 1)[1])
        start = rest.index("RAW_START\n") + len("RAW_START\n")
        raw = rest[start:start + n]
        return raw, None
    except Exception as e:
        return None, f"parse error: {e}, raw stdout: {out[:300]!r}"


def test_ex05(ex_dir, rep):
    src = "ft_show_tab.c"
    if not os.path.exists(os.path.join(ex_dir, src)):
        rep.record(f"{src} exists", "CORE", False,
                  "The subject requires ft_show_tab.c implementing void ft_show_tab(struct "
                  "s_stock_str *par).",
                  f"Create {ex_dir}/{src}.")
        return
    rep.record(f"{src} exists", "CORE", True,
              "The subject requires ft_show_tab.c implementing the prototyped function.")

    forbidden = ["printf", "fprintf", "sprintf", "puts", "putchar", "strlen", "itoa"]
    found = grep_forbidden(ex_dir, src, forbidden, "write")
    why_forbidden = ("Subject: 'Allowed functions: write'. Text-based scan for common standard "
                    "library output/length helpers outside that list -- notably printf() (the "
                    "obvious shortcut) and itoa() for converting the integer size field to text, "
                    "both of which this exercise expects you to avoid in favour of write() plus "
                    "your own manual int-to-string conversion.")
    hint_forbidden = (f"Found calls to: {', '.join(found)}. Per the subject's rules this is "
                      f"treated as cheating (grade -42). Replace with write() and a hand-written "
                      f"integer-to-ASCII conversion for the size field.") if found else None
    rep.record("Only uses the allowed function (write)", "CORE", not found, why_forbidden,
              hint_forbidden, got=(found if found else "none found"), expected="none")

    tmp_dir = tempfile.mkdtemp()
    try:
        student_src_content = open(os.path.join(ex_dir, src)).read()
        raw, err = capture_show_tab_output(tmp_dir, [], {src: student_src_content})
        if raw is None:
            rep.record("Compiles and runs ft_show_tab", "CORE", False,
                      "Sanity check before checking exact output.",
                      "See the compiler/runtime error for details.", got=err,
                      expected="clean compile and run")
            return
        rep.record("Compiles and runs ft_show_tab", "CORE", True, "Sanity check passed.")

        expected = "Hello\n5\nHello\n" + "World!\n6\nWORLD!\n" + "\n0\n\n" + "BigSize\n12345\nBigSize\n"
        why = ("Builds a 4-element array + sentinel by hand and checks the EXACT byte output "
              "against the subject's spec: 'the string, then \\n, the size, then \\n, the copy, "
              "then \\n' per element, nothing else. This single test packs in a lot: (1) correct "
              "field order, (2) correct manual int-to-string conversion including a MULTI-DIGIT "
              "size (12345) -- catches implementations that only handle single digits, (3) "
              "correct handling of an empty string (size 0), (4) that 'copy' is printed (not "
              "'str' printed twice -- element 1's copy deliberately differs in case: 'WORLD!' vs "
              "'World!'), and (5) that the loop stops exactly at the sentinel and prints nothing "
              "extra or garbage afterwards.")
        hint = ("Compare your raw output to the expected string character by character. A wrong "
               "digit conversion, a missing newline, printing str twice instead of str-then-copy, "
               "or not stopping at the sentinel will all show up here as a mismatch -- check which "
               "part of the expected string first diverges from what you printed.")
        rep.record("Exact byte-for-byte output matches the spec", "CORE", raw == expected, why, hint,
                  got=repr(raw), expected=repr(expected))
    finally:
        shutil.rmtree(tmp_dir)


# ==========================================================================
#  INTEGRATION: ex04 + ex05 together, exactly as the subject describes
# ==========================================================================

def test_integration(base_dir, rep):
    ex04_file = os.path.join("ex04", "ft_strs_to_tab.c")
    ex05_file = os.path.join("ex05", "ft_show_tab.c")
    if not (os.path.exists(ex04_file) and os.path.exists(ex05_file)):
        print(f"{C_DIM}(skipping ex04+ex05 integration check -- one of the two files is missing){C_RESET}")
        return

    tmp_dir = tempfile.mkdtemp()
    try:
        strs_to_tab_content = open(ex04_file).read()
        show_tab_content = open(ex05_file).read()
        harness = """
#include "ft_stock_str.h"
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

t_stock_str	*ft_strs_to_tab(int ac, char **av);
void		ft_show_tab(t_stock_str *par);

int	main(void)
{
	char		*av[3];
	t_stock_str	*tab;
	int			stdout_backup;
	char		tmp_path[] = "/tmp/integ_out_XXXXXX";
	int			fd;
	FILE		*f;
	static char	buf[8192];
	size_t		n;

	av[0] = "foo";
	av[1] = "bar";
	av[2] = "bazqux";

	tab = ft_strs_to_tab(3, av);
	if (!tab)
	{
		printf("NULL_RETURNED\\n");
		return (0);
	}

	fd = mkstemp(tmp_path);
	fflush(stdout);
	stdout_backup = dup(1);
	dup2(fd, 1);	close(fd);

	ft_show_tab(tab);

	fflush(stdout);
	dup2(stdout_backup, 1);
	close(stdout_backup);

	f = fopen(tmp_path, "r");
	n = 0;
	if (f)
	{
		n = fread(buf, 1, sizeof(buf) - 1, f);
		fclose(f);
	}
	unlink(tmp_path);

	printf("LEN=%zu\\n", n);
	printf("RAW_START\\n");
	fwrite(buf, 1, n, stdout);
	printf("RAW_END\\n");
	return (0);
}
"""
        files = {
            "harness.c": harness,
            "ft_stock_str.h": STOCK_STR_H,
            "ft_strs_to_tab.c": strs_to_tab_content,
            "ft_show_tab.c": show_tab_content,
        }
        res = compile_sources(tmp_dir, files)
        why = ("The subject explicitly says: \"We'll test your function with our ft_show_tab / "
              "ft_strs_to_tab. Make it work according to this!\" -- meaning the real grading "
              "wires YOUR ex04 output directly into (a reference) ft_show_tab, and vice-versa. "
              "This test does exactly that with your own two files: builds a table with "
              "ft_strs_to_tab(3, {\"foo\",\"bar\",\"bazqux\"}) and feeds the result straight "
              "into ft_show_tab, checking the final printed output end-to-end.")
        if res.returncode != 0:
            rep.record("ex04 + ex05 compile together", "CORE", False, why,
                      "A conflict between your two files (e.g. both defining a helper with the "
                      "same name) will show up here even if each file compiles fine alone.",
                      got=res.stderr.strip()[:500], expected="clean compile")
            return
        proc = run_bin(tmp_dir)
        out = proc.stdout if proc else "(timeout)"
        try:
            len_line, rest = out.split("\n", 1)
            n = int(len_line.split("=", 1)[1])
            start = rest.index("RAW_START\n") + len("RAW_START\n")
            raw = rest[start:start + n]
        except Exception:
            raw = out

        expected = "foo\n3\nfoo\n" + "bar\n3\nbar\n" + "bazqux\n6\nbazqux\n"
        rep.record("ft_strs_to_tab(3, av) -> ft_show_tab(...) end-to-end output", "CORE",
                  raw == expected, why,
                  "If ex04 and ex05 each pass their own standalone tests above but this fails, "
                  "the bug is specifically in how the two interact -- e.g. the sentinel isn't "
                  "where ft_show_tab expects it, or a field got mixed up between the two files' "
                  "assumptions about the struct.",
                  got=repr(raw), expected=repr(expected))
    finally:
        shutil.rmtree(tmp_dir)


# ==========================================================================
#  MAIN
# ==========================================================================

EXERCISES = {
    "ex00": test_ex00,
    "ex01": test_ex01,
    "ex02": test_ex02,
    "ex03": test_ex03,
    "ex04": test_ex04,
    "ex05": test_ex05,
}


def main():
    print(f"{C_WHITE}{C_BOLD}=========================================================")
    print("        42 PISCINE C08 - ADVERSARIAL / VERBOSE TESTER    ")
    print("=========================================================")
    print(f"{C_RESET}{C_DIM}CORE  = tests a rule stated in the subject; counts toward score/rank.")
    print(f"TRAP  = adversarial edge case (header guards, macro hygiene, robustness);")
    print(f"        informational only, never affects score.{C_RESET}")
    print(f"{C_DIM}Note: ex00-ex03 are header-only exercises, so most of what's testable here")
    print(f"is exact prototype/struct/macro correctness and compiling the subject's own")
    print(f"example code verbatim -- there's no student *logic* to fuzz in a bare header.{C_RESET}")

    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    sorted_exercises = sorted(EXERCISES.keys())
    run_integration = True
    if args:
        sorted_exercises = [a for a in sorted_exercises if a in args]
        run_integration = "ex04" in args and "ex05" in args if args else True
        if not sorted_exercises:
            print_fail(f"No matching exercises for: {args}")
            return

    results = []
    for ex in sorted_exercises:
        print(f"\n{C_CYAN}{C_BOLD}============ Evaluating {ex} ============{C_RESET}")
        rep = Reporter()
        if not os.path.exists(ex):
            print_fail(f"Turn-in directory '{ex}' missing.")
            results.append((ex, 0, "F", 0, (0, 0)))
            continue
        EXERCISES[ex](ex, rep)
        score = rep.score()
        rank = calculate_rank(score)
        results.append((ex, score, rank, rep.core_total, (rep.trap_pass, rep.trap_total)))

    if run_integration:
        print(f"\n{C_CYAN}{C_BOLD}============ Evaluating ex04 + ex05 (integration) ============{C_RESET}")
        rep_i = Reporter()
        test_integration(".", rep_i)
        if rep_i.core_total > 0:
            score_i = rep_i.score()
            results.append(("integration", score_i, calculate_rank(score_i), rep_i.core_total, (rep_i.trap_pass, rep_i.trap_total)))

    print(f"\n{C_WHITE}{C_BOLD}+-------------------------------------------------------+")
    print("|                   FINAL SCOREBOARD                     |")
    print(f"+-------------------------------------------------------+{C_RESET}")
    print(f"| {'Exercise':<12} | {'CORE score':<12} | {'Rank':<6} | {'Trap insights':<14}|")
    print("+--------------+--------------+--------+----------------+")
    for ex, score, rank, core_total, (tpass, ttotal) in results:
        c_status = C_GREEN if rank in ["S", "A"] else (C_YELLOW if rank in ["B", "C"] else C_RED)
        trap_str = f"{tpass}/{ttotal}" if ttotal else "n/a"
        trap_color = C_GREEN if (ttotal == 0 or tpass == ttotal) else C_MAGENTA
        print(f"| {ex:<12} | {score:>3}/100      | {c_status}{rank:<6}{C_RESET} | {trap_color}{trap_str:<14}{C_RESET} |")
    print("+--------------+--------------+--------+----------------+")
    print(f"{C_DIM}Rank is computed from CORE tests only (the rules the subject actually states).")
    print(f"Trap insights are adversarial bonus checks; a low trap score is a learning signal,")
    print(f"not a grading penalty -- read the [TRAP] failure messages above for what to fix.{C_RESET}")


if __name__ == "__main__":
    main()
