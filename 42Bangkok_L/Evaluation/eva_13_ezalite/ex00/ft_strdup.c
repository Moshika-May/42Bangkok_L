/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ezalite <ezalite@student.42bangkok>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/21 23:13:09 by ezalite           #+#    #+#             */
/*   Updated: 2026/07/22 21:58:03 by ezalite          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

char	*ft_strdup(char *src)
{
	int		i;
	char	*src_cpy;

	i = 0;
	while (src[i])
		i++;
	src_cpy = malloc(sizeof (char) * (i + 1));
	if (!src_cpy)
	{
		return (0);
	}
	i = 0;
	while (src[i])
	{
		src_cpy[i] = src[i];
		i++;
	}
	src_cpy[i] = '\0';
	return (src_cpy);
}
/*
#include <stdio.h>

int	main(void)
{
	char	*str;
	char	*str_cpy;

	str = "Hello this is the original\n";
	printf("%s", str);
	str_cpy = ft_strdup(str);
	if (str_cpy)
		printf("%s", str_cpy);
	return (0);
}*/
