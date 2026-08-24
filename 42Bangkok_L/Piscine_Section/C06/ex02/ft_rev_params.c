/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_rev_params.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/25 13:00:49 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/25 13:04:17 by kmahanin         ###   ########.fr       */
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

	i = argc - 1;
	while (i > 0)
	{
		putstr(argv[i]);
		putstr("\n");
		i--;
	}
	return (0);
}
