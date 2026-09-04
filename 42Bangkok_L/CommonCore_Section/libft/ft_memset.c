/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/01 11:12:23 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/04 11:10:47 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>

void	*ft_memset(void *str, int c, size_t n)
{
	unsigned char	*p;
	size_t			i;

	p = str;
	i = 0;
	while (i < n)
	{
		p[i] = c;
		i++;
	}
	return (str);
}
/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	char	str1[20] = "Hello World!";
	char	str2[20] = "Hello World!";

	ft_memset(str1, 'O', 5);
	memset(str2, 'O', 5);
	printf("ft_memset : %s\n", str1);
	printf("memset    : %s\n", str2);
	return (0);
}
*/
