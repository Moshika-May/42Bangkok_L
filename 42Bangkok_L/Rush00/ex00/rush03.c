void	rush(int x, int y)
{	
	int	a;
	int	b;

	a = 0;
	b = 0;
	while (b <= y)
	{
		while (a <= x)
		{
			if (a == 0)
				ft_putchar('A');
			else if (a == x)
				ft_putchar('C')
			else if (b == 0 ||  a == 0 || b == y )
				ft_putchar('B')
		}
	}
}
