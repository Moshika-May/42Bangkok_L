/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strs_to_tab.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/23 11:52:09 by mbury             #+#    #+#             */
/*   Updated: 2026/07/23 16:57:02 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_stock_str.h"
#include <stdlib.h>

int ft_strlen(char *str)
{
	int i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

char	*ft_strdup(char *src)
{
	int		len;
	char	*dup;
	char	*ptr;

	len = 0;
	while (src[len])
		len++;
	dup = malloc(sizeof(char) * (len + 1));
	if (dup == NULL)
		return (NULL);
	ptr = dup;
	while (*src)
		*dup++ = *src++;
	*dup = '\0';
	return (ptr);
}

struct s_stock_str	*ft_strs_to_tab(int ac, char **av)
{
	int			i;
	int			len;
	t_stock_str	*array;

	array = malloc(sizeof(t_stock_str) * (ac + 1));
	i = 0;
	while (i < ac)
	{
		array[i].size = ft_strlen(av[i]);
		array[i].str = av[i];
		array[i].copy = ft_strdup(av[i]);
		if (array[i].copy == NULL)
			return (NULL);
		i++;
	}
	array[i].str = 0;
	return (array);
}
