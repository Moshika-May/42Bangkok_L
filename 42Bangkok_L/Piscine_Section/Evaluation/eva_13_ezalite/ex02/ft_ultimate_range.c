/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_ultimate_range.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ezalite <ezalite@student.42bangkok>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/21 23:38:02 by ezalite           #+#    #+#             */
/*   Updated: 2026/07/22 01:59:25 by ezalite          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

int	ft_ultimate_range(int **range, int min, int max)
{
	int	i;

	if (min >= max)
	{
		*range = 0;
		return (0);
	}
	*range = malloc(sizeof (int) * (max - min));
	if (!(*range))
	{
		return (-1);
	}
	i = 0;
	while (i < max - min)
	{
		(*range)[i] = min + i;
		i++;
	}
	return (i);
}
/*
#include <stdio.h>

int	main(void)
{
	int	**array;
	int	min;
	int	max;

	array = malloc(sizeof (int *));
	min = 20;
	max = 40;
	printf("%d\n", ft_ultimate_range(array, min, max));
	if (!*array)
		printf("Hell it returned a null pointer\n");
	else
	{
		printf("%d\n", (*array)[0]);
		printf("%d\n", (*array)[max - min - 1]);
	}
	return (0);
}*/
