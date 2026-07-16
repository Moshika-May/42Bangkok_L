/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/16 18:20:14 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/16 22:13:26 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// #include <stdio.h>

int	ft_atoi(char *str)
{
	unsigned int	i;
	int				j;
	int				k;

	i = 0;
	j = 1;
	k = 0;
	while (str[i] == ' ' || (str[i] >= '\t' && str[i] <= '\r'))
		i++;
	while (str[i] == '+' || str[i] == '-')
	{
		if (str[i] == '-')
			j = -j;
		i++;
	}
	while (str[i] >= '0' && str[i] <= '9')
	{
		k = (k * 10) + (str[i] - '0');
		i++;
	}
	return (k * j);
}
/*
int	main(int argc, char *argv[])
{
	if (argc == 2)
		printf("%d", ft_atoi(argv[1]));
	return (0);
}
*/
