/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/08 15:33:25 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/19 01:32:53 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>
#include <stdlib.h>

void	ft_bzero(void *s, size_t n)
{
	unsigned char	*ptr;
	size_t			i;

	ptr = (unsigned char *)s;
	i = 0;
	while (i < n)
	{
		ptr[i] = '\0';
		i++;
	}
}

void	*ft_calloc(size_t n, size_t size)
{
	void	*v;
	size_t	i_size;

	if (n > 0 && size > ((size_t)-1) / n)
		return (NULL);
	i_size = n * size;
	v = malloc(i_size);
	if (!v)
		return (NULL);
	ft_bzero(v, i_size);
	return (v);
}
