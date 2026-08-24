/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rush02.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/11 00:22:12 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/11 17:08:21 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

/*
void	rush(int x, int y)s
{
	int	a;
	int	b;

	b = 1;
	while (b <= y)
	{
		a = 1;
		while (a <= x)
		{
			if (b == 1 && (a == 1 || a == x))
				ft_putchar('A');
			else if (((b == 1 || b == y) && (a > 1 && a < x)) || ((b > 1
						&& b < y) && (a == 1 || a == x)))
				ft_putchar('B');
			else if (b == y && (a == 1 || a == x))
				ft_putchar('C');
			else if (((b > 1 && b < y) && (a > 1 && a < x)))
				ft_putchar(' ');
			a++;
		}
		ft_putchar('\n');
		b++;
	}
}
*/
void	rush02(int x, int y)
{
	int	a;
	int	b;

	b = 1;
	while (b <= y)
	{
		a = 1;
		while (a <= x)
		{
			if (b == 1 && (a == 1 || a == x))
				ft_putchar('A');
			else if (((b == 1 || b == y) && (a > 1 && a < x)) || ((b > 1
						&& b < y) && (a == 1 || a == x)))
				ft_putchar('B');
			else if (b == y && (a == 1 || a == x))
				ft_putchar('C');
			else if (((b > 1 && b < y) && (a > 1 && a < x)))
				ft_putchar(' ');
			a++;
		}
		ft_putchar('\n');
		b++;
	}
}
