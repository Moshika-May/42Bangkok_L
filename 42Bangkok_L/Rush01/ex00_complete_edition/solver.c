/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   solver.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aukyaw <aukyaw@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/19 12:02:38 by aukyaw            #+#    #+#             */
/*   Updated: 2026/07/19 23:35:18 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	check_all_clues(int **grid, int *clues, int n);
int	solve_puzzle(int **grid, int *clues, int *pos);

int	is_safe(int **grid, int *pos, int num)
{
	int	i;

	i = 0;
	while (i < pos[2])
	{
		if (grid[pos[0]][i] == num || grid[i][pos[1]] == num)
			return (0);
		i++;
	}
	return (1);
}

int	try_numbers(int **grid, int *clues, int *pos)
{
	int	num;
	int	nxt[3];

	num = 1;
	nxt[0] = pos[0];
	nxt[1] = pos[1] + 1;
	nxt[2] = pos[2];
	while (num <= pos[2])
	{
		if (is_safe(grid, pos, num))
		{
			grid[pos[0]][pos[1]] = num;
			if (solve_puzzle(grid, clues, nxt))
				return (1);
			grid[pos[0]][pos[1]] = 0;
		}
		num++;
	}
	return (0);
}

int	solve_puzzle(int **grid, int *clues, int *pos)
{
	int	nxt[3];

	if (pos[0] == pos[2])
		return (check_all_clues(grid, clues, pos[2]));
	if (pos[1] == pos[2])
	{
		nxt[0] = pos[0] + 1;
		nxt[1] = 0;
		nxt[2] = pos[2];
		return (solve_puzzle(grid, clues, nxt));
	}
	return (try_numbers(grid, clues, pos));
}
