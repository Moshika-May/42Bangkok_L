/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strs_to_tab.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 20:41:44 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/29 21:46:42 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>
#include <stdlib.h>

int	len(char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

char	*strdupli(char *src)
{
	int		i;
	char	*dest;

	dest = (char *)malloc(sizeof(char) * (len(src) + 1));
	if (!dest)
		return (NULL);
	i = 0;
	while (src[i])
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = '\0';
	return (dest);
}

struct s_stock_str	*ft_strs_to_tab(int ac, char **av)
{
	t_stock_str	*var;
	int			i;

	i = 0;
	var = (t_stock_str *)malloc(sizeof(t_stock_str) * (ac + 1));
	if (!var)
		return (NULL);
	while (i < ac)
	{
		var[i].size = len(av[i]);
		var[i].str = av[i];
		var[i].copy = strdupli(av[i]);
		if (!var[i].copy)
		{
			while (--i >= 0)
				free(var[i].copy);
			free(var);
			return (NULL);
		}
		i++;
	}
	var[i].str = 0;
	return (var);
}
