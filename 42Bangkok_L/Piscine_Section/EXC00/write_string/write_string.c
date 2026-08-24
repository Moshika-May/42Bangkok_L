/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   write_string.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/10 22:59:14 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/10 23:11:24 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	write_string(char *str)
{
	int		n;
	char	a;

	n = 0;
	a = str[0];
	if (a == ' ')
	{
		while (str[n] != '\0')
		{
			write(1, str, 1);
			n++;
		}
	}
	else if (a != '\0')
	{
		write(1, str, 1);
	}
	write(1, "\n", 1);
}

int	main(void)
{
	write_string("          ");
	write_string("weg2");
	write_string("");
}
// >          $
// >          $
// \ no new in files$
