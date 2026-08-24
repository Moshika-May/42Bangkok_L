/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_numbers.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/08 11:31:17 by zwai              #+#    #+#             */
/*   Updated: 2026/07/09 12:26:34 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_print_numbers(void)
{
	char	a;

	a = '0';
	while (a <= '9')
	{
		write(1, &a, 1);
		a++;
	}
}

int	main(void)
{
	ft_print_numbers();
	return (0);
}