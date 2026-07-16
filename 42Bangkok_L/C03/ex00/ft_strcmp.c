/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/15 16:54:05 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/16 11:59:48 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// #include <stdio.h>

int	ft_strcmp(char *s1, char *s2)
{
	unsigned int	i;
	int				var;

	i = 0;
	while (s1[i] != '\0' && s1[i] == s2[i])
	{
		i++;
	}
	var = ((unsigned char)s1[i]) - ((unsigned char)s2[i]);
	return (var);
}
/*
int	main(void)
{
	printf("%d", ft_strcmp("", "ABC"));
	return (0);
}
*/
