/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input_validation.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ataweech <ataweech@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 19:47:27 by ataweech          #+#    #+#             */
/*   Updated: 2026/07/26 19:47:28 by ataweech         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rush02.h"

int	is_number(char *str)
{
	unsigned int	i;

	i = 0;
	if (!str || !str[i])
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
