/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/12 14:30:47 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/19 13:07:52 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static size_t	ft_in(const char word, const char *in)
{
	size_t	i;

	i = 0;
	while (in[i])
	{
		if (word == in[i])
			return (1);
		i++;
	}
	return (0);
}

static size_t	len(const char *str)
{
	size_t	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

static char	*str_add(char *str_trim, size_t t_start, size_t t_len,
		const char *s1)
{
	size_t	i;

	i = 0;
	while (i < t_len)
	{
		str_trim[i] = s1[t_start];
		t_start++;
		i++;
	}
	str_trim[i] = '\0';
	return (str_trim);
}

char	*ft_strtrim(char const *s1, char const *set)
{
	char	*str_trim;
	size_t	trim_strt;
	size_t	trim_end;
	size_t	i;
	size_t	trim_len;

	if (!s1 || !set)
		return (NULL);
	i = 0;
	while (s1[i] && ft_in(s1[i], set) == 1)
		i++;
	trim_strt = i;
	i = len(s1);
	while (i > trim_strt && (ft_in(s1[i - 1], set) == 1))
		i--;
	trim_end = i;
	trim_len = trim_end - trim_strt;
	str_trim = malloc(sizeof(char) * (trim_len + 1));
	if (!str_trim)
		return (NULL);
	return (str_add(str_trim, trim_strt, trim_len, s1));
}
/*
#include <stdio.h>
#include <string.h>

int	main(int ac, char **av)
{
	(void)ac;
	printf("%s\n", ft_strtrim(av[1], av[2]));
	return (0);
}
*/
