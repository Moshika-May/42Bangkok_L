/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/04 13:42:25 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/07 11:53:55 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memcpy(void *dest, const void *src, size_t n)
{
	unsigned char		*ptr_d;
	const unsigned char	*ptr_s;
	size_t				i;

	if (!dest && !src)
		return (NULL);
	i = 0;
	ptr_d = (unsigned char *)dest;
	ptr_s = (const unsigned char *)src;
	while (i < n)
	{
		ptr_d[i] = ptr_s[i];
		i++;
	}
	return (dest);
}
/*
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int	main(int ac, char **av)
{
	unsigned char	*a;

	a = malloc(sizeof(char) * (strlen(av[1]) + 1));
	if (!a)
		return (0);
	ft_memcpy(a, av[1], (strlen(av[1]) + 1));
	(void)ac;
	printf("%s\n", a);
	free(a);
	return (0);
}
*/
