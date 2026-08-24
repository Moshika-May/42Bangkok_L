/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_iterative power.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sguigui <sguigui@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/25 12:29:26 by sguigui           #+#    #+#             */
/*   Updated: 2026/07/25 13:47:15 by sguigui          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <unistd.h>

int	ft_iterative_power(int nb, int power)
{
	int	i;
	int	result;

	if (power < 0)
		return (0);
	result = 1;
	i = 0;
	while (i < power)
	{
		result *= nb;
		i++;
	}
	return (result);
}
