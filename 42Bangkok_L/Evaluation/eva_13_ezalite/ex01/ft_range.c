/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_range.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ezalite <ezalite@student.42bangkok>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/21 23:27:16 by ezalite           #+#    #+#             */
/*   Updated: 2026/07/22 21:58:27 by ezalite          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

int	*ft_range(int min, int max)
{
	int	*range;
	int	i;

	if (min >= max)
	{
		return (0);
	}
	range = malloc(sizeof (int) * (max - min));
	if (!range)
	{
		return (0);
	}
	i = 0;
	while (i < max - min)
	{
		range[i] = min + i;
		i++;
	}
	return (range);
}
