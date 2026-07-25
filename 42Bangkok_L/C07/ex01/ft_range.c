/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_range.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/25 23:16:13 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/25 23:57:34 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>
#include <stdlib.h>

int	*ft_range(int min, int max)
{
	unsigned int	i;
	unsigned int	n;
	int				*array;

	if (min >= max)
		return (NULL);
	n = max - min;
	array = (int *)malloc(sizeof(int) * n);
	if (!array)
		return (NULL);
	i = 0;
	while (n > i)
	{
		array[i] = min + i;
		i++;
	}
	return (array);
}
/*
#include <stdio.h>

int	main(int argc, char **argv)
{
	int	min;
	int	max;
	int	*ran;
	int	i;

	if (argc < 3)
		return (0);
	min = atoi(argv[1]);
	max = atoi(argv[2]);
	i = 0;
	ran = ft_range(min, max);
	if (!ran)
	{
		printf("NULL");
		return (0);
	}
	while (i < max - min)
	{
		printf("%d ", ran[i]);
		i++;
	}
	printf("\n");
	free(ran);
	return (0);
}
*/
