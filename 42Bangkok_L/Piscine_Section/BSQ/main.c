/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 17:17:03 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/29 17:35:49 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "bsq.h"

void	process_file(int fd)
{
	int		dim[2];
	char	cfg[3];
	char	**grid;

	if (fd < 0 || !parse_header(fd, &dim[0], cfg))
	{
		write(1, "map error\n", 10);
		if (fd > 0)
			close(fd);
		return ;
	}
	grid = (char **)malloc(sizeof(char *) * dim[0]);
	if (!read_grid(fd, grid, dim, cfg))
	{
		write(1, "map error\n", 10);
		if (fd > 0)
			close(fd);
		return ;
	}
	if (fd > 0)
		close(fd);
	bsq(grid, dim[0], dim[1], cfg);
	print_and_free(grid, dim[0], dim[1]);
}

int	main(int argc, char **argv)
{
	int	i;
	int	fd;

	if (argc == 1)
		process_file(0);
	else
	{
		i = 1;
		while (i < argc)
		{
			fd = open(argv[i], O_RDONLY);
			process_file(fd);
			if (i < argc - 1)
				write(1, "\n", 1);
			i++;
		}
	}
	return (0);
}
