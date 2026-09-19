/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/28 22:51:40 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/12 23:35:51 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static size_t	word_len(char const *s, char c)
{
	size_t	i;

	i = 0;
	while (s[i] && s[i] != c)
		i++;
	return (i);
}

static size_t	len_words(const char *str, char sep)
{
	size_t	i;
	size_t	words;

	words = 0;
	i = 0;
	while (str[i])
	{
		while (str[i] && str[i] == sep)
			i++;
		if (str[i] && str[i] != sep)
		{
			words++;
			while (str[i] && str[i] != sep)
				i++;
		}
	}
	return (words);
}

static char	*fill_word(char const *s, size_t len)
{
	char	*word;
	size_t	i;

	word = malloc(sizeof(char) * (len + 1));
	if (!word)
		return (NULL);
	i = 0;
	while (i < len)
	{
		word[i] = s[i];
		i++;
	}
	word[i] = '\0';
	return (word);
}

static void	free_split(char **str_split, size_t i)
{
	while (i > 0)
	{
		i--;
		free(str_split[i]);
	}
	free(str_split);
}

char	**ft_split(char const *s, char c)
{
	char	**str_split;
	size_t	words;
	size_t	i;
	size_t	j;

	words = len_words(s, c);
	str_split = malloc(sizeof(char *) * (words + 1));
	if (!str_split)
		return (NULL);
	i = 0;
	j = 0;
	while (i < words)
	{
		while (s[j] == c)
			j++;
		str_split[i] = fill_word(s + j, word_len(s + j, c));
		if (!str_split[i])
			return (free_split(str_split, i), NULL);
		j += word_len(s + j, c);
		i++;
	}
	str_split[i] = NULL;
	return (str_split);
}
/*
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

char	**ft_split(char const *s, char *c)
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
*/
/*
#include <stdio.h>

int	main(int c, char **v)
{
	char	**result;
	int		i;

	i = 0;
	if (c == 3)
	{
		result = ft_split(v[1], v[2][0]);
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
