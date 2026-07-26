/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input_validation.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/24 20:09:35 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/24 22:37:23 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rsh02.h"

int	is_number(char *str)
{
	unsigned int	i;

	i = 0;
	if (!str[i] || !str)
		return (1);
	while (str[i])
	{
		if (str[i] < '0' || str[i] > '9')
			return (1);
		i++;
	}
	return (0);
}

int	input_validation(int argc, char **argv)
{
	if (argc != 2 && argc != 3)
		return (1);
	if (argc == 2 && is_number(argv[1]))
		return (1);
	if (argc == 3 && is_number(argv[2]))
		return (1);
	return (0);
}
