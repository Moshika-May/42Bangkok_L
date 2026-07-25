/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_is_negative.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkarun <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/09 19:41:57 by nkarun            #+#    #+#             */
/*   Updated: 2026/07/11 15:15:15 by nkarun           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_is_negative(int n)
{
	if (n < 0)
		write(1, "N", 1);
	if (n >= 0)
		write(1, "P", 1);
}
/*
int	main(void)
{
	ft_is_negative(1);
	ft_is_negative(-1);
	ft_is_negative(0);
	return (0);
}
*/
