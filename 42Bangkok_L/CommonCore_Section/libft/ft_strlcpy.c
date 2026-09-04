/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/14 11:42:54 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/04 12:14:09 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>

size_t	ft_strlcpy(char *dst, const char *restrict src, size_t d_size)
{
	unsigned int	i;

	i = 0;
	while (src[i] != '\0')
	{
		if (i < d_size)
			dst[i] = src[i];
		i++;
	}
	dst[d_size - 1] = '\0';
	return (i);
}
