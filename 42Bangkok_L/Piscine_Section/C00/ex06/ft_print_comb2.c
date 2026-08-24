/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_comb2.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/15 00:45:55 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/15 13:38:13 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	cal_print(unsigned int a, unsigned int b)
{
	char	i;
	char	j;
	char	k;
	char	l;

	i = (a / 10) + '0';
	j = (a % 10) + '0';
	k = (b / 10) + '0';
	l = (b % 10) + '0';
	write(1, &i, 1);
	write(1, &j, 1);
	write(1, " ", 1);
	write(1, &k, 1);
	write(1, &l, 1);
}

void	ft_print_comb2(void)
{
	unsigned int	a;
	unsigned int	b;

	a = 0;
	while (a <= 98)
	{
		b = a + 1;
		while (b <= 99)
		{
			cal_print(a, b);
			if (a != 98 || b != 99)
				write(1, ", ", 2);
			b++;
		}
		a++;
	}
}
/*
int	main(void)
{
	ft_print_comb2();
	return (0);
}
*/
