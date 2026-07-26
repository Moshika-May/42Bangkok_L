/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   validate.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ataweech <ataweech@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 19:52:13 by ataweech          #+#    #+#             */
/*   Updated: 2026/07/26 20:42:20 by ataweech         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rush02.h"

static int	check_tens_ones(char *chunk, t_list *dict)
{
	char	key[3];

	key[2] = '\0';
	if (chunk[1] == '1')
	{
		key[0] = chunk[1];
		key[1] = chunk[2];
		return (get_value(dict, key) != NULL);
	}
	if (chunk[1] > '1')
	{
		key[0] = chunk[1];
		key[1] = '0';
		if (!get_value(dict, key))
			return (0);
	}
	key[0] = chunk[2];
	key[1] = '\0';
	if (chunk[2] > '0' && !get_value(dict, key))
		return (0);
	return (1);
}

int	check_chunk_keys(char *chunk, t_list *dict)
{
	char	key[2];

	if (chunk[0] > '0')
	{
		key[0] = chunk[0];
		key[1] = '\0';
		if (!get_value(dict, key) || !get_value(dict, "100"))
			return (0);
	}
	return (check_tens_ones(chunk, dict));
}

int	validate_all_keys(char *num_str, t_list *dict, int group_count)
{
	int		g;
	char	chunk[4];
	char	*mult_key;

	g = group_count;
	while (g > 0)
	{
		get_chunk(num_str, g, group_count, chunk);
		if (chunk[0] != '0' || chunk[1] != '0' || chunk[2] != '0')
		{
			if (!check_chunk_keys(chunk, dict))
				return (0);
			mult_key = get_multiplier(g - 1);
			if (mult_key && !get_value(dict, mult_key))
			{
				free(mult_key);
				return (0);
			}
			free(mult_key);
		}
		g--;
	}
	return (1);
}
