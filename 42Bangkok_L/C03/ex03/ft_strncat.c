/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/16 13:37:30 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/16 13:52:49 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// #include <stdio.h>

int	len(char *prams)
{
	unsigned int	i;

	i = 0;
	while (prams[i] != '\0')
		i++;
	return (i);
}

char	*ft_strncat(char *dest, char *src, unsigned int nb)
{
	unsigned int	i;
	unsigned int	j;

	i = len(dest);
	j = 0;
	while (src[j] != '\0' && j < nb)
	{
		dest[i] = src[j];
		j++;
		i++;
	}
	dest[i] = '\0';
	return (dest);
}
/*
int	main(void)
{
	char	des[30] = "You'll never grow";
	char	src[] = ", If you never try";

	printf("%s\n", des);
	ft_strncat(des, src, 11);
	printf("%s\n", des);
	return (0);
}
*/
