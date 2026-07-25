/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_reverse_alphabet.c                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkarun <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/08 22:16:59 by nkarun            #+#    #+#             */
/*   Updated: 2026/07/11 16:57:00 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_print_reverse_alphabet(void)
{
	char	za;

	za = 'z';
	while (za >= 'a')
	{
		write(1, &za, 1);
		za --;
	}
}

int	main(void)
{
	ft_print_reverse_alphabet();
	write(1, "\n", 1);
	return 0;
}

