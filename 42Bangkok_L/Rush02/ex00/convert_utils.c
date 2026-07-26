/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   convert_utils.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ataweech <ataweech@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 19:52:13 by ataweech          #+#    #+#             */
/*   Updated: 2026/07/26 20:42:37 by ataweech         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rush02.h"

char	*get_multiplier(int magnitude)
{
	char	*mult;
	int		i;

	if (magnitude == 0)
		return (NULL);
	mult = malloc(sizeof(char) * (magnitude * 3 + 2));
	if (!mult)
		return (NULL);
	mult[0] = '1';
	i = 1;
	while (i <= magnitude * 3)
	{
		mult[i] = '0';
		i++;
	}
	mult[i] = '\0';
	return (mult);
}

void	print_word(char *word, int *first_word)
{
	if (!word)
		return ;
	if (!(*first_word))
		ft_putstr(" ");
	ft_putstr(word);
	*first_word = 0;
}

int	handle_zero(t_list *dict)
{
	if (!get_value(dict, "0"))
		return (0);
	ft_putstr(get_value(dict, "0"));
	ft_putstr("\n");
	return (1);
}

static void	print_tens_ones(char *chunk, t_list *dict, int *first)
{
	char	key[3];

	key[2] = '\0';
	if (chunk[1] == '1')
	{
		key[0] = chunk[1];
		key[1] = chunk[2];
		print_word(get_value(dict, key), first);
		return ;
	}
	if (chunk[1] > '1')
	{
		key[0] = chunk[1];
		key[1] = '0';
		print_word(get_value(dict, key), first);
	}
	key[0] = chunk[2];
	key[1] = '\0';
	if (chunk[2] > '0')
		print_word(get_value(dict, key), first);
}

void	print_chunk(char *chunk, t_list *dict, int *first)
{
	char	key[3];

	if (chunk[0] > '0')
	{
		key[0] = chunk[0];
		key[1] = '\0';
		key[2] = '\0';
		print_word(get_value(dict, key), first);
		print_word(get_value(dict, "100"), first);
	}
	print_tens_ones(chunk, dict, first);
}
