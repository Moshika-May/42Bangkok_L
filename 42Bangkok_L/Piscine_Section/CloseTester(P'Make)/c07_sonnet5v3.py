#!/usr/bin/env python3
"""
42 Piscine - C07 Adversarial Tester
-----------------------------------
Same design as the c05 tester:

  * Every test carries a CATEGORY:
      - CORE : directly checks a rule stated in the subject. Moulinette-relevant.
               These are the only tests that count towards the score/rank.
      - TRAP : an adversarial/edge test that is NOT explicitly graded by the
               subject, but exposes classic implementation bugs (INT_MIN
               negation overflow, writing through a "read-only" input
               pointer, etc). TRAP failures are reported as insights and
               never hurt the score, but they explain a real bug class.

  * Every test carries a WHY (why we bother testing this) and, on failure,
    a HINT (a concrete, actionable pointer towards the likely bug).

  * -v / --verbose prints the WHY for every test (even passing ones).

Usage:
    python3 c07_tester.py            # normal run
    python3 c07_tester.py -v         # verbose: show rationale for every test
    python3 c07_tester.py ex04       # only run a specific exercise
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

CC = "cc"
CFLAGS = ["-Wall", "-Wextra", "-Werror"]                                          # exact moulinette flags
SANFLAGS = ["-Wall", "-Wextra", "-Werror", "-fsanitize=address,undefined", "-g"]  # extra safety net

# ==========================================================================
#  HARNESSES
# ==========================================================================
# Each harness is a self-contained C program (compiled together with the
# turned-in source file(s)). It exposes two modes:
#   argv[1] == "list"   -> prints "id|CATEGORY|Name" for every test, one per line
#   argv[1] == "<id>"   -> runs test <id> and prints a single RESULT line:
#        RESULT<US>name<US>category<US>PASS/FAIL<US>got<US>expected<US>inputs<US>why<US>hint
#
# HARNESSES[ex] = (list_of_c_files_to_compile, harness_source)

HARNESSES = {}

# --------------------------------------------------------------------------
# ex00 : ft_strdup
# --------------------------------------------------------------------------
HARNESSES["ex00"] = (["ft_strdup.c"], r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *ft_strdup(char *src);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Normal string",                                             "CORE"},
    {"Empty string",                                               "CORE"},
    {"Independent copy (mutating dup must not affect original)",   "CORE"},
    {"Long string (1000 chars)",                                   "CORE"},
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

    static char longbuf[1001];
    for (int i = 0; i < 1000; i++)
        longbuf[i] = 'a' + (i % 26);
    longbuf[1000] = '\0';
    char testbuf[] = "Test";

    char *srcs[] = {"Hello, 42!", "", testbuf, longbuf};
    const char *why_arr[] = {
        "Baseline: strdup must allocate a new buffer and copy the string content exactly.",
        "Edge case with strlen(src)==0: must still malloc 1 byte for the null terminator and return a valid, freeable pointer, not NULL.",
        "strdup must return an INDEPENDENT allocation. If it secretly returns the same pointer (or one aliasing the same memory), mutating the copy corrupts the original.",
        "Stress test: a longer buffer catches off-by-one size calculations that a short string might hide (e.g. malloc(strlen(src)) forgetting the +1)."
    };
    const char *hint_arr[] = {
        "Check that you malloc(strlen(src) + 1) and copy every byte including the terminating '\\0'.",
        "Even for an empty string you must still call malloc(1) and write '\\0' -- don't special-case it into returning NULL.",
        "If this fails, you are probably returning src itself instead of a newly malloc'd buffer.",
        "If short strings pass but this fails, recount your malloc size -- it must be strlen(src)+1, not strlen(src)."
    };

    char *src = srcs[id];
    char *ret = ft_strdup(src);
    int passed = 1;
    char got[128] = "matches src content, independent allocation";

    if (!ret) { passed = 0; strcpy(got, "NULL"); }
    else if (ret == src) { passed = 0; strcpy(got, "same pointer as src (not a new allocation)"); }
    else if (strcmp(ret, src) != 0) { passed = 0; snprintf(got, sizeof(got), "\"%.60s\"", ret); }
    else if (id == 2) {
        ret[0] = 'X';
        if (src[0] != 'T') { passed = 0; strcpy(got, "mutating the copy affected the original"); }
    }
    if (ret)
        free(ret); /* if this wasn't a real malloc, this may abort -- caught as a crash */

    char inputs[64];
    snprintf(inputs, sizeof(inputs), "src=\"%.20s\" (len=%zu)", src, strlen(src));

    printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, passed ? "PASS" : "FAIL", got,
        "malloc'd copy, equal content, freeable", inputs, why_arr[id], hint_arr[id]);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex01 : ft_range
# --------------------------------------------------------------------------
HARNESSES["ex01"] = (["ft_range.c"], r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int *ft_range(int min, int max);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Normal ascending range [3,8)",     "CORE"},
    {"min == max -> NULL",               "CORE"},
    {"min > max -> NULL",                "CORE"},
    {"Range crossing zero [-3,3)",       "CORE"},
    {"Single element range [5,6)",       "CORE"},
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

    int mins[] = {3, 5, 8, -3, 5};
    int maxs[] = {8, 5, 3, 3, 6};
    const char *why_arr[] = {
        "Baseline correctness: the array must contain exactly the integers from min (inclusive) to max (exclusive), in order.",
        "Subject: 'If the value of min is greater than or equal to max, a NULL pointer should be returned.' Tests the == boundary of that rule.",
        "Same rule, opposite direction: min strictly greater than max must also yield NULL.",
        "Ranges spanning zero can reveal off-by-one bugs in loop bounds that only manifest when crossing the sign boundary.",
        "Smallest non-empty range (exactly one element) checks the loop runs exactly once, not zero or two times."
    };
    const char *hint_arr[] = {
        "Trace your loop: for i from min to max-1, array[i-min] should equal i.",
        "Make sure your guard is 'min >= max', not 'min > max' -- otherwise this equal case slips through and dereferences a zero-size (or garbage) allocation.",
        "Check the direction of your comparison operator in the guard clause.",
        "Print every element and compare against -3,-2,-1,0,1,2 by hand.",
        "If this returns an empty or wrong-length array, your loop bound is probably 'i < max - 1' instead of 'i < max - min'."
    };

    int min = mins[id], max = maxs[id];
    int *r = ft_range(min, max);
    int passed = 1;
    char got[128] = "matches expected sequence";

    if (id == 1 || id == 2) {
        if (r != NULL) { passed = 0; strcpy(got, "non-NULL pointer"); free(r); }
        else strcpy(got, "NULL");
    } else {
        if (!r) { passed = 0; strcpy(got, "NULL"); }
        else {
            for (int i = 0; i < max - min; i++) {
                if (r[i] != min + i) { passed = 0; snprintf(got, sizeof(got), "r[%d] = %d", i, r[i]); break; }
            }
            free(r);
        }
    }

    char inputs[64];
    snprintf(inputs, sizeof(inputs), "min=%d max=%d", min, max);
    char expected[64];
    if (id == 1 || id == 2) strcpy(expected, "NULL");
    else snprintf(expected, sizeof(expected), "[%d..%d)", min, max);

    printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, passed ? "PASS" : "FAIL", got, expected, inputs, why_arr[id], hint_arr[id]);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex02 : ft_ultimate_range (includes a deterministic malloc-failure test via RLIMIT_AS)
# --------------------------------------------------------------------------
HARNESSES["ex02"] = (["ft_ultimate_range.c"], r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>

int ft_ultimate_range(int **range, int min, int max);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Normal ascending range [3,8)",             "CORE"},
    {"min == max -> 0, *range = NULL",           "CORE"},
    {"min > max -> 0, *range = NULL",            "CORE"},
    {"Range crossing zero [-3,3)",               "CORE"},
    {"Single element range [5,6)",               "CORE"},
    {"Large range correctness (2000 elements)",  "CORE"},
    {"Forced allocation failure (RLIMIT_AS) -> -1", "CORE"},
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

    int mins[] = {3, 5, 8, -3, 5, -1000, 0};
    int maxs[] = {8, 5, 3, 3, 6, 1000, 50000000};
    const char *why_arr[] = {
        "Baseline correctness: same rule as ft_range, but returned via an out-parameter and a size return value.",
        "Subject: 'If min is greater or equal to max, range will point to NULL and it should return 0.' Tests the == boundary.",
        "Same rule, opposite direction: min strictly greater than max must also give 0 / *range == NULL.",
        "Ranges spanning zero can reveal off-by-one bugs in loop bounds that only manifest when crossing the sign boundary.",
        "Smallest non-empty range (exactly one element) checks the loop runs exactly once.",
        "Larger dataset increases confidence that indexing math holds up beyond tiny examples -- catches subtle stride/index bugs that only show up statistically.",
        "Subject: 'The size of range should be returned (or -1 on error).' A real malloc() failure, forced here via RLIMIT_AS, is the only well-defined error case."
    };
    const char *hint_arr[] = {
        "Trace your loop: for i from min to max-1, (*range)[i-min] should equal i.",
        "Make sure your guard is 'min >= max', not 'min > max'.",
        "Check the direction of your comparison operator in the guard clause.",
        "Print every element and compare against -3,-2,-1,0,1,2 by hand.",
        "If this returns 0 or a wrong size, your loop bound is probably 'i < max - 1' instead of 'i < max - min'.",
        "If only large ranges fail, look for integer overflow or truncation in your size calculation (max-min) or in your loop index type.",
        "Check that you actually test malloc's return value for NULL and return -1 in that case, instead of dereferencing a NULL pointer or returning a bogus size."
    };

    int min = mins[id], max = maxs[id];

    if (id == 6) {
        struct rlimit lim;
        lim.rlim_cur = 15 * 1024 * 1024;
        lim.rlim_max = 15 * 1024 * 1024;
        setrlimit(RLIMIT_AS, &lim);
    }

    int *range = (int *)0x1; /* poison value: lets us tell "left untouched" apart from a real NULL */
    int ret = ft_ultimate_range(&range, min, max);
    int passed = 1;
    char got[160] = "matches expected";

    if (id == 1 || id == 2) {
        if (ret != 0) { passed = 0; snprintf(got, sizeof(got), "returned %d", ret); }
        else if (range != NULL) { passed = 0; strcpy(got, "*range != NULL"); }
    } else if (id == 6) {
        if (ret != -1) {
            passed = 0;
            snprintf(got, sizeof(got), "returned %d instead of -1", ret);
            if (ret > 0 && range && range != (int *)0x1)
                free(range);
        }
    } else {
        int expected_size = max - min;
        if (ret != expected_size) { passed = 0; snprintf(got, sizeof(got), "returned %d", ret); }
        else if (!range) { passed = 0; strcpy(got, "*range is NULL"); }
        else {
            for (int i = 0; i < expected_size; i++) {
                if (range[i] != min + i) { passed = 0; snprintf(got, sizeof(got), "range[%d] = %d", i, range[i]); break; }
            }
            free(range);
        }
    }

    char inputs[64];
    snprintf(inputs, sizeof(inputs), "min=%d max=%d", min, max);
    char expected[64];
    if (id == 1 || id == 2) strcpy(expected, "return 0, *range = NULL");
    else if (id == 6) strcpy(expected, "return -1 on alloc failure");
    else snprintf(expected, sizeof(expected), "return %d, [%d..%d)", max - min, min, max);

    printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, passed ? "PASS" : "FAIL", got, expected, inputs, why_arr[id], hint_arr[id]);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex03 : ft_strjoin
# --------------------------------------------------------------------------
HARNESSES["ex03"] = (["ft_strjoin.c"], r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *ft_strjoin(int size, char **strs, char *sep);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"size=0 -> freeable empty string",                "CORE"},
    {"Normal two-element join",                         "CORE"},
    {"Single element (no separator should appear)",     "CORE"},
    {"Empty separator",                                 "CORE"},
    {"Multi-char separator, many elements",              "CORE"},
    {"Array containing empty-string elements",           "CORE"},
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

    char *strs0[] = {NULL};
    char *strs1[] = {"Hello", "World"};
    char *strs2[] = {"Solo"};
    char *strs3[] = {"a", "b", "c"};
    char *strs4[] = {"a", "b", "c", "d"};
    char *strs5[] = {"", "mid", ""};

    int sizes[] = {0, 2, 1, 3, 4, 3};
    char **arrs[] = {strs0, strs1, strs2, strs3, strs4, strs5};
    char *seps[] = {",", ", ", "-", "", " | ", "-"};
    char *exps[] = {"", "Hello, World", "Solo", "abc", "a | b | c | d", "-mid-"};

    const char *why_arr[] = {
        "Subject: 'If size is 0, you must return an empty string that can be freed using free().' A literal like \"\" is not free()-able; it must come from malloc.",
        "Baseline correctness: strings must be concatenated with the separator inserted exactly once between each pair.",
        "With only one string, no separator should be inserted anywhere -- a common bug is unconditionally appending sep after every element.",
        "An empty sep string is a degenerate case: joining should reduce to straight concatenation with nothing in between.",
        "Multi-character separators catch size-calculation bugs where you assumed sep is always a single character.",
        "Empty elements within the array must still get their surrounding separators -- they're not skipped or treated as absent."
    };
    const char *hint_arr[] = {
        "malloc(1) and write '\\0' into it when size==0, rather than returning a string literal or NULL.",
        "Count the separators: for N strings there should be exactly N-1 separators total.",
        "Your separator-insertion logic should only run BETWEEN elements (skip it before the first one), not after every element unconditionally.",
        "Make sure strcat/strcpy of an empty separator doesn't accidentally advance your write pointer or crash on a zero-length copy.",
        "Your total-size calculation must use strlen(sep), not a hardcoded '+1' per gap.",
        "Don't special-case a zero-length strs[i] by skipping the separator around it; treat it like any other element."
    };

    char *ret = ft_strjoin(sizes[id], arrs[id], seps[id]);
    int passed = 1;
    char got[160] = "matches expected";
    if (!ret) { passed = 0; strcpy(got, "NULL"); }
    else if (strcmp(ret, exps[id]) != 0) { passed = 0; snprintf(got, sizeof(got), "\"%.100s\"", ret); }
    if (ret)
        free(ret); /* aborts if this wasn't a real malloc -- caught as a crash */

    char inputs[64];
    snprintf(inputs, sizeof(inputs), "size=%d sep=\"%s\"", sizes[id], seps[id]);
    char expected[128];
    snprintf(expected, sizeof(expected), "\"%s\"", exps[id]);

    printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, passed ? "PASS" : "FAIL", got, expected, inputs, why_arr[id], hint_arr[id]);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex04 : ft_convert_base (files ft_convert_base.c + ft_convert_base2.c, both compiled in)
# Uses a small self-contained reference parser/renderer so expected values are
# computed on the fly for ANY (nbr, base_from, base_to) combo, instead of being
# hand-derived and potentially wrong.
# --------------------------------------------------------------------------
HARNESSES["ex04"] = (["ft_convert_base.c", "ft_convert_base2.c"], r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *ft_convert_base(char *nbr, char *base_from, char *base_to);

#define US "\x1f"

typedef struct { const char *name; const char *cat; } meta_t;

static meta_t META[] = {
    {"Decimal to hex",                                          "CORE"},
    {"Negative number",                                          "CORE"},
    {"Leading whitespace + explicit '+' stripped",               "CORE"},
    {"Zero, base_to starting with '0' (baseline)",               "CORE"},
    {"Zero, base_to NOT starting with '0'",                      "CORE"},
    {"Fully scrambled base_from/base_to (moulinette-style)",     "CORE"},
    {"INT_MAX boundary",                                         "CORE"},
    {"Parsing stops at first non-digit (ft_atoi_base rules)",    "CORE"},
    {"Round-trip through a non-decimal base_from",                "CORE"},
    {"Invalid base_from: duplicate character",                  "CORE"},
    {"Invalid base_to: only one character",                     "CORE"},
    {"Invalid base: contains '+'",                               "CORE"},
    {"INT_MIN boundary",                                         "TRAP"},
    {"Randomized round-trip fuzz across bases (anti-hardcoding)", "TRAP"},
};

static long parse_ref(const char *nbr, const char *base_from) {
    long radix = (long)strlen(base_from);
    int i = 0;
    while (nbr[i] == ' ' || nbr[i] == '\t' || nbr[i] == '\n' || nbr[i] == '\v' || nbr[i] == '\f' || nbr[i] == '\r') i++;
    int neg = 0;
    if (nbr[i] == '+' || nbr[i] == '-') { neg = (nbr[i] == '-'); i++; }
    long val = 0;
    while (nbr[i]) {
        char *p = strchr((char *)base_from, nbr[i]);
        if (!p) break;
        val = val * radix + (long)(p - base_from);
        i++;
    }
    return neg ? -val : val;
}

static void render_ref(long val, const char *base_to, char *out) {
    long radix = (long)strlen(base_to);
    int idx = 0;
    if (val < 0) out[idx++] = '-';
    unsigned long mag = (val < 0) ? (unsigned long)(-val) : (unsigned long)val;
    char tmp[64]; int t = 0;
    if (mag == 0) tmp[t++] = base_to[0];
    while (mag > 0) { tmp[t++] = base_to[mag % (unsigned long)radix]; mag /= (unsigned long)radix; }
    while (t > 0) out[idx++] = tmp[--t];
    out[idx] = '\0';
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

    if (id == 13) {
        /* Randomized round-trip fuzz: pick a random integer value, render it
           into a random base_from (using the same render_ref oracle used
           elsewhere), convert it with the student's ft_convert_base, and
           check the result against render_ref in a random base_to. A
           solution that special-cases specific literal test strings has no
           way to pass this, since both the value and the bases are
           re-randomized (with a fixed seed, so still reproducible) on
           every run. */
        char *pool[] = {
            "0123456789", "01", "0123456789ABCDEF", "gYhQ_zUVuv", "i~pv",
            "01234567", "abcdefghijklmnopqrstuvwxyz", "ZYXWVUTSRQPONMLKJIHGFEDCBA"
        };
        int pool_size = 8;
        long forced[] = {0, 1, -1, 2147483647L, -2147483648L};
        int forced_count = 5;
        int trials = 300;
        int passed = 1;
        char got[200] = "matches expected";
        char expected[200] = "";
        char inputs[200] = "";

        srand(20260727);
        for (int t = 0; t < trials && passed; t++) {
            char *base_from = pool[rand() % pool_size];
            char *base_to = pool[rand() % pool_size];
            long value;
            if (t < forced_count)
                value = forced[t];
            else
                value = ((long)(rand() % 4000000001) - 2000000000L);

            char nbr[80];
            render_ref(value, base_from, nbr);
            char *ret = ft_convert_base(nbr, base_from, base_to);
            char exp[80];
            render_ref(value, base_to, exp);

            if (!ret || strcmp(ret, exp) != 0) {
                passed = 0;
                snprintf(got, sizeof(got), "\"%.100s\"", ret ? ret : "NULL");
                snprintf(expected, sizeof(expected), "\"%s\"", exp);
                snprintf(inputs, sizeof(inputs), "trial %d/%d: nbr=\"%s\" from=\"%s\" to=\"%s\" (value=%ld)",
                    t + 1, trials, nbr, base_from, base_to, value);
            }
            if (ret)
                free(ret);
        }
        if (passed) {
            snprintf(inputs, sizeof(inputs), "%d random (value, base_from, base_to) round-trips, fixed seed", trials);
            strcpy(expected, "all trials match");
        }

        printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s\n",
            META[id].name, META[id].cat, passed ? "PASS" : "FAIL", got, expected, inputs,
            "TRAP: a solution that special-cases specific literal test values (\"tape fixes\" patched in to satisfy a fixed test suite) will fail here even while passing every curated CORE test above, since these values are freshly randomized on every run and can't be pattern-matched in advance.",
            "If only this test fails, look for conditions in your code that check for a SPECIFIC input value or string rather than a general property of it (e.g. 'if nbr equals exactly this') -- that's the signature of a hardcoded patch standing in for a real implementation.");
        return 0;
    }

    char *DEC   = "0123456789";
    char *BIN   = "01";
    char *HEXUP = "0123456789ABCDEF";

    char *SCRAMBLED_TO   = "gYhQ_zUVuv";  /* zero digit is 'g', NOT '0' -- catches hardcoded-'0' bugs */
    char *SCRAMBLED_FROM = "i~pv";        /* zero digit is 'i' in this base_from */

    char *nbrs[]       = {"255", "-10", "   +42", "0", "0",           "i",             "2147483647", "12a34", "101",  "42",    "42", "42",           "-2147483648"};
    char *bases_from[] = {DEC,   DEC,    DEC,      DEC,  DEC,          SCRAMBLED_FROM,  DEC,          DEC,     BIN,    "0112",  DEC,  DEC,           DEC};
    char *bases_to[]   = {HEXUP, BIN,    DEC,      HEXUP, SCRAMBLED_TO, SCRAMBLED_TO,    BIN,          DEC,     HEXUP,  DEC,     "Z",  "01+3456789",  DEC};
    int   expect_null[] = {0,    0,      0,        0,     0,           0,               0,            0,       0,      1,       1,    1,            0};

    const char *why_arr[] = {
        "Baseline correctness: converts an ordinary positive decimal number into another base.",
        "Subject: the returned number must be prefixed only by a single and unique '-'. Confirms negative numbers are parsed and rendered with exactly one minus sign.",
        "Subject: 'nbr will follow the same rules as ft_atoi_base. Beware of +, -, and whitespaces.' Checks leading whitespace is skipped and an explicit '+' never appears in the output.",
        "Zero is a common special case: a digit-extraction loop that runs 'while value != 0' would produce an empty string if not special-cased. Uses a base_to whose zero digit happens to be the character '0', as a baseline sanity check.",
        "Same zero special-case, but with a base_to whose FIRST character is NOT '0'. This is the case that exposes a hardcoded return of the literal character '0' instead of a real base_to[0] lookup -- exactly the moulinette failure pattern of returning \"0\" when \"g\" was expected.",
        "Mirrors a real moulinette test: both base_from and base_to are fully scrambled, non-numeric alphabets. Every lookup (parsing AND rendering) must work purely by index -- there's no guarantee any particular character means 'zero' or that digits are '0'-'9' at all.",
        "Subject: 'The number represented by nbr must fit inside an int.' INT_MAX is the largest positive value that must round-trip correctly without overflow.",
        "Subject: nbr follows the same rules as ft_atoi_base -- parsing must stop at the first character not valid in base_from, not error out or read garbage past it.",
        "Round-tripping through a non-decimal base_from confirms the parser isn't silently hardcoded to assume base-10 input.",
        "A base with a repeated character is ambiguous (which occurrence does a digit map to?) and should be rejected as invalid.",
        "Subject: 'If a base is invalid, NULL should be returned.' A base needs at least 2 distinct characters to represent anything meaningful.",
        "Subject explicitly calls out '+' as a character to beware of -- it must not be usable as a base digit since it's reserved for sign parsing.",
        "TRAP: mirrors the INT_MIN bug already found in C04's ft_atoi_base. If the sign is applied by negating a plain 'int' that holds INT_MIN, that negation is signed integer overflow -- undefined behaviour."
    };
    const char *hint_arr[] = {
        "Verify your digit-extraction loop divides by strlen(base_to) each step and indexes into base_to for each digit, most-significant-first.",
        "Track the sign once, before parsing digits, and prepend exactly one '-' to the output -- not one per loop iteration.",
        "Skip whitespace first, then optionally consume a single '+' or '-' sign before parsing digits -- but never copy the '+' itself into the result.",
        "If value == 0, explicitly output the single digit base_to[0] instead of relying on a loop that never executes.",
        "Your zero-case helper must receive base_to and output base_to[0], not a hardcoded '0' character. A helper like ft_itoa_base_zero(void) that never sees base_to can only ever return \"0\", which is wrong for any base whose zero digit isn't literally '0'. Pass base_to into it and index base_to[0].",
        "Every digit lookup, on both the parsing side (looking a character up in base_from) and the rendering side (indexing into base_to), must work for ANY character set -- never assume digits are '0'-'9', and never assume index 0 is the character '0'.",
        "Make sure your accumulator during parsing is wide enough (or carefully bounded) to hold INT_MAX without wrapping before you've read all its digits.",
        "Your parsing loop should break (not error) as soon as it hits a character not found in base_from, and convert whatever was parsed so far.",
        "Double-check that parsing looks up each character's value via base_from (e.g. strchr), not via a hardcoded '0'-'9' assumption.",
        "Validate base_from/base_to for duplicate characters before doing any parsing/rendering, and return NULL immediately if found.",
        "Reject any base string with fewer than 2 characters (strlen(base) < 2).",
        "When validating a base string, explicitly reject it if it contains '+', '-', or any whitespace character.",
        "Keep the magnitude in a wider type (e.g. long) throughout parsing, and only decide the sign when rendering -- never write '-value' on a plain int that might be INT_MIN."
    };

    char *nbr = nbrs[id], *base_from = bases_from[id], *base_to = bases_to[id];
    char *ret = ft_convert_base(nbr, base_from, base_to);
    int passed = 1;
    char got[160] = "matches expected";
    char expected[64] = "";

    if (expect_null[id]) {
        strcpy(expected, "NULL");
        if (ret != NULL) { passed = 0; snprintf(got, sizeof(got), "\"%.100s\"", ret); free(ret); }
        else strcpy(got, "NULL");
    } else {
        long val = parse_ref(nbr, base_from);
        render_ref(val, base_to, expected);
        if (!ret) { passed = 0; strcpy(got, "NULL"); }
        else if (strcmp(ret, expected) != 0) { passed = 0; snprintf(got, sizeof(got), "\"%.100s\"", ret); }
        if (ret) free(ret);
    }

    char inputs[96];
    snprintf(inputs, sizeof(inputs), "nbr=\"%s\" from=\"%s\" to=\"%s\"", nbr, base_from, base_to);

    printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "\"%s\"" US "%s" US "%s" US "%s\n",
        META[id].name, META[id].cat, passed ? "PASS" : "FAIL", got, expected, inputs, why_arr[id], hint_arr[id]);
    return 0;
}
""")

