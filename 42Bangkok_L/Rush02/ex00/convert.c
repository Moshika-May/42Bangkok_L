/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   convert.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ataweech <ataweech@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 19:52:13 by ataweech          #+#    #+#             */
/*   Updated: 2026/07/26 20:42:50 by ataweech         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rush02.h"

void	get_chunk(char *str, int g, int g_count, char *chunk)
{
	int	len;
	int	slen;
	int	start;
	int	i;

	len = ft_strlen(str);
	slen = 3;
	if (g == g_count)
		slen = len - (g_count - 1) * 3;
	start = len - (g - 1) * 3 - slen;
	chunk[0] = '0';
	chunk[1] = '0';
	chunk[2] = '0';
	chunk[3] = '\0';
	i = 0;
	while (i < slen)
	{
		chunk[3 - slen + i] = str[start + i];
		i++;
	}
}

static void	print_group(char *num, t_list *dict, int g, int *first)
{
	char	chunk[4];
	char	*mult_key;

	get_chunk(num, g, (ft_strlen(num) + 2) / 3, chunk);
	if (chunk[0] != '0' || chunk[1] != '0' || chunk[2] != '0')
	{
		print_chunk(chunk, dict, first);
		mult_key = get_multiplier(g - 1);
		if (mult_key)
		{
			print_word(get_value(dict, mult_key), first);
			free(mult_key);
		}
	}
}

int	convert_number(char *num_str, t_list *dict)
{
	int	g_count;
	int	first;
	int	g;

	while (*num_str == '0' && *(num_str + 1) != '\0')
		num_str++;
	if (num_str[0] == '0' && num_str[1] == '\0')
		return (handle_zero(dict));
	g_count = (ft_strlen(num_str) + 2) / 3;
	if (!validate_all_keys(num_str, dict, g_count))
		return (0);
	first = 1;
	g = g_count;
	while (g > 0)
	{
		print_group(num_str, dict, g, &first);
		g--;
	}
	ft_putstr("\n");
	return (1);
}
