/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/08 15:33:25 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/10 10:32:56 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>
#include <stdlib.h>

void	ft_bzero(void *str, size_t n);

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
