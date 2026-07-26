/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   helper_func.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/24 22:39:22 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/26 14:05:45 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rsh02.h"

unsigned long long	atoull(char *str)
{
	unsigned long long	var;
	unsigned int		i;

	var = 0;
	i = 0;
	while (str[i] == ' ' || (str[i] >= '\t' && str[i] <= '\r'))
		i++;
	while (str[i] >= '0' && str[i] <= '9')
	{
		var = (var * 10) + (str[i] - '0');
		i++;
	}
	return (var);
}

unsigned int	len(char *str)
{
	unsigned int	i;

	i = 0;
	while (str && str[i])
		i++;
	return (i);
}

char	*strdup(char *src)
{
	unsigned int	i;
	char			*dest;

	i = 0;
	dest = malloc(sizeof(char) * (len(src) + 1));
	if (!dest)
		return (NULL);
	while (src[i])
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = '\0';
	return (dest);
}
