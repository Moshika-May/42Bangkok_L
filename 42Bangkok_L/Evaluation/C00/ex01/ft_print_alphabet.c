/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_alphabet.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkarun <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/10 16:34:45 by nkarun            #+#    #+#             */
/*   Updated: 2026/07/11 15:05:45 by nkarun           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_print_alphabet(void)
{
	char	az;

	az = 'a';
	while (az <= 'z')
	{
		write(1, &az, 1);
		az++;
	}
}
/*
int	main(void)
{
	ft_print_alphabet();
	write(1, "\n", 1);
	return (0);
}
*/
