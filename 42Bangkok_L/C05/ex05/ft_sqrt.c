/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sqrt.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/23 11:54:08 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/24 00:14:34 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
/*
int	ft_sqrt(int nb)
{
	int	i;

	if (nb <= 0)
		return (0);
	if (nb == 1)
		return (1);
	if (nb % 10 == 2 || nb % 10 == 3 || nb % 10 == 7 || nb % 10 == 8)
		return (0);
	if (nb % 3 == 2)
		return (0);
	if (nb % 4 == 2 || nb % 4 == 3)
		return (0);
	if (nb % 9 != 0 && nb % 9 != 1 && nb % 9 != 4 && nb % 9 != 7)
		return (0);
	if (nb % 16 != 0 && nb % 16 != 1 && nb % 16 != 4 && nb % 16 != 9)
		return (0);
	i = 1;
	while (i * i <= nb)
	{
		if (i * i == nb)
			return (i);
		i++;
	}
	return (0);
}
*/

int	ft_sqrt(int nb)
{
	int	i;

	if (nb <= 0)
		return (0);
	if (nb == 1)
		return (1);
	i = ft_sqrt(nb / 4);
	if (i > 0)
		i *= 2;
	while (i * i <= nb)
	{
		if (i * i == nb)
			return (i);
		i++;
	}
	return (0);
}
/*
#include <stdio.h>
#include <stdlib.h>

int	main(int argc, char **argv)
{
	if (argc != 2)
		return (0);
	printf("%d\n", ft_sqrt(atoi(argv[1])));
	return (0);
}
*/
