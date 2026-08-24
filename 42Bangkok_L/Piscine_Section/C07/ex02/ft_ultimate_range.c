/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_ultimate_range.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/25 23:58:26 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/26 00:18:11 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>
#include <stdlib.h>

int	ft_ultimate_range(int **range, int min, int max)
{
	unsigned int	i;
	int				*array;

	i = 0;
	if (min >= max)
	{
		*range = NULL;
		return (0);
	}
	array = (int *)malloc(sizeof(int) * (max - min));
	if (!array)
	{
		*range = NULL;
		return (-1);
	}
	while (max > min)
	{
		array[i] = min;
		i++;
		min++;
	}
	*range = array;
	return (i);
}
/*
#include <stdio.h>

int	main(int argc, char **argv)
{
	int	*arr;
	int	min;
	int	max;
	int	size;
	int	i;

	if (argc != 3)
	{
		printf("Usage: %s <min> <max>\n", argv[0]);
		printf("Example: %s 5 10\n", argv[0]);
		return (1);
	}
	min = atoi(argv[1]);
	max = atoi(argv[2]);
	size = ft_ultimate_range(&arr, min, max);
	printf("ft_ultimate_range(&arr, %d, %d)\n", min, max);
	printf("Returned size: %d\n", size);
	if (size > 0 && arr != NULL)
	{
		printf("Array elements: ");
		i = 0;
		while (i < size)
		{
			printf("[%d] ", arr[i]);
			i++;
		}
		printf("\n");
		free(arr);
	}
	else if (size == 0 && arr == NULL)
	{
		printf("Result: *range set to NULL (min >= max).\n");
	}
	else
	{
		printf("Result: Malloc error (-1 returned).\n");
	}
return (0);
}
*/
