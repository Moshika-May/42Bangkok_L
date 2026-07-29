/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   validate.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 17:36:18 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/29 17:36:21 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "bsq.h"

int	is_valid_cfg(char *cfg)
{
	int	i;

	i = 0;
	while (i < 3)
	{
		if (cfg[i] < 32 || cfg[i] > 126)
			return (0);
		i++;
	}
	if (cfg[0] == cfg[1] || cfg[0] == cfg[2] || cfg[1] == cfg[2])
		return (0);
	return (1);
}

int	check_line(char *line, int n, char *cfg)
{
	int	i;

	i = 0;
	while (line[i])
	{
		if (line[i] != cfg[0] && line[i] != cfg[1])
			return (0);
		i++;
	}
	if (i != n)
		return (0);
	return (1);
}
