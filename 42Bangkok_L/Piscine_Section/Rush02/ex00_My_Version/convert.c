/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   convert.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/27 05:58:27 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/27 14:27:06 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rsh02.h"

void	convert_number(unsigned __int128 n, t_dict *dict, int *first)
{
	int	i;

	i = 0;
	while (dict[i].val)
	{
		if (dict[i].nb <= n)
			break ;
		i++;
	}
	if (dict[i].nb >= 100)
	{
		convert_number(n / dict[i].nb, dict, first);
		if (!*first)
			write(1, " ", 1);
		*first = 0;
		putstr(dict[i].val);
		if (n % dict[i].nb != 0)
			convert_number(n % dict[i].nb, dict, first);
	}
	else
	{
		if (!*first)
			write(1, " ", 1);
		*first = 0;
		putstr(dict[i].val);
		if (n % dict[i].nb != 0)
			convert_number(n % dict[i].nb, dict, first);
	}
}
