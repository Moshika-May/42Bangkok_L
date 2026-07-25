/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_ultimate_range.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hzheng2 <hzheng2@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/22 14:25:06 by hzheng2           #+#    #+#             */
/*   Updated: 2026/07/25 13:04:32 by hzheng2          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <stdlib.h>

int	ft_ultimate_range(int **range, int min, int max)
{
	int	idx;

	idx = 0;
	if (min >= max)
	{
		*range = NULL;
		return (0);
	}
	*range = (int *) malloc(sizeof(int) * (max - min));
	if (*range == NULL)
	{
		*range = NULL;
		return (-1);
	}
	while (idx < (max - min))
	{
		*((*range) + idx) = min + idx;
		idx++;
	}
	return (max - min);
}
