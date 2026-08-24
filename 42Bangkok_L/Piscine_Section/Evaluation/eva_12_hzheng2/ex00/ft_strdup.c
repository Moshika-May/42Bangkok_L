/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hzheng2 <hzheng2@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/21 20:13:07 by hzheng2           #+#    #+#             */
/*   Updated: 2026/07/25 10:54:36 by hzheng2          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <stdlib.h>

char	*ft_strdup(char *src)
{
	int		length;
	char	*arr;

	length = 0;
	while (*src != '\0')
	{
		length++;
		src++;
	}
	length++;
	arr = (char *) malloc(length * sizeof(char));
	*(arr + length) = '\0';
	while (--length >= 0)
	{
		*(arr + length) = *src;
		src--;
	}
	return (arr);
}
