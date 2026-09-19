/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/16 18:20:14 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/19 15:20:36 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// #include <stdio.h>
#include "libft.h"

int	ft_atoi(const char *nptr)
{
	unsigned int	i;
	int				j;
	int				k;

	i = 0;
	j = 1;
	k = 0;
	while (nptr[i] == ' ' || (nptr[i] >= '\t' && nptr[i] <= '\r'))
		i++;
	if (nptr[i] == '+' || nptr[i] == '-')
	{
		if (nptr[i] == '-')
			j = -j;
		i++;
	}
	while (nptr[i] >= '0' && nptr[i] <= '9')
	{
		k = (k * 10) + (nptr[i] - '0');
		i++;
	}
	return (k * j);
}
/*
int	main(int argc, char *argv[])
{
	if (argc == 2)
		printf("%d", ft_atoi(argv[1]));
	return (0);
}
*/
