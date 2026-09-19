*This project has been created as part of the 42 curriculum by kmahanin.*

# Libft

## Description

**Libft** is a custom C library built as part of the 42 core curriculum. The goal of the
project is to recreate a set of standard C library functions from scratch, understand
how they work internally, and assemble them — along with a set of additional
utility functions and a linked list toolkit — into a static library (`libft.a`) that can
be reused in future C projects at 42.

The library is organized into three parts:

- **Part 1 — Libc functions**: reimplementations of standard `libc` functions
  (e.g. `strlen`, `memcpy`, `strchr`, `atoi`, `calloc`, `strdup`, etc.), each
  prefixed with `ft_` and matching the original's prototype and behavior.
- **Part 2 — Additional functions**: extra string/utility helpers not found in
  the standard library, such as `ft_split`, `ft_itoa`, `ft_strtrim`, `ft_strjoin`,
  `ft_strmapi`, `ft_striteri`, and file-descriptor output helpers
  (`ft_putstr_fd`, `ft_putnbr_fd`, etc.).
- **Part 3 — Linked lists**: a minimal singly linked list implementation
  (`t_list`) with functions to create, add, iterate, map, and free nodes
  (`ft_lstnew`, `ft_lstadd_back`, `ft_lstmap`, `ft_lstclear`, etc.).

## Instructions

### Compilation

Build the static library with:

```bash
make
```
This compiles every `ft_*.c` source file with `-Wall -Wextra -Werror` and archives
the resulting object files into `libft.a` using `ar`.

Other available Makefile rules:

```bash
make all      # same as `make`, builds libft.a
make clean    # removes object files
make fclean   # removes object files and libft.a
make re       # fclean + all
```

### Using the library in another project

1. Copy the `libft` folder (with its `Makefile`, `libft.h`, and `ft_*.c` files) into
   your project.
2. Compile it with `make -C libft` (or by adding a rule to your own Makefile that
   calls into the `libft` Makefile).
3. Include the header and link against the archive when compiling your project:

```bash
cc your_files.c -Ilibft -Llibft -lft -o your_program
```

## Library overview

`libft.h` declares every function in the library along with the `t_list` structure:

```c
typedef struct s_list
{
    void            *content;
    struct s_list   *next;
}   t_list;
```

| Category | Examples |
|---|---|
| Character checks | `ft_isalpha`, `ft_isdigit`, `ft_isalnum`, `ft_isascii`, `ft_isprint` |
| Memory | `ft_memset`, `ft_bzero`, `ft_memcpy`, `ft_memmove`, `ft_memchr`, `ft_memcmp`, `ft_calloc` |
| Strings | `ft_strlen`, `ft_strlcpy`, `ft_strlcat`, `ft_strchr`, `ft_strrchr`, `ft_strncmp`, `ft_strnstr`, `ft_strdup`, `ft_atoi` |
| String building | `ft_substr`, `ft_strjoin`, `ft_strtrim`, `ft_split`, `ft_itoa`, `ft_strmapi`, `ft_striteri` |
| Output (fd) | `ft_putchar_fd`, `ft_putstr_fd`, `ft_putendl_fd`, `ft_putnbr_fd` |
| Linked lists | `ft_lstnew`, `ft_lstadd_front`, `ft_lstadd_back`, `ft_lstsize`, `ft_lstlast`, `ft_lstdelone`, `ft_lstclear`, `ft_lstiter`, `ft_lstmap` |

Each function follows the same prototype and behavior as its standard-library
counterpart (where applicable), and helper functions used internally are declared
`static` to keep them file-scoped.

## Resources

- [The Linux man pages](https://man7.org/linux/man-pages/man3) — reference for the
  behavior/prototypes of the original libc functions being reimplemented
- [FreeBSD](https://man.freebsd.org/cgi/man.cgi) — for reference prototypes/behavior of libc functions

- 42's own Libft subject PDF and intranet documentation

### AI usage

AI was used only to help draft this `README.md` file. AI was used to do Q/A of each functions about how it work how it giving example of use and also asking about edge case for further understanding.
