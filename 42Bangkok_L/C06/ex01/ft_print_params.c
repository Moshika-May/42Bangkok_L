/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_params.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/25 12:51:18 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/25 13:00:09 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	putstr(char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i])
	{
		write(1, &str[i], 1);
		i++;
	}
	return ;
}

int	main(int argc, char **argv)
{
	unsigned int	i;

	i = 1;
	while (i < ((unsigned int)argc))
	{
		putstr(argv[i]);
		putstr("\n");
		i++;
	}
	return (0);
}
