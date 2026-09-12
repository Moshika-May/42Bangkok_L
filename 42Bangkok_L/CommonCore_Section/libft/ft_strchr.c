/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/12 00:16:15 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/12 00:49:17 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>

char	*ft_strchr(const char *s, int c)
{
	size_t	i;

	i = 0;
	while (s[i])
	{
		if (s[i] == (char)c)
			return ((char *)&s[i]);
		i++;
	}
	if ((char)c == '\0')
		return ((char *)&s[i]);
	return (NULL);
}
/*
#include <stdio.h>
#include <string.h>

int	main(int ac, char **av)
{
	(void)ac;
	printf("real: %s\n", strchr(av[1], 'a'));
	printf("me: %s\n", ft_strchr(av[1], 'a'));
	return (0);
}
*/
