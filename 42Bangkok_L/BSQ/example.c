/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   example.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 01:56:13 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/29 03:17:23 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>

int	min2(int a, int b)
{
	if (a < b)
		return (a);
	return (b);
}

int	min3(int a, int b, int c)
{
	return (min2(min2(a, b), c));
}

void	fill_bsq(char **grid, int max_i, int max_j, int size, char fill)
{
	int	i;
	int	j;

	i = max_i - size + 1;
	while (i <= max_i)
	{
		j = max_j - size + 1;
		while (j <= max_j)
		{
			grid[i][j] = fill;
			j++;
		}
		i++;
	}
}

int	**alloc_dp(int m, int n)
{
	int	**dp;
	int	i;

	dp = (int **)malloc(sizeof(int *) * m);
	if (!dp)
		return (NULL);
	i = 0;
	while (i < m)
	{
		dp[i] = (int *)malloc(sizeof(int) * n);
		if (!dp[i])
			return (NULL);
		i++;
	}
	return (dp);
}

void	free_dp(int **dp, int m)
{
	int	i;

	i = 0;
	while (i < m)
	{
		free(dp[i]);
		i++;
	}
	free(dp);
}

void	bsq(char **grid, int m, int n, char *cfg)
{
	int	**dp;
	int	max[3];
	int	i;
	int	j;

	dp = alloc_dp(m, n);
	if (!dp)
		return ;
	max[0] = 0;
	i = -1;
	while (++i < m)
	{
		j = -1;
		while (++j < n)
		{
			if (grid[i][j] == cfg[1])
				dp[i][j] = 0;
			else if (i == 0 || j == 0)
				dp[i][j] = 1;
			else
				dp[i][j] = min3(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
					+ 1;
			if (dp[i][j] > max[0])
			{
				max[0] = dp[i][j];
				max[1] = i;
				max[2] = j;
			}
		}
	}
	fill_bsq(grid, max[1], max[2], max[0], cfg[2]);
	free_dp(dp, m);
}

char	*read_line(int fd)
{
	char	*buf;
	char	c;
	int		len;
	int		cap;

	cap = 128;
	len = 0;
	buf = (char *)malloc(cap);
	if (!buf)
		return (NULL);
	while (read(fd, &c, 1) > 0 && c != '\n')
	{
		buf[len++] = c;
		if (len >= cap - 1)
		{
			cap *= 2;
			buf = (char *)realloc(buf, cap);
		}
	}
	if (len == 0 && c != '\n')
	{
		free(buf);
		return (NULL);
	}
	buf[len] = '\0';
	return (buf);
}

int	ft_atoi(char *str)
{
	int	res;

	res = 0;
	while (*str >= '0' && *str <= '9')
	{
		res = res * 10 + (*str - '0');
		str++;
	}
	return (res);
}

int	parse_header(int fd, int *m, char *cfg)
{
	char	*head;
	int		len;

	head = read_line(fd);
	if (!head)
		return (0);
	len = 0;
	while (head[len])
		len++;
	if (len < 4)
	{
		free(head);
		return (0);
	}
	cfg[2] = head[len - 1];
	cfg[1] = head[len - 2];
	cfg[0] = head[len - 3];
	head[len - 3] = '\0';
	*m = ft_atoi(head);
	free(head);
	if (*m <= 0)
		return (0);
	return (1);
}

void	print_and_free(char **grid, int m, int n)
{
	int	i;

	i = 0;
	while (i < m)
	{
		write(1, grid[i], n);
		write(1, "\n", 1);
		free(grid[i]);
		i++;
	}
	free(grid);
}

void	process_file(const char *filename)
{
	int		fd;
	int		m;
	int		n;
	char	cfg[3];
	char	**grid;
	int		i;

	fd = open(filename, O_RDONLY);
	if (fd < 0 || !parse_header(fd, &m, cfg))
	{
		write(2, "map error\n", 10);
		return ;
	}
	grid = (char **)malloc(sizeof(char *) * m);
	i = 0;
	n = 0;
	while (i < m)
	{
		grid[i] = read_line(fd);
		if (!grid[i])
		{
			write(2, "map error\n", 10);
			close(fd);
			return ;
		}
		if (i == 0)
		{
			while (grid[0][n])
				n++;
		}
		i++;
	}
	close(fd);
	bsq(grid, m, n, cfg);
	print_and_free(grid, m, n);
}

int	main(int argc, char **argv)
{
	int	i;

	if (argc < 2)
	{
		write(2, "map error\n", 10);
		return (0);
	}
	i = 1;
	while (i < argc)
	{
		process_file(argv[i]);
		if (i < argc - 1)
			write(1, "\n", 1);
		i++;
	}
	return (0);
}