# --------------------------------------------------------------------------
# ex05 : ft_split
# --------------------------------------------------------------------------
HARNESSES["ex05"] = (["ft_split.c"], r"""
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
    {"Randomized fuzz across strings/charsets (anti-hardcoding)",   "TRAP"},
};

static int is_sep_ref(char c, const char *charset) {
    if (*charset == '\0')
        return 0;
    return strchr(charset, c) != NULL;
}

/* Reference splitter used only to compute expected output for the fuzz
   test below -- deliberately written differently (scan-then-copy) from the
   likely student approach, so it doesn't share any bug in common. */
static int split_ref(const char *str, const char *charset, char tokens[][32], int max_tokens) {
    int count = 0;
    int i = 0;
    while (str[i]) {
        if (is_sep_ref(str[i], charset)) {
            i++;
            continue;
        }
        int start = i;
        while (str[i] && !is_sep_ref(str[i], charset))
            i++;
        int len = i - start;
        if (len > 31)
            len = 31;
        if (count < max_tokens) {
            memcpy(tokens[count], str + start, len);
            tokens[count][len] = '\0';
            count++;
        }
    }
    return count;
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
        "Baseline correctness: splits on the given charset characters into an array of tokens, NULL-terminated as the subject states.",
        "Subject: 'There cannot be any empty strings in your array.' Consecutive separators must collapse into a single split point.",
        "Leading and trailing separator characters must not produce leading/trailing empty tokens in the result.",
        "charset can contain several distinct separator characters at once -- any of them should trigger a split.",
        "If charset never appears in str, the whole string is exactly one token.",
        "An empty input string has no tokens to produce.",
        "An empty charset means there are no separator characters at all -- the entire input is one token.",
        "TRAP: Subject states 'the string given as an argument won't be modifiable.' Writing through str (e.g. inserting '\\0' in place instead of allocating real substrings) corrupts the caller's buffer even though C won't stop you from doing it."
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

    if (id == 8) {
        /* Randomized fuzz: build a random small string from a mix of
           "content" and "separator" characters plus a random subset of
           candidate separators as charset, compute the expected tokens with
           an independently-written reference splitter, and compare. A
           solution that special-cases specific literal strings/charsets has
           no way to pass this, since both are re-randomized (with a fixed
           seed, so still reproducible) on every run. */
        char SEP_POOL[] = ",;-_ ";
        char CONTENT_POOL[] = "abcdefXYZ0129";
        int trials = 300;
        int passed = 1;
        char got[400] = "matches expected";
        char expected[400] = "";
        char inputs[200] = "";

        srand(20260727);
        for (int t = 0; t < trials && passed; t++) {
            char charset[8];
            int clen = 0;
            for (int k = 0; SEP_POOL[k]; k++) {
                if (rand() % 2)
                    charset[clen++] = SEP_POOL[k];
            }
            charset[clen] = '\0';

            int slen = rand() % 25;
            char str[32];
            for (int k = 0; k < slen; k++) {
                if (rand() % 3 == 0)
                    str[k] = SEP_POOL[rand() % (int)strlen(SEP_POOL)];
                else
                    str[k] = CONTENT_POOL[rand() % (int)strlen(CONTENT_POOL)];
            }
            str[slen] = '\0';

            char exp_tokens[16][32];
            int exp_count = split_ref(str, charset, exp_tokens, 16);

            char str_copy[32];
            strcpy(str_copy, str);
            char **ret = ft_split(str_copy, charset);

            int got_count = 0;
            if (ret) {
                while (ret[got_count])
                    got_count++;
            }

            int ok = 1;
            if (!ret) {
                if (exp_count != 0)
                    ok = 0;
            } else if (got_count != exp_count) {
                ok = 0;
            } else {
                for (int i = 0; i < exp_count; i++) {
                    if (!ret[i] || strcmp(ret[i], exp_tokens[i]) != 0) {
                        ok = 0;
                        break;
                    }
                }
            }

            if (!ok) {
                passed = 0;
                char expjoined[300] = "";
                for (int i = 0; i < exp_count; i++) {
                    strcat(expjoined, "\"");
                    strcat(expjoined, exp_tokens[i]);
                    strcat(expjoined, "\" ");
                }
                char gotjoined[300] = "";
                if (ret) {
                    for (int i = 0; i < got_count; i++) {
                        strcat(gotjoined, "\"");
                        strcat(gotjoined, ret[i]);
                        strcat(gotjoined, "\" ");
                    }
                } else {
                    strcpy(gotjoined, "NULL");
                }
                snprintf(inputs, sizeof(inputs), "trial %d/%d: str=\"%s\" charset=\"%s\"", t + 1, trials, str, charset);
                snprintf(got, sizeof(got), "[%s]", gotjoined);
                snprintf(expected, sizeof(expected), "[%s]", expjoined);
            }

            if (ret) {
                for (int i = 0; i < got_count; i++)
                    free(ret[i]);
                free(ret);
            }
        }
        if (passed) {
            snprintf(inputs, sizeof(inputs), "%d random (str, charset) pairs, fixed seed", trials);
            strcpy(expected, "all trials match");
        }

        printf("RESULT" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s" US "%s\n",
            META[id].name, META[id].cat, passed ? "PASS" : "FAIL", got, expected, inputs,
            "TRAP: a solution that special-cases specific literal test strings/charsets (\"tape fixes\" patched in to satisfy a fixed test suite) will fail here, since both the string and the separator set are freshly randomized on every run and can't be pattern-matched in advance.",
            "If only this test fails, look for conditions that check for a SPECIFIC string or character rather than a general property (e.g. checking whether charset is exactly \",\") -- that's the signature of a hardcoded patch standing in for a real implementation.");
        return 0;
    }

    if (id == 7) {
        /* Heap buffer with one guard byte right after the string, so we can
           detect any in-place write or one-byte-past-the-end overflow. */
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
""")

