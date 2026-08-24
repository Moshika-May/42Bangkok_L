/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_str_is_numeric.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/13 23:13:02 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/13 23:20:36 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
int	ft_str_is_numeric(char *str)
{
	int	i;

	i = 0;
	while (str[i] != '\0')
	{
		if (str[i] < '0' || str[i] > '9')
			return (0);
		i++;
	}
	return (1);
}
/*
int	main(void)
{
	int	a;

	a = ft_str_is_numeric("1456a");
	if (a == 1)
		printf("1");
	else if (a == 0)
		printf("0");
	return (0);
}
*/
