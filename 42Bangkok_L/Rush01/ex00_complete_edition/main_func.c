/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_func.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aukyaw <aukyaw@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/18 16:16:50 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/19 23:35:05 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

void	ft_putstr(char *str);
int		size_count(char *str);
int		input_validation(char *str, int n);
void	print_grid(int **grid, int n);
int		solve_puzzle(int **grid, int *clues, int *pos);
int		init_memory(int ***grid, int **clues, int n);
void	parse_clues(char *str, int *clues, int n);
void	init_grid(int **grid, int n);
void	free_memory(int **grid, int *clues, int n);

int	run_puzzle(int **grid, int *clues, int *pos)
{
	pos[0] = 0;
	pos[1] = 0;
	if (solve_puzzle(grid, clues, pos) == 1)
		print_grid(grid, pos[2]);
	else
		ft_putstr("Error\n");
	free_memory(grid, clues, pos[2]);
	return (0);
}

int	main(int argc, char **argv)
{
	int	*clues;
	int	**grid;
	int	pos[3];

	if (argc != 2)
	{
		ft_putstr("Error\n");
		return (1);
	}
	pos[2] = size_count(argv[1]);
	if (input_validation(argv[1], pos[2]) == 1 || init_memory(&grid, &clues,
			pos[2]) == 1)
	{
		ft_putstr("Error\n");
		return (1);
	}
	parse_clues(argv[1], clues, pos[2]);
	init_grid(grid, pos[2]);
	return (run_puzzle(grid, clues, pos));
}
