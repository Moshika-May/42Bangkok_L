/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_find_next_prime.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sguigui <sguigui@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/25 13:37:06 by sguigui           #+#    #+#             */
/*   Updated: 2026/07/25 13:42:17 by sguigui          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <unistd.h>

int	ft_is_prime(int nb)
{
	int	i;

	if (nb <= 1)
		return (0);
	i = 2;
	while (i <= nb / i)
	{
		if (nb % i == 0)
			return (0);
		i++;
	}
	return (1);
}

int	ft_find_next_prime(int nb)
{
	if (nb <= 2)
		return (2);
	while (!ft_is_prime(nb))
	{
		nb++;
	}
	return (nb);
}
