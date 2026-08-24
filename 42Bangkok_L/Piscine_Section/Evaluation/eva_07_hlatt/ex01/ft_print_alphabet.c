/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_alphabet.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/08 11:15:00 by hlatt             #+#    #+#             */
/*   Updated: 2026/07/09 18:41:34 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_print_alphabet(void)
{
	char	a;

	a = 'a';
	while (a <= 'z')
	{
		write(1, &a, 1);
		a++;
	}
}

int	main(void)
{
	ft_print_alphabet();
	return (0);
}