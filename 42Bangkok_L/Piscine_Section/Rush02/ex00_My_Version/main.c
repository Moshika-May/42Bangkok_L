/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/24 19:59:02 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/27 14:24:22 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rsh02.h"

int	main(int argc, char **argv)
{
	t_dict				*dict;
	unsigned __int128	n;
	int					first;
	char				*dict_path;
	char				*num_str;

	first = 1;
	dict_path = "numbers.dict";
	if (input_validation(argc, argv))
	{
		putstr("Error\n");
		return (0);
	}
	if (argc == 2)
		num_str = argv[1];
	else
	{
		dict_path = argv[1];
		num_str = argv[2];
	}
	n = atoull(num_str);
	dict = parse_dict(dict_path);
	if (!dict)
	{
		putstr("Dict Error\n");
		return (0);
	}
	if (n == 0)
		putstr("zero\n");
	else
	{
		convert_number(n, dict, &first);
		write(1, "\n", 1);
	}
	free_dict(dict);
	return (0);
}
