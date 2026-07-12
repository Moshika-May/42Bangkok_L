/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rush00.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: miazanov <miazanov@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/11 00:22:12 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/12 20:50:44 by miazanov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

void	ft_putchar(char c);

void	rush(int x, int y)
{
	int	a;
	int	b;

	b = 1;
	while (b <= y)
	{
		a = 1;
		while (a <= x)
		{
			if ((b == 1 || b == y) && a == 1)
				ft_putchar('o');
			else if ((b == 1 || b == y) && (a > 1 && a < x))
				ft_putchar('-');
			else if ((b > 1 && b < y) && (a == 1 || a == x))
				ft_putchar('|');
			else if ((b == 1 || b == y) && a == x)
				ft_putchar('o');
			else if (((b > 1 && b < y) && (a > 1 && a < x)))
				ft_putchar(' ');
			a++;
		}
		ft_putchar('\n');
		b++;
	}
}
