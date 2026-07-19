/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   solver_helper_func.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/19 12:32:42 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/19 23:31:39 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	check_row_left(int **grid, int row, int expected, int n)
{
	int	i;
	int	max;
	int	vis;

	i = 0;
	max = 0;
	vis = 0;
	while (i < n)
	{
		if (grid[row][i] > max)
		{
			max = grid[row][i];
			vis++;
		}
		i++;
	}
	return (vis == expected);
}

int	check_row_right(int **grid, int row, int expected, int n)
{
	int	i;
	int	max;
	int	vis;

	i = n - 1;
	max = 0;
	vis = 0;
	while (i >= 0)
	{
		if (grid[row][i] > max)
		{
			max = grid[row][i];
			vis++;
		}
		i--;
	}
	return (vis == expected);
}

int	check_col_top(int **grid, int col, int expected, int n)
{
	int	i;
	int	max;
	int	vis;

	i = 0;
	max = 0;
	vis = 0;
	while (i < n)
	{
		if (grid[i][col] > max)
		{
			max = grid[i][col];
			vis++;
		}
		i++;
	}
	return (vis == expected);
}

int	check_col_bottom(int **grid, int col, int expected, int n)
{
	int	i;
	int	max;
	int	vis;

	i = n - 1;
	max = 0;
	vis = 0;
	while (i >= 0)
	{
		if (grid[i][col] > max)
		{
			max = grid[i][col];
			vis++;
		}
		i--;
	}
	return (vis == expected);
}
