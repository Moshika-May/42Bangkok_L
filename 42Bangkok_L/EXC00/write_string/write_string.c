#include <unistd.h>

void	write_string(char *str)
{
	int	n;
	char	a;

	n = 0;
	a = str[0];
	if (a == ' ')
	{
		while (str[n] != '\0')
		{
			write(1, str, 1);
			n++;
		}
	}
	else
	{
		write(1, str, 1);
	}
	write(1, "\n", 1);
}

int	main(void)
{
	write_string("          ");
	write_string("weg2");
}

// >          $
// >          $
// \ no new in files$
