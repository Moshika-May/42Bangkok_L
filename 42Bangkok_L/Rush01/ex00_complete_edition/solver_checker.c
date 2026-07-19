/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   solver_checker.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/19 23:32:06 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/19 23:32:11 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	check_row_left(int **grid, int row, int expected, int n);
int	check_row_right(int **grid, int row, int expected, int n);
int	check_col_top(int **grid, int col, int expected, int n);
int	check_col_bottom(int **grid, int col, int expected, int n);

int	check_all_clues(int **grid, int *clues, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		if (!check_col_top(grid, i, clues[i], n) || !check_col_bottom(grid, i,
				clues[i + n], n))
			return (0);
		if (!check_row_left(grid, i, clues[i + (n * 2)], n)
			|| !check_row_right(grid, i, clues[i + (n * 3)], n))
			return (0);
		i++;
	}
	return (1);
}
