/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi_base.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/22 15:35:52 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/22 16:37:59 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	index_base(char zam, char *base)
{
	int	i;

	i = 0;
	while (base[i])
	{
		if (base[i] == zam)
			return (i);
		i++;
	}
	return (-1);
}

int	base_check(char *base)
{
	unsigned int	i;
	unsigned int	j;

	i = 0;
	if (!base[0] || !base[1])
		return (0);
	while (base[i])
	{
		if (base[i] == '+' || base[i] == '-' || (base[i] >= '\t'
				&& base[i] <= '\r'))
			return (0);
		j = i + 1;
		while (base[j])
		{
			if (base[i] == base[j])
				return (0);
			j++;
		}
		i++;
	}
	return (i);
}

int	ft_atoi_base(char *str, char *base)
{
	unsigned int	i;
	int				j;
	int				k;

	i = 0;
	j = 1;
	k = 0;
	if (!base_check(base))
		return (0);
	while (str[i] == ' ' || (str[i] >= '\t' && str[i] <= '\r'))
		i++;
	while (str[i] == '+' || str[i] == '-')
	{
		if (str[i] == '-')
			j = -j;
		i++;
	}
	while (str[i] && (index_base(str[i], base) != -1))
	{
		k = (k * base_check(base)) + (index_base(str[i], base));
		i++;
	}
	return (k * j);
}
/*
#include <stdio.h>

int	main(int argc, char **argv)
{
	if (argc != 3)
		return (0);
	printf("%s\n", argv[1]);
	printf("%s\n", argv[2]);
	printf("%d\n", ft_atoi_base(argv[1], argv[2]));
	return (0);
}
*/
