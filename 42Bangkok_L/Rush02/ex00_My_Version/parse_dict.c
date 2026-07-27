/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse_dict.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/27 05:56:31 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/27 14:32:32 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rsh02.h"

void	sort_dict(t_dict *dict, int size)
{
	int		i;
	int		j;
	t_dict	tmp;

	i = 0;
	while (i < size - 1)
	{
		j = i + 1;
		while (j < size)
		{
			if (dict[i].nb < dict[j].nb)
			{
				tmp = dict[i];
				dict[i] = dict[j];
				dict[j] = tmp;
			}
			j++;
		}
		i++;
	}
}

t_dict	*parse_dict(char *path)
{
	int				fd;
	unsigned int	i;
	unsigned int	j;
	char			buf[4096];
	t_dict			*dict;
	int				start;

	i = 0;
	j = 0;
	fd = open(path, O_RDONLY);
	if (fd < 0)
		return (NULL);
	read(fd, buf, 4096);
	close(fd);
	dict = malloc(sizeof(t_dict) * 100);
	if (!dict)
		return (NULL);
	while (buf[i])
	{
		if (buf[i] >= '0' && buf[i] <= '9')
		{
			dict[j].nb = atoull(&buf[i]);
			while (buf[i] && buf[i] != ':')
				i++;
			i++;
			while (buf[i] && buf[i] == ' ')
				i++;
			start = i;
			while (buf[i] && buf[i] != '\n')
				i++;
			buf[i] = '\0';
			dict[j].val = ft_strdup(&buf[start]);
			j++;
		}
		i++;
	}
	dict[j].val = NULL;
	sort_dict(dict, j);
	return (dict);
}

void	free_dict(t_dict *dict)
{
	int	i;

	i = 0;
	while (dict[i].val)
	{
		free(dict[i].val);
		i++;
	}
	free(dict);
}
