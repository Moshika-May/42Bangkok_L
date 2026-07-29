/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 17:18:03 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/29 17:37:02 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "bsq.h"

char	*finalize_line(char *buf, int len, char c)
{
	if (len == 0 && c != '\n')
	{
		free(buf);
		return (NULL);
	}
	buf[len] = '\0';
	return (buf);
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
	return (finalize_line(buf, len, c));
}

int	parse_header(int fd, int *m, char *cfg)
{
	char	*h;
	int		l;

	h = read_line(fd);
	if (!h)
		return (0);
	l = 0;
	while (h[l])
		l++;
	if (l < 4)
		return (free(h), 0);
	cfg[2] = h[l - 1];
	cfg[1] = h[l - 2];
	cfg[0] = h[l - 3];
	h[l - 3] = '\0';
	*m = ft_atoi(h);
	l = is_valid_cfg(cfg);
	free(h);
	return (*m > 0 && l);
}

int	read_grid(int fd, char **grid, int *dim, char *cfg)
{
	int	i;

	i = 0;
	dim[1] = 0;
	while (i < dim[0])
	{
		grid[i] = read_line(fd);
		if (!grid[i])
			return (0);
		if (i == 0)
		{
			while (grid[0][dim[1]])
				dim[1]++;
			if (dim[1] == 0)
				return (0);
		}
		if (!check_line(grid[i], dim[1], cfg))
			return (0);
		i++;
	}
	return (1);
}
