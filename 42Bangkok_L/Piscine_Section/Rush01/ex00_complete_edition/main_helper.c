/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_helper.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/19 23:30:49 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/19 23:30:54 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

int	init_memory(int ***grid, int **clues, int n)
{
	int	i;

	*clues = malloc(sizeof(int) * (n * 4));
	if (!*clues)
		return (1);
	*grid = malloc(sizeof(int *) * n);
	if (!*grid)
	{
		free(*clues);
		return (1);
	}
	i = 0;
	while (i < n)
	{
		(*grid)[i] = malloc(sizeof(int) * n);
		if (!(*grid)[i])
			return (1);
		i++;
	}
	return (0);
}

void	parse_clues(char *str, int *clues, int n)
{
	int	i;
	int	k;

	i = 0;
	k = 0;
	while (str[i] != '\0' && k < (n * 4))
	{
		if (str[i] >= '1' && str[i] <= '9')
		{
			clues[k] = str[i] - '0';
			k++;
		}
		i++;
	}
}

void	init_grid(int **grid, int n)
{
	int	i;
	int	j;

	i = 0;
	while (i < n)
	{
		j = 0;
		while (j < n)
		{
			grid[i][j] = 0;
			j++;
		}
		i++;
	}
}

void	free_memory(int **grid, int *clues, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		free(grid[i]);
		i++;
	}
	free(grid);
	free(clues);
}
