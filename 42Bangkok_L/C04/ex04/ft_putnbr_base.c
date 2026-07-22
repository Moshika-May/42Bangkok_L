/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_base.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/16 23:59:35 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/22 15:33:57 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	print_nbr(long n, char *base, int base_l)
{
	char	zam;

	if (n >= base_l)
		print_nbr(n / base_l, base, base_l);
	zam = base[n % base_l];
	write(1, &zam, 1);
}

int	base_check(char *base)
{
	unsigned int	i;
	unsigned int	j;

	i = 0;
	if (!base[0] || !base[1])
		return (0);
	while (base[i])
	{
		if (base[i] == '+' || base[i] == '-')
			return (0);
		j = i + 1;
		while (base[j])
		{
			if (base[i] == base[j])
				return (0);
			j++;
		}
		i++;
	}
	return (i);
}

void	ft_putnbr_base(int nbr, char *base)
{
	long	n;

	if (base_check(base) < 2)
		return ;
	n = nbr;
	if (n < 0)
	{
		write(1, "-", 1);
		n = -n;
	}
	print_nbr(n, base, base_check(base));
}
/*
#include <stdlib.h>

void	ft_putstr(char *str)
{
	int	i;

	i = 0;
	while (str[i])
	{
		write(1, &str[i], 1);
		i++;
	}
}

int	main(int argc, char **argv)
{
	if (argc != 3)
		return (1);
	ft_putstr(argv[1]);
	write(1, "\n", 1);
	ft_putstr(argv[2]);
	write(1, "\n", 1);
	ft_putnbr_base(atoi(argv[1]), argv[2]);
	write(1, "\n", 1);
	return (0);
}
*/
