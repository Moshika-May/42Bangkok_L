# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/07/29 22:40:53 by kmahanin          #+#    #+#              #
#    Updated: 2026/07/29 22:47:09 by kmahanin         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME		= libft.a

CC			= cc
CFLAGS		= -Wall -Wextra -Werror
INCLUDES	= -Iincludes
AR			= ar rcs
RM			= rm -f

SRCS		= srcs/ft_putchar.c \
			  srcs/ft_swap.c \
			  srcs/ft_putstr.c \
			  srcs/ft_strlen.c \
			  srcs/ft_strcmp.c

OBJS		= $(SRCS:.c=.o)

HEADER		= includes/ft.h

all: $(NAME)

$(NAME): $(OBJS)
	$(AR) $(NAME) $(OBJS)

srcs/%.o: srcs/%.c $(HEADER)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
	$(RM) $(OBJS)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
