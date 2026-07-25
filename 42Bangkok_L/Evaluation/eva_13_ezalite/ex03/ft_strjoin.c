/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ezalite <ezalite@student.42bangkok>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/22 02:00:17 by ezalite           #+#    #+#             */
/*   Updated: 2026/07/22 21:59:38 by ezalite          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

int	ft_find_len(int size, char **strs, char *sep)
{
	int	i;
	int	j;
	int	len;

	len = 0;
	i = 0;
	while (i < size)
	{
		j = 0;
		while (strs[i][j])
			j++;
		len += j;
		i++;
	}
	j = 0;
	while (sep[j])
		j++;
	len += j * (size - 1);
	return (len);
}

char	*ft_catstr(int size, char **strs, char *sep, char *dest)
{
	int	i;
	int	j;
	int	index;

	index = 0;
	i = 0;
	while (i < size)
	{
		j = 0;
		while (strs[i][j])
			dest[index++] = strs[i][j++];
		if (i == size - 1)
			break ;
		j = 0;
		while (sep[j])
			dest[index++] = sep[j++];
		i++;
	}
	dest[index] = '\0';
	return (dest);
}

char	*ft_strjoin(int size, char **strs, char *sep)
{
	char	*str;

	if (size <= 0)
	{
		str = malloc(1);
		if (!str)
		{
			return (0);
		}
		*str = '\0';
		return (str);
	}
	str = malloc(sizeof (char) * (ft_find_len(size, strs, sep) + 1));
	if (!str)
	{
		return (0);
	}
	str = ft_catstr(size, strs, sep, str);
	return (str);
}
/*
#include <stdio.h>

int	main(void)
{
	char	**strs;
	char	*sep;
	char	*str;
	int	size;

	sep = "-----";
	size = 5;
	strs = malloc(sizeof (char *) * size);
	strs[0] = "Hell1";
	strs[1] = "hello2";
	strs[2] = "hello3";
	strs[3] = "hello4";
	strs[4] = "hello5";
	printf("%s\n", ft_strjoin(size, strs, sep));
	str = ft_strjoin(0, strs, sep);
	if (!*str)
		printf("str is a null pointer before free()\n");
	free(str);
	if (!*str)
		printf("str is a null pointer after free()\n");
	return (0);
}*/
