/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_func.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aukyaw <aukyaw@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/18 16:16:50 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/19 12:27:59 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_putstr(char *str);
int		input_validation(char *str);
int		solve_puzzle(int grid[4][4], int clues[16], int row, int col);
void	print_grid(int grid[4][4]);

void	parse_clues(char *str, int clues[16])
{
	int	i;
	int	k;

	i = 0;
	k = 0;
	while (str[i] != '\0' && k < 16)
	{
		if (str[i] >= '1' && str[i] <= '4')
		{
			clues[k] = str[i] - '0';
			k++;
		}
		i++;
	}
}

void	init_grid(int grid[4][4])
{
	int	i;
	int	j;

	i = 0;
	while (i < 4)
	{
		j = 0;
		while (j < 4)
		{
			grid[i][j] = 0;
			j++;
		}
		i++;
	}
}

int	main(int argc, char **argv)
{
	int	clues[16];
	int	grid[4][4];

	if (argc != 2 || input_validation(argv[1]) == 1)
	{
		ft_putstr("Error\n");
		return (1);
	}
	parse_clues(argv[1], clues);
	init_grid(grid);
	if (solve_puzzle(grid, clues, 0, 0) == 1)
	{
		print_grid(grid);
	}
	else
	{
		ft_putstr("Error\n");
	}
	return (0);
}
