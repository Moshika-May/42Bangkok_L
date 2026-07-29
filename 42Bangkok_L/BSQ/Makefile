# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/07/29 17:33:57 by kmahanin          #+#    #+#              #
#    Updated: 2026/07/29 17:34:11 by kmahanin         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = bsq
CC = cc
CFLAGS = -Wall -Wextra -Werror

SRCS = main.c bsq.c parse.c dp.c utils.c validate.c
OBJS = $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) -o $(NAME) $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
