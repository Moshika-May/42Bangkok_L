NAME = rush-02
CC = gcc
CFLAGS = -Wall -Wextra -Werror

SRC = main.c \
		input_validation.c \
		ft_putstr.c \
		ll_helper.c \
		utils.c \
		parse.c \
		convert.c \
		validate.c \
		convert_utils.c

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
