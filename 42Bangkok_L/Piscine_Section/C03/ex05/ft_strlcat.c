/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/20 14:28:53 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/23 16:05:16 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// #include <stdio.h>

unsigned int	len(char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i] != '\0')
		i++;
	return (i);
}

unsigned int	ft_strlcat(char *dest, char *src, unsigned int size)
{
	unsigned int	i;
	unsigned int	j;
	unsigned int	dest_l;
	unsigned int	src_l;

	dest_l = 0;
	src_l = len(src);
	while (dest[dest_l] != '\0' && dest_l < size)
		dest_l++;
	if (dest_l == size)
		return (size + src_l);
	i = dest_l;
	j = 0;
	while (src[j] != '\0' && i < (size - 1))
	{
		dest[i] = src[j];
		j++;
		i++;
	}
	dest[i] = '\0';
	return (dest_l + src_l);
}
/*
int	main(void)
{
	char	dst[21] = "strlcat is cat not";
	char	src[] = " rabbit.";

	printf("%d\n", ft_strlcat(dst, src, 21));
	printf("%s\n", dst);
	return (0);
}
*/
