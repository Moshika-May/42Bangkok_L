/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr_non_printable.c                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/14 13:51:34 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/14 17:31:13 by kmahanin         ###   ########.fr       */
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
		if (str[i] < ' ' || str[i] == 127)
		{
			write(1, "\\", 1);
			write(1, &h[str[i] / 16], 1);
			write(1, &h[str[i] % 16], 1);
		}
		else if (str[i] >= ' ' && str[i] <= '~')
		{
			a = str[i];
			write(1, &a, 1);
		}
		i++;
	}
}
/*
int	main(void)
{
	char	str[] = "Hello\nHow are you?";

	ft_putstr_non_printable(str);
	return (0);
}
*/
