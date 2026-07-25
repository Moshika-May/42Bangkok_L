/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_is_negative.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: miazanov <miazanov@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/09 11:15:29 by miazanov          #+#    #+#             */
/*   Updated: 2026/07/09 11:21:37 by miazanov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_is_negative(int n)
{
	char	a;

	if (n < 0)
	{
		a = 'N';
	}
	else
	{
		a = 'P';
	}
	write(1, &a, 1);
}

// int main() { 
//     ft_is_negative(5);
// 	write(1, "\n", 1);
// 	ft_is_negative(0);
// 	write(1, "\n", 1);
// 	ft_is_negative(-2);
//     return 0;
// }