/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/13 00:20:07 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/14 13:39:02 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>
#include <unistd.h>

static int	ft_pow(int base, size_t n)
{
	int	result;

	result = 1;
	if (n == 0)
		return (1);
	while (n-- > 0)
		result *= base;
	return (result);
}

static size_t	xpown(long n)
{
	size_t	i;

	i = 0;
	if (n == 0)
		return (1);
	while (n > 0)
	{
		n /= 10;
		i++;
	}
	return (i);
}

void	ft_putnbr_fd(int n, int fd)
{
	long	i;
	char	j;
	size_t	k;

	i = n;
	if (n == 0)
	{
		write(fd, "0", 1);
		return ;
	}
	if (n < 0)
	{
		i = -(long)n;
		write(fd, "-", 1);
	}
	k = xpown(i);
	while (k > 0)
	{
		j = ((i / ft_pow(10, k - 1)) % 10) + '0';
		write(fd, &j, 1);
		k--;
	}
}
/*
#include <stdio.h>
#include <stdlib.h>

int	main(int ac, char **av)
{
	(void)ac;
	(void)ft_putnbr_fd(atoi(av[1]), 1);
	return (0);
}
*/
