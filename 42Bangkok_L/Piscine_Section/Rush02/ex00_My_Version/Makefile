# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/07/27 06:01:16 by kmahanin          #+#    #+#              #
#    Updated: 2026/07/27 06:05:49 by kmahanin         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = rush-02
CC = gcc
CFLAGS = -Wall -Wextra -Werror

SRC = main.c \
      input_validation.c \
      putstr.c \
      helper_func.c \
      parse_dict.c \
      convert.c

OBJ = $(SRC:.c=.o)

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(CFLAGS) -o $(NAME) $(OBJ)

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
