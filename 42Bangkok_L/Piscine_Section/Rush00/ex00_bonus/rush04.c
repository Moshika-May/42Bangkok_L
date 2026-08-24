/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rush04.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/11 01:39:52 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/11 04:11:40 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

void	ft_putchar(char c);
/*
void	putchar_closelid(int a, int b, int x, int y)
{
	if (((b == 1 || b == y) && (a > 1 && a < x)) || ((b > 1 && b < y) && (a == 1
				|| a == x)))
		ft_putchar('B');
	else if (((b > 1 && b < y) && (a > 1 && a < x)))
		ft_putchar(' ');
}

void	rush(int x, int y)
{
	int	a;
	int	b;
	int	c;

	c = 0;
	b = 1;
	while (b <= y)
	{
		a = 1;
		while (a <= x)
		{
			if ((a == 1 && b == 1) || ((a == x && b == y) && c <= 0))
			{
				ft_putchar('A');
				if (y == 1 || x == 1)
					c++;
			}
			else if ((a == x && b == 1) || (a == 1 && b == y))
				ft_putchar('C');
			putchar_closelid(a, b, x, y);
			a++;
		}
		ft_putchar('\n');
		b++;
	}
}
*/

void	putchar_closelid04(int a, int b, int x, int y)
{
	if (((b == 1 || b == y) && (a > 1 && a < x)) || ((b > 1 && b < y) && (a == 1
				|| a == x)))
		ft_putchar('B');
	else if (((b > 1 && b < y) && (a > 1 && a < x)))
		ft_putchar(' ');
}

void	rush04(int x, int y)
{
	int	a;
	int	b;
	int	c;

	c = 0;
	b = 1;
	while (b <= y)
	{
		a = 1;
		while (a <= x)
		{
			if ((a == 1 && b == 1) || ((a == x && b == y) && c <= 0))
			{
				ft_putchar('A');
				if (y == 1 || x == 1)
					c++;
			}
			else if ((a == x && b == 1) || (a == 1 && b == y))
				ft_putchar('C');
			putchar_closelid04(a, b, x, y);
			a++;
		}
		ft_putchar('\n');
		b++;
	}
}
