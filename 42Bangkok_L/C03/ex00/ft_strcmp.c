/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/15 16:54:05 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/15 17:14:47 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

int	ft_strcmp(char *s1, char *s2)
{
	unsigned int	i;
	int	_1;
	int	_2;
	int	var;

	_1 = 0;
	_2 = 0;
	i = 0;
	while (s1[i] != '\0')
	{
		_1 += s1[i];
		i++;
	}
	i = 0;
	while (s2[i] != '\0')
	{
		_2 += s2[i];
		i++;
	}
	var = _1 - _2;
	return (var);
}

int	main(void)
{
	printf("%d", ft_strcmp("AB", "ABC"));
	return (0);
}
