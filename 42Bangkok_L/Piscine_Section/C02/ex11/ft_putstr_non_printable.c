/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr_non_printable.c                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/14 13:51:34 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/15 19:14:05 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_putstr_non_printable(char *str)
{
	unsigned int	i;
	char			a;
	char			*h;

	i = 0;
	h = "0123456789abcdef";
	while (str[i] != '\0')
	{
		if (str[i] >= ' ' && str[i] <= '~')
		{
			a = str[i];
			write(1, &a, 1);
		}
		else
		{
			write(1, "\\", 1);
			write(1, &h[str[i] / 16], 1);
			write(1, &h[str[i] % 16], 1);
		}
		i++;
	}
}
/*
int	main(void)
{
	char	str[1];

	str[0] = 128;

	ft_putstr_non_printable(str);
	return (0);
}
*/
