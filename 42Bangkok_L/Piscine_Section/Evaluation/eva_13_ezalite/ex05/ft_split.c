/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ezalite <ezalite@student.42bangkok>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/22 17:49:26 by ezalite           #+#    #+#             */
/*   Updated: 2026/07/25 15:06:29 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

int	ft_belongs(char c, char *str)
{
	while (*str)
	{
		if (c == *str)
			return (1);
		str++;
	}
	return (0);
}

int	ft_count_words(char *str, char *charset)
{
	int	count;

	count = 0;
	while (*str)
	{
		if (!ft_belongs(*str, charset))
		{
			count++;
			while (!ft_belongs(*str, charset) && *str)
				str++;
			continue ;
		}
		str++;
	}
	return (count);
}

char	*ft_retrieve_word(char *src, char *sep)
{
	int		i;
	int		j;
	char	*str;

	i = 0;
	while (!ft_belongs(src[i], sep) && src[i])
		i++;
	str = malloc(sizeof (char) * (i + 1));
	if (str == NULL)
		return (NULL);
	j = 0;
	while (j < i)
	{
		str[j] = src[j];
		j++;
	}
	str[j] = '\0';
	return (str);
}

char	**ft_extract_words(char *str, char *charset, char **array)
{
	char	**array_copy;

	array_copy = array;
	while (*str)
	{
		if (!ft_belongs(*str, charset))
		{
			*array_copy = ft_retrieve_word(str, charset);
			if (*array_copy == NULL)
				return (NULL);
			array_copy++;
			while (!ft_belongs(*str, charset) && *str)
				str++;
			continue ;
		}
		str++;
	}
	*array_copy = NULL;
	return (array);
}

char	**ft_split(char *str, char *charset)
{
	char	**array;

	array = malloc(sizeof (char *) * (ft_count_words(str, charset) + 1));
	if (array == NULL)
		return (NULL);
	if (ft_extract_words(str, charset, array) == NULL)
		return (NULL);
	return (array);
}

#include <stdio.h>

int	main(void)
{
	char **array;

	array = ft_split(" a a b b c c s ssss ", " ");
	while (*array)
		printf("%s\n", *array++);
	printf("%d\n", ft_count_words("my name is er'nests ddd$ss", "'"));
	return (0);
}