# ==========================================================================
#  RUNNER
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

# (ex, test_id) pairs that MUST run under the plain (non-sanitized) binary.
# ASan's own shadow-memory mmap needs far more address space than the
# RLIMIT_AS-restricted allocation-failure test in ex02 allows for.
FORCE_PLAIN = {("ex02", "6")}

def run_exercise_tests(ex_id, c_files, harness_code):
    print(f"\n{C_CYAN}{C_BOLD}============ Evaluating {ex_id} ({', '.join(c_files)}) ============{C_RESET}")

    if not os.path.exists(ex_id):
        print_fail(f"Turn-in directory '{ex_id}' missing.")
        return 0, (0, 0)

    target_cs = [os.path.join(ex_id, f) for f in c_files]
    missing = [f for f in target_cs if not os.path.isfile(f)]
    if missing:
        print_fail(f"Source file(s) missing: {', '.join(missing)}")
        return 0, (0, 0)

    tmp_dir = tempfile.mkdtemp()
    harness_path = os.path.join(tmp_dir, "harness.c")
    bin_plain = os.path.join(tmp_dir, "bin_plain")
    bin_san = os.path.join(tmp_dir, "bin_san")

    with open(harness_path, "w") as f:
        f.write(harness_code)

    comp = subprocess.run([CC] + CFLAGS + [harness_path] + target_cs + ["-o", bin_plain],
                           capture_output=True, text=True)
    if comp.returncode != 0:
        print_fail("Compilation error (-Wall -Wextra -Werror failed)")
        print(f"{C_YELLOW}{comp.stderr}{C_RESET}")
        shutil.rmtree(tmp_dir)
        return 0, (0, 0)

    # Best-effort extra pass with ASan+UBSan for real memory-safety detection.
    # Falls back silently to the plain binary if sanitizers aren't available.
    bin_path = bin_plain
    comp_san = subprocess.run([CC] + SANFLAGS + [harness_path] + target_cs + ["-o", bin_san],
                               capture_output=True, text=True)
    if comp_san.returncode == 0:
        bin_path = bin_san

    list_res = subprocess.run([bin_path, "list"], capture_output=True, text=True)
    if list_res.returncode != 0:
        print_fail("Failed to retrieve test indices configuration.")
        shutil.rmtree(tmp_dir)
        return 0, (0, 0)

    tests = []
    for line in list_res.stdout.strip().split("\n"):
        if US in line:
            t_id, t_cat, t_name = line.split(US, 2)
            tests.append((t_id, t_cat, t_name))

    core_pass = core_total = 0
    trap_pass = trap_total = 0

    for t_id, t_cat, t_name in tests:
        run_bin = bin_plain if (ex_id, t_id) in FORCE_PLAIN else bin_path
        try:
            test_res = subprocess.run([run_bin, t_id], capture_output=True, text=True, timeout=5.0, errors="replace")
            if test_res.returncode != 0:
                _report_crash(t_name, t_cat, test_res.returncode, test_res.stderr)
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
            print_fail(f"{tag(t_cat)} {t_name} -> Timeout (5s) expired -- possible infinite loop/recursion.")
            if t_cat == "CORE":
                core_total += 1
            else:
                trap_total += 1

    shutil.rmtree(tmp_dir)
    score = int((core_pass / core_total) * 100) if core_total > 0 else 0
    return score, (trap_pass, trap_total)


