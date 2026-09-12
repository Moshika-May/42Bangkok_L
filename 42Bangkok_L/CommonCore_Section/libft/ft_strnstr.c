/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/16 13:55:27 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/10 11:10:02 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>

char	*ft_strnstr(const char *str, const char *to_find, size_t len)
{
	size_t	i;
	size_t	j;

	if (!to_find)
		return (NULL);
	if (to_find[0] == '\0')
		return ((char *)str);
	i = 0;
	while (str[i] && i < len)
	{
		j = 0;
		while ((i + j) < len && str[i + j] == to_find[j] && to_find[j] != '\0')
			j++;
		if (to_find[j] == '\0')
			return ((char *)&str[i]);
		i++;
	}
	return (NULL);
}
/*
int	main(void)
{
	char	long_str[] = "Do you see me, I'm pretty sure not seek me";
	char	find[] = "seek";

	printf("%s\n", ft_strstr(long_str, find));
	return (0);
}
*/
