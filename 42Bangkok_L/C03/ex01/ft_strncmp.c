/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncmp.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/15 17:16:47 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/15 20:38:07 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

int	ft_strcmp(char *s1, char *s2, unsigned int n)
{
	unsigned int	i;
	int				j;

	i = 0;
	j = 0;
	while (i <= n)
	{
		if (s1[i] == s2[i])
			i++;
		else
		{
			j = s1[i] - s2[i];
			return (j);
		}
	}
	return (0);
}

int	main(void)
{
	printf("%d", ft_strcmp("Help_Me", "Help_My", 7));
	return (0);
}
