/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlen.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: gamagalh <gamagalh@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/16 14:43:12 by gamagalh          #+#    #+#             */
/*   Updated: 2026/07/23 15:35:09 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_strlen(char *str)
{
	int	i;

	i = 0;
	while (str[i] != '\0')
		i++;
	if (i > 0)
		return (i);
	return (0);
}

#include <stdio.h>
int	main(void)
{
	printf("%d\n", ft_strlen("Here is 9"));
	return (0);
}
