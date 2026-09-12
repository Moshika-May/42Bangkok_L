/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlen.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/09 17:02:01 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/12 01:04:42 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>

size_t	ft_strlen(const char *str)
{
	size_t	n;

	n = 0;
	while (*str != '\0')
	{
		str++;
		n++;
	}
	return (n);
}
// int	main(void)
//{
//	ft_strlen("Safari");
//	return (0);
//}
