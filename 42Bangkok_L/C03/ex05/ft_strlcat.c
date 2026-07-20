/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/20 14:28:53 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/20 16:52:14 by kmahanin         ###   ########.fr       */
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
	unsigned int	a;
	unsigned int	b;

	a = len(dest);
	b = len(src);
	if (size <= a)
		return (size + b);
	i = a;
	j = 0;
	while (src[j] != '\0' && i < (size - 1))
	{
		dest[i] = src[j];
		j++;
		i++;
	}
	dest[i] = '\0';
	return (a + b);
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
