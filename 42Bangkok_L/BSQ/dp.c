/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dp.c                                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 17:18:24 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/29 17:37:42 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "bsq.h"

int	**alloc_dp(int m, int n)
{
	int	**dp;
	int	i;

	dp = (int **)malloc(sizeof(int *) * m);
	if (!dp)
		return (NULL);
	i = 0;
	while (i < m)
	{
		dp[i] = (int *)malloc(sizeof(int) * n);
		if (!dp[i])
			return (NULL);
		i++;
	}
	return (dp);
}

void	free_dp(int **dp, int m)
{
	int	i;

	i = 0;
	while (i < m)
	{
		free(dp[i]);
		i++;
	}
	free(dp);
}
