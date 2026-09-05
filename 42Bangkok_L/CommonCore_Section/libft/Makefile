# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/09/04 10:19:17 by kmahanin          #+#    #+#              #
#    Updated: 2026/09/06 01:20:23 by kmahanin         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME        = libft.a

CC          = cc
CFLAGS      = -Wall -Wextra -Werror
INCLUDES    = -I.
AR          = ar rcs
RM          = rm -f

SRCS        = ft_atoi.c \
ft_isdigit.c \
ft_strdup.c \
ft_strlen.c \
ft_isalnum.c \
ft_isprint.c \
ft_strlcat.c \
ft_strncmp.c \
ft_isalpha.c \
ft_memset.c \
ft_strlcpy.c \
ft_isascii.c \
ft_bzero.c \
ft_memmove.c \
ft_toupper.c \
ft_tolower.c

OBJS        = $(SRCS:.c=.o)
HEADER      = libft.h

all: $(NAME)

$(NAME): $(OBJS)
	$(AR) $(NAME) $(OBJS)

%.o: %.c $(HEADER)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
	$(RM) $(OBJS)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
