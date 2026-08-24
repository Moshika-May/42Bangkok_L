/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: gamagalh <gamagalh@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/16 14:49:41 by gamagalh          #+#    #+#             */
/*   Updated: 2026/07/23 15:39:21 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int	ftrlog(int base, long int nbr, int *r)
{
	int	i;

	i = 0;
	if (nbr == 0)
	{
		r[0] = 0;
		return (1);
	}
	while (nbr > 0)
	{
		r[i] = nbr % base;
		nbr = nbr / base;
		i++;
	}
	return (i);
}

void	ft_putnbr(int nb)
{
	int			r[32];
	int			j;
	char		c;
	long int	num;

	num = nb;
	if (num < 0)
	{
		write(1, "-", 1);
		num = 0 - num;
	}
	if (num == 0)
	{
		write(1, "0", 1);
		return ;
	}
	j = ftrlog(10, num, r);
	j = j - 1;
	while (j >= 0)
	{
		c = 48 + r[j];
		write(1, &c, 1);
		j--;
	}
}

#include <stdlib.h>
int	main(int argc, char **argv)
{
	if (argc != 2)
		return (0);
	ft_putnbr(atoi(argv[1]));
	return (0);
}
