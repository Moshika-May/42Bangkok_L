/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/12 02:30:10 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/12 03:10:08 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>
#include <stdlib.h>

size_t	ft_strlen(const char *str)
{
	size_t	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	size_t	s_len;
	size_t	i;
	char	*sstr;

	if (!s)
		return (NULL);
	s_len = ft_strlen(s);
	if (start > s_len)
		start = s_len;
	if (len > s_len - start)
		len = s_len - start;
	sstr = malloc(sizeof(char) * (len + 1));
	if (!sstr)
		return (NULL);
	i = 0;
	while (len > i)
	{
		sstr[i] = s[start + i];
		i++;
	}
	sstr[i] = '\0';
	return (sstr);
}
/*
#include <stdio.h>

int	main(int ac, char **av)
{
	(void)ac;
	printf("%s\n", ft_substr(av[1], atoi(av[2]), atoi(av[3])));
	return (0);
}
*/
