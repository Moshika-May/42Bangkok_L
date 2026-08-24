/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_iterative_power.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/22 21:31:51 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/26 11:51:18 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_iterative_power(int nb, int power)
{
	int	a;

	a = nb;
	if (power == 0 || (nb == 0 && power == 0))
		return (1);
	else if (power < 0 || (nb == 0 && power != 0))
		return (0);
	while (power > 1)
	{
		a *= nb;
		power--;
	}
	return (a);
}
/*
#include <stdio.h>
#include <stdlib.h>

int	main(int argc, char **argv)
{
	if (argc != 3)
		return (0);
	printf("%d\n", ft_iterative_power(atoi(argv[1]), atoi(argv[2])));
	return (0);
}
*/
