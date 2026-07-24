/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/24 19:59:02 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/25 00:05:57 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rsh02.h"

int	main(int argc, char **argv)
{
	unsigned long long	num;
	char				*dict_str;

	dict_str = "number.dict";
	if (input_validation(argc, argv))
	{
		putstr("Error\n");
		return (0);
	}
	if (argc == 2)
		num = atoull(argv[1]);
	else if (argc == 3)
	{
		dict_str = argv[1];
		num = atoull(argv[2]);
	}
	(void)num;
	(void)dict_str;
	return (0);
}
