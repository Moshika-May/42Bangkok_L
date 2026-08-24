/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_str_is_alpha.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/13 21:35:06 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/13 22:20:58 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// #include <stdio.h>
int	ft_str_is_alpha(char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i] != '\0')
	{
		if ((str[i] < 'A' || str[i] > 'Z') && (str[i] < 'a' || str[i] > 'z'))
			return (0);
		i++;
	}
	return (1);
}
/*
int	main(void)
{
	int	a;

	a = ft_str_is_alpha("Adobe 13");
	if (a == 1)
		printf("1\n");
	else if (a == 0)
		printf("0\n");
	return (0);
}
*/
