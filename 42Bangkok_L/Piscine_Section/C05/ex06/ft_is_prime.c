/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_is_prime.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/23 13:49:16 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/24 00:15:13 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_is_prime(int nb)
{
	unsigned int	i;

	if (nb <= 1)
		return (0);
	if (nb == 2)
		return (1);
	if (nb % 2 == 0)
		return (0);
	i = 3;
	while (i <= nb / i)
	{
		if (nb % i == 0)
			return (0);
		i += 2;
	}
	return (1);
}
/*
#include <stdio.h>
#include <stdlib.h>

int	main(int argc, const char **argv)
{
	if (argc != 2)
		return (0);
	printf("%d\n", ft_is_prime(atoi(argv[1])));
	return (0);
}
*/
