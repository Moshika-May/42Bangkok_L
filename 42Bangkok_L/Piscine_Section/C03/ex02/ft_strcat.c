/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strcat.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/16 12:49:00 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/16 13:31:52 by kmahanin         ###   ########.fr       */
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

char	*ft_strcat(char *dest, char *src)
{
	unsigned int	i;
	unsigned int	j;

	i = len(dest);
	j = 0;
	while (src[j] != '\0')
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
	char	dest[50] = "Wait, ";
	char	src[] = "What  Howww";

	printf("%s\n", dest);
	ft_strcat(dest, src);
	printf("%s\n", dest);
	return (0);
}
*/
