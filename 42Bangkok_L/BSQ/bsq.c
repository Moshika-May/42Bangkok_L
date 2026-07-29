/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bsq.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 17:17:48 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/29 17:37:26 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "bsq.h"

void	fill_bsq(char **grid, int *max, char fill)
{
	int	i;
	int	j;
	int	size;

	size = max[0];
	i = max[1] - size + 1;
	while (i <= max[1])
	{
		j = max[2] - size + 1;
		while (j <= max[2])
		{
			grid[i][j] = fill;
			j++;
		}
		i++;
	}
}

void	compute_cell(int **dp, char **g, char *cfg, int *c)
{
	int	i;
	int	j;

	i = c[0];
	j = c[1];
	if (g[i][j] == cfg[1])
		dp[i][j] = 0;
	else if (i == 0 || j == 0)
		dp[i][j] = 1;
	else
		dp[i][j] = min3(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1;
}

void	bsq(char **grid, int m, int n, char *cfg)
{
	int	**dp;
	int	max[3];
	int	c[2];

	dp = alloc_dp(m, n);
	if (!dp)
		return ;
	max[0] = 0;
	c[0] = -1;
	while (++c[0] < m)
	{
		c[1] = -1;
		while (++c[1] < n)
		{
			compute_cell(dp, grid, cfg, c);
			if (dp[c[0]][c[1]] > max[0])
			{
				max[0] = dp[c[0]][c[1]];
				max[1] = c[0];
				max[2] = c[1];
			}
		}
	}
	fill_bsq(grid, max, cfg[2]);
	free_dp(dp, m);
}
