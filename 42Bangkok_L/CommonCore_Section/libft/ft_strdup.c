/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/25 16:23:56 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/19 13:05:55 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static unsigned long	len(const char *str)
{
	unsigned long	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

char	*ft_strdup(const char *src)
{
	unsigned long	i;
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
/*
#include <stdio.h>
#include <string.h>

int	main(int ac, char **av)
{
	char	*a;
	char	*b;

	(void)ac;
	a = strdup(av[1]);
	b = ft_strdup(av[1]);
	printf("std: %s\n", a);
	printf("my: %s\n", b);
	free(a);
	free(b);
	return (0);
}
*/
