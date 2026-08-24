/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ataweech <ataweech@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 20:00:00 by ataweech          #+#    #+#             */
/*   Updated: 2026/07/26 20:44:16 by ataweech         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rush02.h"

static void	setup_args(int argc, char **argv, char **dict_path, char **num_str)
{
	*dict_path = "numbers.dict";
	if (argc == 2)
		*num_str = argv[1];
	else
	{
		*dict_path = argv[1];
		*num_str = argv[2];
	}
}

int	main(int argc, char **argv)
{
	t_list	*dict;
	char	*dict_path;
	char	*num_str;

	if (input_validation(argc, argv))
	{
		ft_putstr("Error\n");
		return (0);
	}
	setup_args(argc, argv, &dict_path, &num_str);
	dict = parse_dict(dict_path);
	if (!dict || !convert_number(num_str, dict))
	{
		ft_putstr("Dict Error\n");
		if (dict)
			free_list(dict);
		return (0);
	}
	free_list(dict);
	return (0);
}
