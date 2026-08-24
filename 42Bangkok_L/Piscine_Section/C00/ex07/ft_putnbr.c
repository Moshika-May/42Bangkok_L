/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/15 13:42:53 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/15 15:41:03 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int	condition(int nb)
{
	if (nb == -2147483648)
	{
		write(1, "-2147483648", 11);
		return (-1);
	}
	if (nb < 0)
	{
		write(1, "-", 1);
		return (-nb);
	}
	if (nb == 0)
	{
		write(1, "0", 1);
		return (-1);
	}
	return (nb);
}

void	ft_putnbr(int nb)
{
	char	n;
	int		i;
	int		j;

	i = 1;
	nb = condition(nb);
	if (nb < 0)
		return ;
	while (nb / i >= 10)
	{
		i *= 10;
	}
	while (i > 0)
	{
		j = nb / i;
		n = j + '0';
		write(1, &n, 1);
		nb %= i;
		i /= 10;
	}
}
/*
int	main(void)
{
	ft_putnbr(-4422);
	return (0);
}
*/