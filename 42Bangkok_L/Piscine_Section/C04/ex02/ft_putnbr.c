/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/15 13:42:53 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/16 22:20:08 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int	cond_check(long n)
{
	if (n < 0)
	{
		write(1, "-", 1);
		return (0);
	}
	if (n == 0)
	{
		write(1, "0", 1);
		return (1);
	}
	return (0);
}

void	ft_putnbr(int nb)
{
	char			b[20];
	unsigned int	i;
	long			n;

	n = nb;
	i = 0;
	if (cond_check(n) == 1)
		return ;
	if (n < 0)
		n = -n;
	while (n > 0)
	{
		b[i] = (n % 10) + '0';
		n /= 10;
		i++;
	}
	while (i > 0)
	{
		i--;
		write(1, &b[i], 1);
	}
}
/*
int	main(void)
{
	ft_putnbr(2147483647);
	return (0);
}
*/
