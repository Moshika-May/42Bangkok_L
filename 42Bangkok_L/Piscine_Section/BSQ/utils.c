/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 17:18:47 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/29 17:37:56 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "bsq.h"

int	min2(int a, int b)
{
	if (a < b)
		return (a);
	return (b);
}

int	min3(int a, int b, int c)
{
	return (min2(min2(a, b), c));
}

int	ft_atoi(char *str)
{
	int	res;

	res = 0;
	while (*str >= '0' && *str <= '9')
	{
		res = res * 10 + (*str - '0');
		str++;
	}
	return (res);
}

void	print_and_free(char **grid, int m, int n)
{
	int	i;

	i = 0;
	while (i < m)
	{
		write(1, grid[i], n);
		write(1, "\n", 1);
		free(grid[i]);
		i++;
	}
	free(grid);
}
