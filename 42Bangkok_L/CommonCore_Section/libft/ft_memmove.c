/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/04 13:54:38 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/04 16:13:16 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
void	*memmove_to(unsigned char *ptr_dst, const unsigned char *ptr_src,
		size_t n)
{
	size_t	i;

	if ((size_t)ptr_dst > (size_t)ptr_src)
	{
		while (n > 0)
		{
			n--;
			ptr_dst[n] = ptr_src[n];
		}
	}
	else if (ptr_dst < ptr_src)
	{
		i = 0;
		while (i < n)
		{
			ptr_dst[n] = ptr_src[n];
			i++;
		}
	}
	return (ptr_dst);
}
*/

void	*ft_memmove(void *dst, const void *src, size_t n)
{
	unsigned char		*ptr_dst;
	const unsigned char	*ptr_src;

	if (!dst && !src)
		return (NULL);
	ptr_dst = (unsigned char *)dst;
	ptr_src = (const unsigned char *)src;
	if (ptr_dst > ptr_src)
	{
		while (n--)
			ptr_dst[n] = ptr_src[n];
	}
	else if (ptr_dst < ptr_src)
	{
		while (n--)
			*ptr_dst++ = *ptr_src++;
	}
	return (dst);
}