def _report_crash(t_name, t_cat, code, stderr):
    if code < 0:
        reason = f"terminated by signal {-code} (likely a crash: segfault, abort, etc.)"
    else:
        reason = f"exited with status {code}"
    crash_info = ""
    stderr = (stderr or "").strip()
    if "ERROR: LeakSanitizer" in stderr:
        # Pull the leak summary + the first allocation-site frame (the line
        # naming the actual malloc call in the student's own source file, not
        # deep libc/runtime frames) so the message points somewhere useful.
        lines = stderr.split("\n")
        summary = next((l for l in lines if "byte(s) leaked" in l or "detected memory leaks" in l), "")
        alloc_frame = next((l.strip() for l in lines if ".c:" in l and "#" in l), "")
        detail = " -- ".join(x for x in [summary.strip(), alloc_frame] if x)
        crash_info = f" -- LEAK: {detail[:200]}" if detail else " -- memory leak detected (LeakSanitizer)"
        reason = "exited reporting a memory leak"
    elif "ERROR: AddressSanitizer" in stderr or "runtime error" in stderr:
        first_line = next((l for l in stderr.split("\n") if "ERROR" in l or "runtime error" in l), "")
        crash_info = f" -- {first_line.strip()[:160]}"
    print_fail(f"{tag(t_cat)} {t_name} -> Process {reason}.{crash_info}")
    if "LEAK" in crash_info:
        print(f"  └── Hint     : {C_YELLOW}Every malloc() on a path that returns/breaks out early needs a matching free() (or must not allocate at all before bailing). Trace the allocation site named above and check every return path after it.{C_RESET}")
    elif t_cat == "TRAP":
        print(f"  └── Hint     : {C_YELLOW}This is an adversarial/edge case, not officially graded -- but a crash here usually points to signed overflow, an out-of-bounds write, or writing through a pointer that should be read-only. See the WHY/HINT for this specific test above for the bug class targeted.{C_RESET}")


def main():
    print(f"{C_WHITE}{C_BOLD}=========================================================")
    print("        42 PISCINE C07 - ADVERSARIAL / VERBOSE TESTER    ")
    print("=========================================================")
    print(f"{C_RESET}{C_DIM}CORE  = tests a rule stated in the subject; counts toward score/rank.")
    print(f"TRAP  = adversarial edge case (INT_MIN overflow, writing through a")
    print(f"        read-only input, etc); informational only, never affects score.{C_RESET}")

    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    sorted_exercises = sorted(HARNESSES.keys())
    if args:
        sorted_exercises = [a for a in sorted_exercises if a in args]
        if not sorted_exercises:
            print_fail(f"No matching exercises for: {args}")
            return

    results = []

    for ex in sorted_exercises:
        c_files, harness = HARNESSES[ex]
        score, (tpass, ttotal) = run_exercise_tests(ex, c_files, harness)
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
