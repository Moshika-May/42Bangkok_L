/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strstr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/16 13:55:27 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/20 11:34:53 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// #include <stdio.h>

char	*ft_strstr(char *str, char *to_find)
{
	unsigned int	i;
	unsigned int	j;

	if (to_find[0] == '\0')
		return (str);
	i = 0;
	while (str[i] != '\0')
	{
		j = 0;
		while (str[i + j] == to_find[j] && to_find[j] != '\0')
			j++;
		if (to_find[j] == '\0')
			return (&str[i]);
		i++;
	}
	return (0);
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
