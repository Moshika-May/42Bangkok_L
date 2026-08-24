/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_range.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hzheng2 <hzheng2@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/22 11:36:51 by hzheng2           #+#    #+#             */
/*   Updated: 2026/07/25 10:54:53 by hzheng2          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <stdlib.h>

int	*ft_range(int min, int max)
{
	int	*ans;
	int	idx;

	idx = 0;
	if (min >= max)
		return (NULL);
	ans = (int *) malloc((max - min) * sizeof(int));
	if (ans == NULL)
		return (NULL);
	while (idx < (max - min))
	{
		*(ans + idx) = min + idx;
		idx++;
	}
	return (ans);
}
