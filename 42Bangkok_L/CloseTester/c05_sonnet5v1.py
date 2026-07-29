#!/usr/bin/env python3
"""
42 Piscine - C05 Adversarial Tester
-----------------------------------
Design goals (matching the style used for the c02/c03/c04 testers):

  * Every test carries a CATEGORY:
      - CORE : directly checks a rule stated in the subject. Moulinette-relevant.
               These are the only tests that count towards the score/rank.
      - TRAP : an adversarial/edge test that is NOT explicitly graded by the
               subject, but exposes classic implementation bugs (signed
               overflow on INT_MIN negation, unguarded loops on negative
               bounds, missing overflow guards, exponential blow-up, etc).
               TRAP failures are reported separately as "insights" and never
               hurt the score, but they explain a real bug class if hit.

  * Every test carries a WHY (why we bother testing this at all) and, on
    failure, a HINT (a concrete, actionable pointer towards the likely bug).

  * -v / --verbose prints the WHY for every test (even passing ones), so you
    can see the full reasoning of the suite, not just pass/fail.

Usage:
    python3 c05_tester.py            # normal run
    python3 c05_tester.py -v         # verbose: show rationale for every test
    python3 c05_tester.py ex05       # only run a specific exercise
"""

import os
import sys
import subprocess
import tempfile
import shutil

US = "\x1f"  # unit separator, used as the field delimiter in harness output

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

# ==========================================================================
#  HARNESSES
# ==========================================================================
# Each harness is a self-contained C program. It exposes two modes:
#   argv[1] == "list"   -> prints "id|CATEGORY|Name" for every test, one per line
#   argv[1] == "<id>"   -> runs test <id> and prints a single RESULT line:
#        RESULT<US>name<US>category<US>PASS/FAIL<US>got<US>expected<US>inputs<US>why<US>hint
#
# Field separator is \x1f (unit separator) rather than '|' so that hint/why
# text can freely contain punctuation without breaking the parser.

HARNESSES = {}

