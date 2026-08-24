/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   solver.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aukyaw <aukyaw@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/19 12:02:38 by aukyaw            #+#    #+#             */
/*   Updated: 2026/07/19 12:35:00 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	check_row_left(int grid[4][4], int row, int expected);

int	check_row_right(int grid[4][4], int row, int expected);

int	check_col_top(int grid[4][4], int col, int expected);

int	check_col_bottom(int grid[4][4], int col, int expected);

int	check_all_clues(int grid[4][4], int clues[16]);

int	is_safe(int grid[4][4], int row, int col, int num)
{
	int	i;

	i = 0;
	while (i < 4)
	{
		if (grid[row][i] == num || grid[i][col] == num)
			return (0);
		i++;
	}
	return (1);
}

int	solve_puzzle(int grid[4][4], int clues[16], int row, int col)
{
	int	num;

	if (row == 4)
		return (check_all_clues(grid, clues));
	if (col == 4)
		return (solve_puzzle(grid, clues, row + 1, 0));
	num = 1;
	while (num <= 4)
	{
		if (is_safe(grid, row, col, num))
		{
			grid[row][col] = num;
			if (solve_puzzle(grid, clues, row, col + 1))
				return (1);
			grid[row][col] = 0;
		}
		num++;
	}
	return (0);
}
