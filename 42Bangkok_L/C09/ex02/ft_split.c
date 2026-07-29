/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/28 22:51:40 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/29 00:40:06 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>
#include <stdlib.h>

unsigned int	is_sep(char chr, char *chatset)
{
	unsigned int	i;

	i = 0;
	while (chatset[i])
	{
		if (chr == chatset[i])
			return (1);
		i++;
	}
	return (0);
}

unsigned int	len_words(char *str, char *chatset)
{
	unsigned int	i;
	unsigned int	count;

	i = 0;
	count = 0;
	while (str[i])
	{
		while (str[i] && is_sep(str[i], chatset))
			i++;
		if (str[i] && !is_sep(str[i], chatset))
		{
			count++;
			while (str[i] && !is_sep(str[i], chatset))
				i++;
		}
	}
	return (count);
}

static char	*strduplicate(char *str, unsigned int n)
{
	char			*word;
	unsigned int	k;

	word = (char *)malloc(sizeof(char) * (n + 1));
	if (!word)
		return (NULL);
	k = 0;
	while (k < n)
	{
		word[k] = str[k];
		k++;
	}
	word[k] = '\0';
	return (word);
}

char	**ft_split(char *str, char *chatset)
{
	char			**word;
	unsigned int	i;
	unsigned int	n;
	unsigned int	j;

	i = 0;
	j = 0;
	word = (char **)malloc(sizeof(char *) * (len_words(str, chatset) + 1));
	if (!word)
		return (NULL);
	while (str[i])
	{
		while (str[i] && is_sep(str[i], chatset))
			i++;
		n = 0;
		while (str[i + n] && !is_sep(str[i + n], chatset))
			n++;
		if (n > 0)
			word[j++] = strduplicate(&str[i], n);
		i += n;
	}
	word[j] = NULL;
	return (word);
}
/*
#include <stdio.h>

int	main(int c, char **v)
{
	char	**result;
	int		i;

	i = 0;
	if (c == 3)
	{
		result = ft_split(v[1], v[2]);
		if (!result)
			return (1);
		while (result[i])
		{
			printf("Word %d: %s\n", i, result[i]);
			free(result[i]);
			i++;
		}
		free(result);
	}
	return (0);
}
*/