# --------------------------------------------------------------------------
# ex00 : ft_iterative_factorial
# --------------------------------------------------------------------------
HARNESSES["ex00"] = ("ft_iterative_factorial.c", r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

int ft_iterative_factorial(int nb);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Negative input (-5)",                 "CORE"},
    {"Boundary just below zero (-1)",       "CORE"},
    {"Zero input (0)",                      "CORE"},
    {"One input (1)",                       "CORE"},
    {"First non-trivial case (2)",          "CORE"},
    {"Standard case (5)",                   "CORE"},
    {"Larger case (10)",                    "CORE"},
    {"Max safe int32 value (12)",           "CORE"},
    {"INT_MIN boundary",                    "TRAP"},
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
    int res, exp;
    const char *why, *hint, *inputs;
    if (id == 0) {
        res = ft_iterative_factorial(-5); exp = 0; inputs = "nb=-5";
        why = "Subject: 'if the argument is not valid, the function should return 0'. Negative numbers have no factorial.";
        hint = "Make sure the negativity check actually returns 0 instead of falling through into the loop.";
    } else if (id == 1) {
        res = ft_iterative_factorial(-1); exp = 0; inputs = "nb=-1";
        why = "Tests the exact edge of the valid domain to catch off-by-one mistakes in the guard (e.g. 'nb <= 0' vs 'nb < 0').";
        hint = "If this fails but -5 passed, your negativity check is likely off by one (check < vs <=).";
    } else if (id == 2) {
        res = ft_iterative_factorial(0); exp = 1; inputs = "nb=0";
        why = "0! is a mathematical special case defined as 1, not a product of nothing that defaults to 0.";
        hint = "Your accumulator should be initialised to 1, not 0, before the multiplication loop.";
    } else if (id == 3) {
        res = ft_iterative_factorial(1); exp = 1; inputs = "nb=1";
        why = "1! = 1 is the smallest non-special-case input; checks the loop can run for exactly zero real iterations.";
        hint = "Check your loop bounds: a loop starting at 2 and going up to nb should simply never execute when nb=1.";
    } else if (id == 4) {
        res = ft_iterative_factorial(2); exp = 2; inputs = "nb=2";
        why = "First value where the multiplication loop must actually run at least once; catches a wrong starting index (e.g. starting at 0 or 1 and multiplying by it).";
        hint = "If you get 0 or 1 here, your loop is probably starting the accumulator multiplication at the wrong index.";
    } else if (id == 5) {
        res = ft_iterative_factorial(5); exp = 120; inputs = "nb=5";
        why = "Standard mid-range value, the one everybody checks by hand.";
        hint = "Re-trace the loop by hand for nb=5 and compare each intermediate product.";
    } else if (id == 6) {
        res = ft_iterative_factorial(10); exp = 3628800; inputs = "nb=10";
        why = "Slightly larger input to catch accumulation bugs that only surface after several iterations (e.g. wrong loop increment).";
        hint = "Compare your intermediate accumulator values against 1,2,6,24,120,720,... step by step.";
    } else if (id == 7) {
        res = ft_iterative_factorial(12); exp = 479001600; inputs = "nb=12";
        why = "12! = 479001600 is the largest factorial that fits in a signed 32-bit int (13! overflows). Confirms the full valid range works, not just small inputs.";
        hint = "If smaller values pass but this fails, look for premature truncation or a loop bound that stops one iteration early.";
    } else if (id == 8) {
        res = ft_iterative_factorial(INT_MIN); exp = 0; inputs = "nb=INT_MIN";
        why = "TRAP: checks that the negativity guard is a simple comparison and never negates nb. Negating INT_MIN (e.g. 'if (nb<0) nb=-nb;') is signed integer overflow: undefined behaviour in C.";
        hint = "This mirrors the INT_MIN negation bug found earlier in C04's ft_atoi_base. Never write '-nb' before you know nb isn't INT_MIN; just compare and return 0 directly.";
    } else {
        return 1;
    }
    printf("RESULT" US "%s" US "%s" US "%s" US "%d" US "%d" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, res == exp ? "PASS" : "FAIL", res, exp, inputs, why, hint);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex01 : ft_recursive_factorial
# --------------------------------------------------------------------------
HARNESSES["ex01"] = ("ft_recursive_factorial.c", r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

int ft_recursive_factorial(int nb);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Negative input (-10)",                "CORE"},
    {"Boundary just below zero (-1)",       "CORE"},
    {"Zero input (0) - base case",          "CORE"},
    {"One input (1) - base case",           "CORE"},
    {"First non-trivial case (2)",          "CORE"},
    {"Standard case (6)",                   "CORE"},
    {"Larger case (10)",                    "CORE"},
    {"Max safe int32 value (12)",           "CORE"},
    {"INT_MIN boundary",                    "TRAP"},
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
    int res, exp;
    const char *why, *hint, *inputs;
    if (id == 0) {
        res = ft_recursive_factorial(-10); exp = 0; inputs = "nb=-10";
        why = "Recursive version must apply the same 'invalid argument -> 0' rule as the iterative one before recursing.";
        hint = "The guard for nb<0 must be checked before any recursive call, or you'll recurse forever downward.";
    } else if (id == 1) {
        res = ft_recursive_factorial(-1); exp = 0; inputs = "nb=-1";
        why = "Exact edge of the valid domain; catches an off-by-one guard (e.g. checking 'nb < -1' instead of 'nb < 0').";
        hint = "Double check the comparison operator in your base/guard case.";
    } else if (id == 2) {
        res = ft_recursive_factorial(0); exp = 1; inputs = "nb=0";
        why = "0! = 1 is very often the recursion's base case; if it's wrong, every other call built on top of it is wrong too.";
        hint = "Make sure your base case explicitly returns 1 for nb==0 (or nb<=1), not 0.";
    } else if (id == 3) {
        res = ft_recursive_factorial(1); exp = 1; inputs = "nb=1";
        why = "Second common base case; some implementations only special-case 0 and mishandle 1.";
        hint = "If 0 passes but 1 fails, you likely need nb<=1 (not just nb==0) as your base case, or one extra recursive step is off.";
    } else if (id == 4) {
        res = ft_recursive_factorial(2); exp = 2; inputs = "nb=2";
        why = "First value that actually requires one real recursive multiplication; catches an inverted recursive formula.";
        hint = "Trace nb=2: it should compute 2 * ft_recursive_factorial(1). Check the multiplication isn't swapped or off by one call.";
    } else if (id == 5) {
        res = ft_recursive_factorial(6); exp = 720; inputs = "nb=6";
        why = "Standard mid-range value to validate the general recursive case, not just the base cases.";
        hint = "Recompute 6*5*4*3*2*1 and compare against each recursion level if you have debug prints.";
    } else if (id == 6) {
        res = ft_recursive_factorial(10); exp = 3628800; inputs = "nb=10";
        why = "Deeper recursion depth (10 stack frames) to catch bugs that only appear after several recursive steps.";
        hint = "If this fails while 6 passes, look for an accumulation error that compounds over more calls.";
    } else if (id == 7) {
        res = ft_recursive_factorial(12); exp = 479001600; inputs = "nb=12";
        why = "12! is the largest factorial that fits a 32-bit signed int; confirms correctness across the whole valid range.";
        hint = "Check for premature truncation or an off-by-one recursion depth near the top of the valid range.";
    } else if (id == 8) {
        res = ft_recursive_factorial(INT_MIN); exp = 0; inputs = "nb=INT_MIN";
        why = "TRAP: same INT_MIN negation-overflow class as ex00. A guard like 'if (nb<0) nb=-nb;' before recursing is undefined behaviour on INT_MIN.";
        hint = "Never negate nb to 'normalize' it; just compare nb<0 directly and return 0 immediately, with no recursive call at all.";
    } else {
        return 1;
    }
    printf("RESULT" US "%s" US "%s" US "%s" US "%d" US "%d" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, res == exp ? "PASS" : "FAIL", res, exp, inputs, why, hint);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex02 : ft_iterative_power
# --------------------------------------------------------------------------
HARNESSES["ex02"] = ("ft_iterative_power.c", r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

int ft_iterative_power(int nb, int power);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Negative power",                      "CORE"},
    {"Zero power (0^0)",                    "CORE"},
    {"Standard zero power (5^0)",           "CORE"},
    {"Standard usage (2^10)",               "CORE"},
    {"Standard usage (3^4)",                "CORE"},
    {"Negative base, odd power (-3^3)",     "CORE"},
    {"Negative base, even power (-2^4)",    "CORE"},
    {"Zero base, negative power (0^-1)",    "CORE"},
    {"Extreme negative power (INT_MIN)",    "TRAP"},
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
    int res, exp;
    const char *why, *hint, *inputs;
    if (id == 0) {
        res = ft_iterative_power(2, -3); exp = 0; inputs = "nb=2 power=-3";
        why = "Subject: 'if the power is less than 0, the function should return 0'.";
        hint = "Check that the power<0 guard runs before entering the multiplication loop.";
    } else if (id == 1) {
        res = ft_iterative_power(0, 0); exp = 1; inputs = "nb=0 power=0";
        why = "Subject explicitly states 0^0 must return 1 by definition, overriding the usual mathematical ambiguity.";
        hint = "Your loop-based implementation should naturally return 1 here if the accumulator starts at 1 and the loop runs 0 times; if it doesn't, check for a special-cased nb==0 branch that fires too early.";
    } else if (id == 2) {
        res = ft_iterative_power(5, 0); exp = 1; inputs = "nb=5 power=0";
        why = "Any nonzero number to the power 0 is 1; validates the loop correctly runs zero iterations.";
        hint = "Make sure the accumulator is initialised to 1 before the loop, not to nb.";
    } else if (id == 3) {
        res = ft_iterative_power(2, 10); exp = 1024; inputs = "nb=2 power=10";
        why = "Standard positive case with enough iterations to catch a loop-count off-by-one (e.g. running 9 or 11 times instead of 10).";
        hint = "Check whether your loop condition is 'i < power' or 'i <= power' -- only one is correct.";
    } else if (id == 4) {
        res = ft_iterative_power(3, 4); exp = 81; inputs = "nb=3 power=4";
        why = "Second standard case with a different base, to rule out a bug that only happens to cancel out for base 2.";
        hint = "Recompute 3*3*3*3 by hand and compare intermediate products.";
    } else if (id == 5) {
        res = ft_iterative_power(-3, 3); exp = -27; inputs = "nb=-3 power=3";
        why = "Negative base with an odd exponent must keep the negative sign; catches implementations that only ever return abs(nb)^power.";
        hint = "If you get +27 instead of -27, you're likely using abs(nb) somewhere, or unsigned intermediate storage.";
    } else if (id == 6) {
        res = ft_iterative_power(-2, 4); exp = 16; inputs = "nb=-2 power=4";
        why = "Negative base with an even exponent must produce a positive result; combined with the previous test this fully validates sign handling.";
        hint = "If you get -16 here, your sign logic is inverted (e.g. always flipping the sign instead of only for odd exponents).";
    } else if (id == 7) {
        res = ft_iterative_power(0, -1); exp = 0; inputs = "nb=0 power=-1";
        why = "Combines two rules at once: base 0 (which tempts a special-case branch) with a negative power (which must return 0 regardless of the base).";
        hint = "If a special-case for nb==0 runs before the power<0 check, this can slip through with the wrong value. The power<0 rule must be checked first, unconditionally.";
    } else if (id == 8) {
        res = ft_iterative_power(2, INT_MIN); exp = 0; inputs = "nb=2 power=INT_MIN";
        why = "TRAP: if the power<0 guard is missing or is placed after some loop setup that still executes, using INT_MIN as a loop bound could mean iterating ~2^31 times instead of returning immediately.";
        hint = "This must return instantly. If the tester seems to hang/timeout on this case, your power<0 check either doesn't exist or runs too late.";
    } else {
        return 1;
    }
    printf("RESULT" US "%s" US "%s" US "%s" US "%d" US "%d" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, res == exp ? "PASS" : "FAIL", res, exp, inputs, why, hint);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex03 : ft_recursive_power
# --------------------------------------------------------------------------
HARNESSES["ex03"] = ("ft_recursive_power.c", r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

int ft_recursive_power(int nb, int power);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Negative power",                      "CORE"},
    {"Zero power (0^0)",                    "CORE"},
    {"Standard zero power (3^0)",           "CORE"},
    {"Standard usage (5^3)",                "CORE"},
    {"Standard usage (2^8)",                "CORE"},
    {"Negative base, odd power (-2^5)",     "CORE"},
    {"Negative base, even power (-2^4)",    "CORE"},
    {"Zero base, negative power (0^-1)",    "CORE"},
    {"Deep recursion depth (1^200000)",     "TRAP"},
    {"Extreme negative power (INT_MIN)",    "TRAP"},
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
    int res, exp;
    const char *why, *hint, *inputs;
    if (id == 0) {
        res = ft_recursive_power(5, -1); exp = 0; inputs = "nb=5 power=-1";
        why = "Subject: negative power must return 0. Must be checked before any recursive call is made.";
        hint = "Put the power<0 guard as the very first check, before recursing.";
    } else if (id == 1) {
        res = ft_recursive_power(0, 0); exp = 1; inputs = "nb=0 power=0";
        why = "0^0 must return 1 by definition; this is usually the recursion's base case (power==0).";
        hint = "Your base case 'if (power == 0) return 1;' must fire before any nb==0 special case does.";
    } else if (id == 2) {
        res = ft_recursive_power(3, 0); exp = 1; inputs = "nb=3 power=0";
        why = "Standard base-case check with a nonzero base.";
        hint = "Confirm the base case returns 1 regardless of nb, as long as power==0.";
    } else if (id == 3) {
        res = ft_recursive_power(5, 3); exp = 125; inputs = "nb=5 power=3";
        why = "Standard recursive case; validates the general 'nb * recurse(power-1)' formula.";
        hint = "Trace power=3,2,1,0 and check each intermediate multiplication.";
    } else if (id == 4) {
        res = ft_recursive_power(2, 8); exp = 256; inputs = "nb=2 power=8";
        why = "Deeper recursion (8 stack frames) with a round power-of-two result, easy to sanity-check by hand.";
        hint = "If this fails but 5^3 passes, look for an off-by-one in how many times you recurse.";
    } else if (id == 5) {
        res = ft_recursive_power(-2, 5); exp = -32; inputs = "nb=-2 power=5";
        why = "Negative base with an odd exponent must keep the negative sign.";
        hint = "If you get +32, you're likely dropping the sign somewhere (e.g. multiplying abs values).";
    } else if (id == 6) {
        res = ft_recursive_power(-2, 4); exp = 16; inputs = "nb=-2 power=4";
        why = "Negative base with an even exponent must be positive; paired with the previous test this fully checks sign handling.";
        hint = "If you get -16, your sign handling always flips instead of depending on the parity of the exponent.";
    } else if (id == 7) {
        res = ft_recursive_power(0, -1); exp = 0; inputs = "nb=0 power=-1";
        why = "Combines a tempting nb==0 special case with the power<0 rule, which must take priority.";
        hint = "The power<0 check must be evaluated first, unconditionally, before any nb==0 branch.";
    } else if (id == 8) {
        res = ft_recursive_power(1, 200000); exp = 1; inputs = "nb=1 power=200000";
        why = "TRAP: the subject requires recursion here, and 200000 stack frames is deep but should still fit in a typical stack. Confirms the recursive implementation doesn't do anything pathological (e.g. large local buffers per frame) that would blow the stack far earlier than necessary.";
        hint = "If this crashes (segfault) while smaller powers work, each of your recursive calls is probably using more stack space than needed (large local arrays/structs per frame).";
    } else if (id == 9) {
        res = ft_recursive_power(2, INT_MIN); exp = 0; inputs = "nb=2 power=INT_MIN";
        why = "TRAP: without an immediate power<0 check, INT_MIN could be misused as a recursion/loop bound, effectively never terminating in practice.";
        hint = "This must return instantly with no recursion at all. If it hangs, your power<0 guard is missing or placed after other logic.";
    } else {
        return 1;
    }
    printf("RESULT" US "%s" US "%s" US "%s" US "%d" US "%d" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, res == exp ? "PASS" : "FAIL", res, exp, inputs, why, hint);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex04 : ft_fibonacci
# --------------------------------------------------------------------------
HARNESSES["ex04"] = ("ft_fibonacci.c", r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

int ft_fibonacci(int index);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Negative index (-42)",                "CORE"},
    {"Boundary just below zero (-1)",       "CORE"},
    {"Index 0 - base case",                 "CORE"},
    {"Index 1 - base case",                 "CORE"},
    {"Index 2 (sequence-definition trap)",  "CORE"},
    {"Standard index (7)",                  "CORE"},
    {"Larger index (10)",                   "CORE"},
    {"Extreme negative index (INT_MIN)",    "TRAP"},
    {"Exponential blow-up stress (index 42)", "TRAP"},
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
    long res, exp;
    const char *why, *hint, *inputs;
    if (id == 0) {
        res = ft_fibonacci(-42); exp = -1; inputs = "index=-42";
        why = "Subject: 'if index is less than 0, the function should return -1'.";
        hint = "Make sure the negative-index guard returns -1 immediately, without recursing.";
    } else if (id == 1) {
        res = ft_fibonacci(-1); exp = -1; inputs = "index=-1";
        why = "Exact edge of the valid domain; catches an off-by-one guard (e.g. 'index <= -1' vs 'index < 0', which happen to be equivalent, but 'index < -1' would not be).";
        hint = "Double-check your comparison operator on the negative-index guard.";
    } else if (id == 2) {
        res = ft_fibonacci(0); exp = 0; inputs = "index=0";
        why = "Subject fixes the sequence to start '0, 1, 1, 2', i.e. F(0)=0. This is the first recursion base case.";
        hint = "Your base case for index==0 must return 0, not 1.";
    } else if (id == 3) {
        res = ft_fibonacci(1); exp = 1; inputs = "index=1";
        why = "Second explicit base case, F(1)=1.";
        hint = "If index 0 passes but this fails, check you have a distinct base case for index==1 (not just index<=0).";
    } else if (id == 4) {
        res = ft_fibonacci(2); exp = 1; inputs = "index=2";
        why = "Classic trap: some people misremember Fibonacci as starting '1, 1, 2, 3...' and expect F(2)=2. The subject explicitly fixes F(2)=1 (0,1,1,2). This test exists purely to catch that misconception.";
        hint = "If you get 2 instead of 1, you've shifted the whole sequence by one index -- re-check against the subject's exact sequence '0, 1, 1, 2'.";
    } else if (id == 5) {
        res = ft_fibonacci(7); exp = 13; inputs = "index=7";
        why = "Standard case (sequence: 0,1,1,2,3,5,8,13) validating the general recursive step, not just the base cases.";
        hint = "Recompute the sequence by hand up to index 7 and compare.";
    } else if (id == 6) {
        res = ft_fibonacci(10); exp = 55; inputs = "index=10";
        why = "Slightly deeper recursion to catch an accumulation bug that only appears after several recursive steps.";
        hint = "If 7 passes but 10 fails, look closely for an off-by-one that compounds with recursion depth.";
    } else if (id == 7) {
        res = ft_fibonacci(INT_MIN); exp = -1; inputs = "index=INT_MIN";
        why = "TRAP: same INT_MIN class of bug as the other exercises. A guard that negates index before comparing (e.g. 'if (-index > 0)') is undefined behaviour for INT_MIN.";
        hint = "Just compare index<0 directly; never negate it to normalise the sign.";
    } else if (id == 8) {
        res = ft_fibonacci(42); exp = 267914296; inputs = "index=42";
        why = "TRAP, informational only: the subject requires a recursive implementation but does not require memoization. A naive recursive Fibonacci is exponential (roughly 2*F(n) calls), so index 42 takes a noticeable moment even in optimised C. This is NOT a spec violation if it's slow -- it just demonstrates the real cost of unmemoized recursion, which is worth knowing.";
        hint = "If this times out, it's not necessarily wrong per the subject, just slow. If you're curious how to speed it up without breaking the 'must be recursive' rule, look into memoization (caching already-computed results, e.g. in a static array).";
    } else {
        return 1;
    }
    printf("RESULT" US "%s" US "%s" US "%s" US "%ld" US "%ld" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, res == exp ? "PASS" : "FAIL", res, exp, inputs, why, hint);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex05 : ft_sqrt
# --------------------------------------------------------------------------
HARNESSES["ex05"] = ("ft_sqrt.c", r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

int ft_sqrt(int nb);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Negative bound (-25)",                "CORE"},
    {"Boundary just below zero (-1)",       "CORE"},
    {"Zero value (0)",                      "CORE"},
    {"One value (1)",                       "CORE"},
    {"Irrational square root (2)",          "CORE"},
    {"Perfect square (4)",                  "CORE"},
    {"Just below a perfect square (15)",    "CORE"},
    {"Perfect square (16)",                 "CORE"},
    {"Largest perfect square near INT_MAX (2147395600)", "CORE"},
    {"INT_MIN boundary",                    "TRAP"},
    {"INT_MAX overflow guard",              "TRAP"},
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
    int res, exp;
    const char *why, *hint, *inputs;
    if (id == 0) {
        res = ft_sqrt(-25); exp = 0; inputs = "nb=-25";
        why = "Negative numbers have no real square root, so the function must fall into the 'irrational -> 0' rule.";
        hint = "Make sure negative input is rejected before any search loop runs.";
    } else if (id == 1) {
        res = ft_sqrt(-1); exp = 0; inputs = "nb=-1";
        why = "Exact edge of the negative domain, catches an off-by-one guard.";
        hint = "Check your comparison operator on the negativity guard.";
    } else if (id == 2) {
        res = ft_sqrt(0); exp = 0; inputs = "nb=0";
        why = "0 is a perfect square (0*0=0); this must be found by the search, not accidentally excluded by a loop that starts at 1.";
        hint = "If your search loop starts at i=1 instead of i=0, this case will incorrectly fall into the 'irrational' branch.";
    } else if (id == 3) {
        res = ft_sqrt(1); exp = 1; inputs = "nb=1";
        why = "1 is a perfect square (1*1=1); smallest strictly-positive case.";
        hint = "Confirm your search loop actually checks i=1 before concluding nb is irrational.";
    } else if (id == 4) {
        res = ft_sqrt(2); exp = 0; inputs = "nb=2";
        why = "2 has no integer square root, so the function must return 0 for it, per the subject.";
        hint = "If you return something other than 0, your loop's stopping condition is probably wrong (it should stop once i*i exceeds nb, and return 0 if no exact match was found).";
    } else if (id == 5) {
        res = ft_sqrt(4); exp = 2; inputs = "nb=4";
        why = "Simple standard perfect square case.";
        hint = "Basic sanity check of the search loop's core comparison i*i == nb.";
    } else if (id == 6) {
        res = ft_sqrt(15); exp = 0; inputs = "nb=15";
        why = "15 sits directly below the perfect square 16; a classic off-by-one bug will incorrectly return 4 here (mistaking 'i*i > nb, stop' for 'i*i >= nb, this is the answer').";
        hint = "If you got 4 instead of 0, your loop is probably returning the *approaching* value instead of only returning on an *exact* match.";
    } else if (id == 7) {
        res = ft_sqrt(16); exp = 4; inputs = "nb=16";
        why = "Paired with the previous test: confirms the exact match right after the off-by-one boundary still works correctly.";
        hint = "If 15 passes but this fails, your loop bound might stop one iteration too early.";
    } else if (id == 8) {
        res = ft_sqrt(2147395600); exp = 46340; inputs = "nb=2147395600";
        why = "46340^2 = 2147395600 is the largest perfect square that fits in a 32-bit signed int without overflowing during the multiplication. Confirms correctness across the full valid range, not just tiny numbers.";
        hint = "If this fails while smaller perfect squares pass, your loop might not run far enough, or your intermediate i*i computation might have overflowed earlier than necessary.";
    } else if (id == 9) {
        res = ft_sqrt(INT_MIN); exp = 0; inputs = "nb=INT_MIN";
        why = "TRAP: same negation-overflow bug class as other exercises. A guard like 'if (nb<0) nb=-nb;' is undefined behaviour for INT_MIN.";
        hint = "Just return 0 directly on nb<0; never negate nb to search for its 'positive equivalent'.";
    } else if (id == 10) {
        res = ft_sqrt(2147483647); exp = 0; inputs = "nb=INT_MAX (2147483647)";
        why = "TRAP: INT_MAX is not a perfect square, so the correct answer is 0 -- but reaching that answer safely requires the search loop to avoid overflow: the true square root boundary is ~46340.9, and 46341*46341 = 2147488281 overflows a signed 32-bit int (undefined behaviour), which can happen if the loop naively keeps computing i*i without bounding i by roughly sqrt(INT_MAX) or comparing via division instead of multiplication.";
        hint = "If this crashes or returns garbage while test 8 (nb=2147395600) passes, your search loop likely overflows int when i reaches ~46341. Bound the loop to i<=46340, or compare 'i <= nb/i' instead of computing i*i directly.";
    } else {
        return 1;
    }
    printf("RESULT" US "%s" US "%s" US "%s" US "%d" US "%d" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, res == exp ? "PASS" : "FAIL", res, exp, inputs, why, hint);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex06 : ft_is_prime
# --------------------------------------------------------------------------
HARNESSES["ex06"] = ("ft_is_prime.c", r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

int ft_is_prime(int nb);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Negative bound (-7)",                 "CORE"},
    {"Zero (0)",                            "CORE"},
    {"One (1)",                             "CORE"},
    {"Smallest prime (2)",                  "CORE"},
    {"Small prime (3)",                     "CORE"},
    {"Small non-prime (4)",                 "CORE"},
    {"Perfect square of a prime (9)",       "CORE"},
    {"Mid-range prime (17)",                "CORE"},
    {"Large prime, INT_MAX (2147483647)",   "CORE"},
    {"INT_MIN boundary",                    "TRAP"},
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
    int res, exp;
    const char *why, *hint, *inputs;
    if (id == 0) {
        res = ft_is_prime(-7); exp = 0; inputs = "nb=-7";
        why = "Negative numbers are not prime by definition.";
        hint = "Make sure negative input is rejected before any divisor-search loop runs.";
    } else if (id == 1) {
        res = ft_is_prime(0); exp = 0; inputs = "nb=0";
        why = "Subject explicitly states 0 is not prime; a naive divisor loop might behave oddly for 0 (e.g. 0 % i == 0 for every i).";
        hint = "Add an explicit nb<2 guard rather than relying on the divisor loop to reject 0 correctly.";
    } else if (id == 2) {
        res = ft_is_prime(1); exp = 0; inputs = "nb=1";
        why = "Subject explicitly states 1 is not prime -- a very common mistake, since 1 has no divisors other than itself.";
        hint = "If your loop only checks divisors from 2 up to sqrt(nb), it will never find a divisor for 1 and might wrongly conclude it's prime. Special-case nb<2 explicitly.";
    } else if (id == 3) {
        res = ft_is_prime(2); exp = 1; inputs = "nb=2";
        why = "Smallest prime; a classic loop-boundary trap. If your loop starts at i=2 and checks i*i<=nb (or nb/i), it must not enter the loop body at all for nb=2 (since 2*2 > 2) and still return 1.";
        hint = "If you get 0 here, your loop condition for entering the divisor search is probably too permissive for this exact boundary.";
    } else if (id == 4) {
        res = ft_is_prime(3); exp = 1; inputs = "nb=3";
        why = "Second small prime, right after the loop-boundary case above, to confirm the fix isn't a coincidence.";
        hint = "Same idea as nb=2: no divisor between 2 and sqrt(3) exists, so the loop must not find one.";
    } else if (id == 5) {
        res = ft_is_prime(4); exp = 0; inputs = "nb=4";
        why = "Smallest composite number with a repeated prime factor (2*2); simple standard non-prime case.";
        hint = "Confirm your loop actually detects 4 % 2 == 0.";
    } else if (id == 6) {
        res = ft_is_prime(9); exp = 0; inputs = "nb=9";
        why = "9 = 3*3 is a perfect square of a prime. This is the classic trap for sqrt-based loops: if the stopping condition is 'i*i < nb' instead of 'i*i <= nb' (or the division equivalent), the loop stops just before checking i=3 and wrongly returns 1.";
        hint = "If you got 1 instead of 0, your loop's stopping condition excludes the case where the divisor equals the square root exactly. Use <= (or 'i <= nb/i'), not <.";
    } else if (id == 7) {
        res = ft_is_prime(17); exp = 1; inputs = "nb=17";
        why = "Standard mid-range prime to validate the general case beyond the tiny boundary values.";
        hint = "Manually check 17 isn't divisible by 2..4 (sqrt(17)~4.1) and compare against your loop's result.";
    } else if (id == 8) {
        res = ft_is_prime(2147483647); exp = 1; inputs = "nb=2147483647 (INT_MAX)";
        why = "INT_MAX (2^31 - 1) is a known Mersenne prime. Validates correctness at the top of the valid range, and implicitly checks the divisor loop doesn't overflow while searching up to sqrt(INT_MAX) ~ 46341.";
        hint = "If this crashes or times out, your divisor-search loop bound (e.g. i*i <= nb) may overflow near i~46341 -- consider comparing i <= nb/i instead of computing i*i directly.";
    } else if (id == 9) {
        res = ft_is_prime(INT_MIN); exp = 0; inputs = "nb=INT_MIN";
        why = "TRAP: same INT_MIN negation-overflow class as the other exercises. A guard like 'if (nb<0) nb=-nb;' before checking primality is undefined behaviour for INT_MIN.";
        hint = "This mirrors the INT_MIN bug already caught in C04's ft_atoi_base. Just return 0 directly on nb<2; never negate nb.";
    } else {
        return 1;
    }
    printf("RESULT" US "%s" US "%s" US "%s" US "%d" US "%d" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, res == exp ? "PASS" : "FAIL", res, exp, inputs, why, hint);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex07 : ft_find_next_prime
# --------------------------------------------------------------------------
HARNESSES["ex07"] = ("ft_find_next_prime.c", r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

int ft_find_next_prime(int nb);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Negative bound (-10)",                "CORE"},
    {"Zero (0)",                            "CORE"},
    {"One (1)",                             "CORE"},
    {"Already the smallest prime (2)",      "CORE"},
    {"Already prime, standard (13)",        "CORE"},
    {"Non-prime standard value (14)",       "CORE"},
    {"Large value near INT_MAX (2147483640)", "CORE"},
    {"Self-prime overflow guard (INT_MAX)", "TRAP"},
    {"INT_MIN boundary",                    "TRAP"},
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
    int res, exp;
    const char *why, *hint, *inputs;
    if (id == 0) {
        res = ft_find_next_prime(-10); exp = 2; inputs = "nb=-10";
        why = "No lower bound is stated for invalid input here (unlike other exercises); the natural behaviour is to search upward and find the smallest prime, 2.";
        hint = "If you get something other than 2, your search may start from nb itself without clamping negative values up first.";
    } else if (id == 1) {
        res = ft_find_next_prime(0); exp = 2; inputs = "nb=0";
        why = "0 and 1 are both non-prime; the search must skip both and land on 2.";
        hint = "Make sure your is-prime check correctly rejects 0 before incrementing further.";
    } else if (id == 2) {
        res = ft_find_next_prime(1); exp = 2; inputs = "nb=1";
        why = "Same as above for nb=1, paired to make sure both edge values are handled, not just one by coincidence.";
        hint = "Make sure your is-prime check correctly rejects 1 before incrementing further.";
    } else if (id == 3) {
        res = ft_find_next_prime(2); exp = 2; inputs = "nb=2";
        why = "If nb is already prime, the function must return nb itself (>= nb, not > nb). Using the smallest prime here also catches a loop-boundary bug.";
        hint = "If you get 3 instead of 2, your search is probably starting from nb+1 instead of checking nb itself first.";
    } else if (id == 4) {
        res = ft_find_next_prime(13); exp = 13; inputs = "nb=13";
        why = "Standard case confirming the 'already prime, return nb' rule with a bigger prime, ruling out that test 3 passed by coincidence (2 is a very small/special value).";
        hint = "Recheck that your search always checks nb itself before incrementing.";
    } else if (id == 5) {
        res = ft_find_next_prime(14); exp = 17; inputs = "nb=14";
        why = "Standard non-prime case requiring the search to skip a composite in between (14, 15, 16 are all composite) before finding 17.";
        hint = "Manually verify 14, 15, 16 are all rejected by your is-prime check before 17 is accepted.";
    } else if (id == 6) {
        res = ft_find_next_prime(2147483640); exp = 2147483647; inputs = "nb=2147483640";
        why = "Validates the function works correctly all the way up to INT_MAX (2147483647, a known prime), without needing to go beyond it.";
        hint = "If this fails or crashes, check whether your is-prime check for large numbers overflows internally (e.g. i*i for i near 46341).";
    } else if (id == 7) {
        res = ft_find_next_prime(2147483647); exp = 2147483647; inputs = "nb=INT_MAX (2147483647)";
        why = "TRAP: INT_MAX itself is prime, so the correct answer is INT_MAX unchanged. But if the implementation always increments nb at least once before checking primality (e.g. 'do { nb++; } while (!is_prime(nb));' without first checking nb itself), incrementing past INT_MAX is signed integer overflow: undefined behaviour.";
        hint = "Always check whether nb itself is already prime before entering any incrementing loop. Don't assume you always need to move forward at least once.";
    } else if (id == 8) {
        res = ft_find_next_prime(INT_MIN); exp = 2; inputs = "nb=INT_MIN";
        why = "TRAP: same INT_MIN negation-overflow class as the other exercises. A guard like 'if (nb<0) nb=-nb;' is undefined behaviour for INT_MIN.";
        hint = "Just clamp negative input up to a small starting point (e.g. 2) by comparison, never by negating nb.";
    } else {
        return 1;
    }
    printf("RESULT" US "%s" US "%s" US "%s" US "%d" US "%d" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, res == exp ? "PASS" : "FAIL", res, exp, inputs, why, hint);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex08 : ft_ten_queens_puzzle
# --------------------------------------------------------------------------
HARNESSES["ex08"] = ("ft_ten_queens_puzzle.c", r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

int ft_ten_queens_puzzle(void);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Total unique solution count (== 724)",        "CORE"},
    {"Output line format (10 digits + newline)",     "CORE"},
    {"Each line is a valid row permutation",         "CORE"},
    {"No two queens share a diagonal",               "CORE"},
    {"No duplicate solutions",                       "CORE"},
};

/* Runs the student's puzzle solver with stdout redirected to a temp file,
 * so we can inspect the raw byte output regardless of which write-based
 * approach they used (write() directly, or buffered stdio on top of it). */
static int capture_output(char *path_out, int *ret_val)
{
    int stdout_backup = dup(STDOUT_FILENO);
    char tmp_path[] = "/tmp/queens_out_XXXXXX";
    int fd = mkstemp(tmp_path);
    if (fd < 0)
        return 0;
    fflush(stdout);
    dup2(fd, STDOUT_FILENO);
    close(fd);

    *ret_val = ft_ten_queens_puzzle();

    fflush(stdout);
    dup2(stdout_backup, STDOUT_FILENO);
    close(stdout_backup);
    strcpy(path_out, tmp_path);
    return 1;
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
    char tmp_path[64];
    int ret_val = 0;
    const char *why, *hint, *inputs = "void";

    if (!capture_output(tmp_path, &ret_val)) {
        printf("RESULT" US "%s" US "CORE" US "FAIL" US "capture error" US "n/a" US "void" US "n/a" US "Could not create a temp file to capture stdout.\n", META[id].name);
        return 0;
    }

    FILE *f = fopen(tmp_path, "r");
    char lines[900][16];
    int line_count = 0;
    if (f) {
        char buf[64];
        while (fgets(buf, sizeof(buf), f) && line_count < 900) {
            strncpy(lines[line_count], buf, 15);
            lines[line_count][15] = '\0';
            line_count++;
        }
        fclose(f);
    }
    unlink(tmp_path);

    if (id == 0) {
        why = "Subject: the function must return the total number of valid solutions found. The 10-queens problem has exactly 724 solutions -- this is a well known, verifiable constant.";
        hint = "If your count is off, double-check that you count every successful full-board placement exactly once, and that you don't return early or double count.";
        printf("RESULT" US "%s" US "%s" US "%s" US "%d" US "724" US "void" US "%s" US "%s\n",
            META[id].name, META[id].cat, ret_val == 724 ? "PASS" : "FAIL", ret_val, why, hint);
    } else if (id == 1) {
        int valid_format = (line_count > 0);
        for (int i = 0; i < line_count && valid_format; i++) {
            size_t len = strlen(lines[i]);
            if (len != 11 || lines[i][10] != '\n') { valid_format = 0; break; }
            for (int c = 0; c < 10; c++)
                if (lines[i][c] < '0' || lines[i][c] > '9') { valid_format = 0; break; }
        }
        why = "Subject's example output shows exactly 10 digits followed by a newline per solution, read left to right as one row-position per column.";
        hint = "Check you print exactly 10 characters ('0'-'9') per solution followed by '\\n', with nothing extra (no spaces, no trailing garbage).";
        printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "10 digits + newline" US "void" US "%s" US "%s\n",
            META[id].name, META[id].cat, valid_format ? "PASS" : "FAIL", valid_format ? "OK" : "Malformed line", why, hint);
    } else if (id == 2) {
        int valid = (line_count > 0);
        int bad_line = -1;
        for (int i = 0; i < line_count && valid; i++) {
            int seen[10] = {0};
            for (int c = 0; c < 10 && strlen(lines[i]) >= 10; c++) {
                int d = lines[i][c] - '0';
                if (d < 0 || d > 9 || seen[d]) { valid = 0; bad_line = i; break; }
                seen[d] = 1;
            }
        }
        why = "Since each column holds exactly one queen and there are 10 rows, a genuinely valid solution's digits must be a permutation of 0-9 (no repeated row). If two queens shared a row, they'd attack each other horizontally -- this checks that beyond just 'looks like 10 digits'.";
        hint = bad_line >= 0 ? "At least one printed line has a repeated digit, meaning two queens were placed on the same row -- a real non-attack violation, not just a formatting issue." : "n/a";
        printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "permutation of 0-9 per line" US "void" US "%s" US "%s\n",
            META[id].name, META[id].cat, valid ? "PASS" : "FAIL", valid ? "OK" : "Repeated digit found", why, hint);
    } else if (id == 3) {
        int valid = (line_count > 0);
        int bad_line = -1;
        for (int i = 0; i < line_count && valid; i++) {
            if (strlen(lines[i]) < 10) { valid = 0; bad_line = i; break; }
            int row[10];
            for (int c = 0; c < 10; c++)
                row[c] = lines[i][c] - '0';
            for (int a = 0; a < 10 && valid; a++)
                for (int b = a + 1; b < 10; b++)
                    if (row[a] - row[b] == a - b || row[b] - row[a] == a - b) { valid = 0; bad_line = i; break; }
        }
        why = "The whole point of the N-Queens puzzle is that no two queens attack each other: same row (checked separately above), same column (impossible by construction, one per column), OR same diagonal. This directly verifies the diagonal constraint by checking |row[a]-row[b]| != |a-b| for every pair of columns, which is what actually makes a placement a *real* solution rather than just 10 well-formatted digits.";
        hint = bad_line >= 0 ? "At least one printed solution has two queens on the same diagonal -- your backtracking's diagonal-attack check has a bug (often an off-by-one in the |row difference| vs |column difference| comparison)." : "n/a";
        printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "no shared diagonal in any line" US "void" US "%s" US "%s\n",
            META[id].name, META[id].cat, valid ? "PASS" : "FAIL", valid ? "OK" : "Diagonal attack found", why, hint);
    } else if (id == 4) {
        int valid = (line_count > 0);
        int dup_found = -1;
        for (int i = 0; i < line_count && valid; i++)
            for (int j = i + 1; j < line_count; j++)
                if (strncmp(lines[i], lines[j], 10) == 0) { valid = 0; dup_found = i; break; }
        why = "724 is the count of *distinct* solutions. Printing the same solution twice (e.g. from a bug that doesn't fully backtrack/reset state between branches) could inflate the reported count to match 724 by accident while actually missing a different real solution.";
        hint = dup_found >= 0 ? "The same exact board layout was printed more than once -- check that your backtracking correctly undoes ('un-places') a queen before trying the next row in a column." : "n/a";
        printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "all %d lines distinct" US "void" US "%s" US "%s\n",
            META[id].name, META[id].cat, valid ? "PASS" : "FAIL", valid ? "OK" : "Duplicate solution found", line_count, why, hint);
    }
    (void)inputs;
    return 0;
}
""")

# ==========================================================================
#  TEST RUNNER
# ==========================================================================

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

def tag(category):
    if category == "TRAP":
        return f"{C_MAGENTA}[TRAP]{C_RESET}"
    return f"{C_DIM}[CORE]{C_RESET}"

def run_exercise_tests(ex_id, c_file_name, harness_code):
    print(f"\n{C_CYAN}{C_BOLD}============ Evaluating {ex_id} ({c_file_name}) ============{C_RESET}")

    if not os.path.exists(ex_id):
        print_fail(f"Turn-in directory '{ex_id}' missing.")
        return 0, 0, 0

    src_path = os.path.join(ex_id, c_file_name)
    if not os.path.exists(src_path):
        print_fail(f"Source file '{src_path}' missing.")
        return 0, 0, 0

    tmp_dir = tempfile.mkdtemp()
    harness_path = os.path.join(tmp_dir, "harness.c")
    exec_path = os.path.join(tmp_dir, "test_runner")

    with open(harness_path, "w") as f:
        f.write(harness_code)

    shutil.copy(src_path, tmp_dir)

    comp_cmd = ["cc", "-Wall", "-Wextra", "-Werror", "harness.c", c_file_name, "-o", "test_runner"]
    comp_res = subprocess.run(comp_cmd, cwd=tmp_dir, capture_output=True, text=True)

    if comp_res.returncode != 0:
        print_fail("Compilation error (-Wall -Wextra -Werror failed)")
        print(f"{C_YELLOW}{comp_res.stderr}{C_RESET}")
        shutil.rmtree(tmp_dir)
        return 0, 0, 0

    list_res = subprocess.run([exec_path, "list"], capture_output=True, text=True)
    if list_res.returncode != 0:
        print_fail("Failed to retrieve test indices configuration.")
        shutil.rmtree(tmp_dir)
        return 0, 0, 0

    tests = []
    for line in list_res.stdout.strip().split("\n"):
        if US in line:
            t_id, t_cat, t_name = line.split(US, 2)
            tests.append((t_id, t_cat, t_name))

    core_pass = core_total = 0
    trap_pass = trap_total = 0

    for t_id, t_cat, t_name in tests:
        timeout = 20 if t_cat == "CORE" else 20
        try:
            test_res = subprocess.run([exec_path, t_id], capture_output=True, text=True, timeout=timeout)
            if test_res.returncode != 0:
                _report_crash(t_name, t_cat, test_res.returncode)
                if t_cat == "CORE":
                    core_total += 1
                else:
                    trap_total += 1
                continue

            out = test_res.stdout.strip()
            if not out.startswith("RESULT" + US):
                print_fail(f"{tag(t_cat)} {t_name} -> Invalid harness output format.")
                if t_cat == "CORE":
                    core_total += 1
                else:
                    trap_total += 1
                continue

            parts = out.split(US)
            # RESULT, name, category, status, got, expected, inputs, why, hint
            if len(parts) < 9:
                print_fail(f"{tag(t_cat)} {t_name} -> Output parsing error (unexpected field count).")
                if t_cat == "CORE":
                    core_total += 1
                else:
                    trap_total += 1
                continue

            _, name, category, status, got, expected, inputs, why, hint = parts[:9]

            if category == "CORE":
                core_total += 1
            else:
                trap_total += 1

            if status == "PASS":
                print_pass(f"{tag(category)} {name}")
                if category == "CORE":
                    core_pass += 1
                else:
                    trap_pass += 1
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

        except subprocess.TimeoutExpired:
            print_fail(f"{tag(t_cat)} {t_name} -> Timeout ({timeout}s) expired -- possible infinite loop/recursion.")
            if t_cat == "CORE":
                core_total += 1
            else:
                trap_total += 1

    shutil.rmtree(tmp_dir)
    score = int((core_pass / core_total) * 100) if core_total > 0 else 0
    return score, (trap_pass, trap_total), core_total


def _report_crash(t_name, t_cat, code):
    if code < 0:
        reason = f"terminated by signal {-code} (likely a crash: segfault, abort, etc.)"
    else:
        reason = f"exited with status {code}"
    print_fail(f"{tag(t_cat)} {t_name} -> Process {reason}.")
    if t_cat == "TRAP":
        print(f"  └── Hint     : {C_YELLOW}This is an adversarial/edge case, not officially graded -- but a crash here usually points to signed overflow, unguarded recursion depth, or an unguarded loop bound. See the exercise's TRAP tests above for the specific bug class targeted.{C_RESET}")


def main():
    print(f"{C_WHITE}{C_BOLD}=========================================================")
    print("        42 PISCINE C05 - ADVERSARIAL / VERBOSE TESTER    ")
    print("=========================================================")
    print(f"{C_RESET}{C_DIM}CORE  = tests a rule stated in the subject; counts toward score/rank.")
    print(f"TRAP  = adversarial edge case (overflow, recursion depth, perf);")
    print(f"        informational only, never affects score.{C_RESET}")

    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    sorted_exercises = sorted(HARNESSES.keys())
    if args:
        sorted_exercises = [a for a in sorted_exercises if a in args]
        if not sorted_exercises:
            print_fail(f"No matching exercises for: {args}")
            return

    results = []
    trap_summary = []

    for ex in sorted_exercises:
        c_file, harness = HARNESSES[ex]
        score, trap_stats, core_total = run_exercise_tests(ex, c_file, harness)
        rank = calculate_rank(score)
        results.append((ex, score, rank, core_total))
        if isinstance(trap_stats, tuple):
            trap_summary.append((ex, trap_stats[0], trap_stats[1]))

    print(f"\n{C_WHITE}{C_BOLD}+-------------------------------------------------------+")
    print("|                   FINAL SCOREBOARD                     |")
    print(f"+-------------------------------------------------------+{C_RESET}")
    print(f"| {'Exercise':<10} | {'CORE score':<12} | {'Rank':<6} | {'Trap insights':<14}|")
    print("+------------+--------------+--------+----------------+")

    for (ex, score, rank, core_total), (_, tpass, ttotal) in zip(results, trap_summary or [(e, 0, 0) for e, *_ in results]):
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
