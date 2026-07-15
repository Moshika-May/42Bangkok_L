/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/14 11:42:54 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/15 19:12:43 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// #include <stdio.h>

unsigned int	ft_strlcpy(char *dest, char *src, unsigned int size)
{
	unsigned int	i;

	i = 0;
	while (src[i] != '\0')
	{
		if (i < size)
			dest[i] = src[i];
		i++;
	}
	dest[size - 1] = '\0';
	return (i);
}
/*
int	main(void)
{
	char			src[] = "Hello, World!";
	char			dst[16];
	unsigned int	test;

	test = ft_strlcpy(dst, src, 16);
	printf("%d\n", test);
	printf("%s\n", dst);
	return (0);
}
*/
