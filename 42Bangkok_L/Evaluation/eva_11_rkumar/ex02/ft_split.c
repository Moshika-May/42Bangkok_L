/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/21 07:57:13 by rkumar            #+#    #+#             */
/*   Updated: 2026/07/25 14:05:42 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

int	is_separator(char c, char *sep)
{
	int	i;

	i = 0;
	while (sep[i])
	{
		if (c == sep[i])
			return (1);
		i++;
	}
	return (0);
}

int	count_words(char *str, char *sep)
{
	int	i;
	int	words;

	i = 0;
	words = 0;
	while (str[i])
	{
		if (!is_separator(str[i], sep))
		{
			words++;
			while (str[i] && !is_separator(str[i], sep))
				i++;
		}
		else
			i++;
	}
	return (words);
}

char	*word_splitter(char *str, char *sep)
{
	char	*word;
	int		i;

	i = 0;
	while (str[i] && !is_separator(str[i], sep))
		i++;
	word = malloc(sizeof(char) * (i + 1));
	if (!word)
		return (NULL);
	i = 0;
	while (str[i] && !is_separator(str[i], sep))
	{
		word[i] = str[i];
		i++;
	}
	word[i] = '\0';
	return (word);
}

void	fill_words(char **words, char *str, char *charset)
{
	int	i;
	int	j;

	i = 0;
	j = 0;
	while (str[i])
	{
		if (!is_separator(str[i], charset))
		{
			words[j++] = word_splitter(&str[i], charset);
			while (str[i] && !is_separator(str[i], charset))
				i++;
		}
		else
			i++;
	}
	words[j] = NULL;
}

char	**ft_split(char *str, char *charset)
{
	char	**words;

	if (!str || !charset)
		return (NULL);
	words = malloc(sizeof(char *) * (count_words(str, charset) + 1));
	if (!words)
		return (NULL);
	fill_words(words, str, charset);
	return (words);
}
 #include <stdio.h>

 int	main(void)
 {
 	char	*str = "Words to.be/splitted*in@six";
 	char	*sep = "./*@! ";
 	char	**words;
 	int		i;

 	words = ft_split(str, sep);
 	i = 0;
 	printf("Before: %s\n", str);
 	printf("After:\n");
 	while (words[i])
 	{
 		printf("%s\n", words[i]);
 		free(words[i]);
 		i++;
 	}
 	free(words);
 	return (0);
 }
