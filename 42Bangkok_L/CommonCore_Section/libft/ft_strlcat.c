/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/20 14:28:53 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/10 09:53:36 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>

size_t	len(const char *str)
{
	size_t	i;

	i = 0;
	while (str[i] != '\0')
		i++;
	return (i);
}

size_t	ft_strlcat(char *dest, const char *src, size_t d_size)
{
	size_t	i;
	size_t	j;
	size_t	dest_l;
	size_t	src_l;

	dest_l = 0;
	src_l = len(src);
	while (dest[dest_l] != '\0' && dest_l < d_size)
		dest_l++;
	if (dest_l == d_size)
		return (d_size + src_l);
	i = dest_l;
	j = 0;
	while (src[j] != '\0' && i < (d_size - 1))
	{
		dest[i] = src[j];
		j++;
		i++;
	}
	dest[i] = '\0';
	return (dest_l + src_l);
}

// #include <stdio.h>
/*
int	main(void)
{
	char	dst[21] = "strlcat is cat not";
	char	src[] = " rabbit.";

	printf("%ld\n", ft_strlcat(dst, src, 21));
	printf("%s\n", dst);
	return (0);
}
*/
