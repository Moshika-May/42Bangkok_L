/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ataweech <ataweech@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 19:52:13 by ataweech          #+#    #+#             */
/*   Updated: 2026/07/26 20:57:57 by ataweech         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rush02.h"

static char	*ft_strndup(char *src, int n)
{
	char	*dest;
	int		i;

	dest = malloc(sizeof(char) * (n + 1));
	if (!dest)
		return (NULL);
	i = 0;
	while (i < n && src[i])
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = '\0';
	return (dest);
}

static char	*read_file(char *path)
{
	int		fd;
	int		bytes;
	char	*buffer;

	fd = open(path, O_RDONLY);
	if (fd < 0)
		return (NULL);
	buffer = malloc(sizeof(char) * 30000);
	if (buffer)
	{
		bytes = read(fd, buffer, 29999);
		if (bytes > 0)
		{
			buffer[bytes] = '\0';
			close(fd);
			return (buffer);
		}
		free(buffer);
	}
	close(fd);
	return (NULL);
}

static char	*parse_val(char *buf, int *i)
{
	int	start;
	int	end;

	while (buf[*i] == ' ' || buf[*i] == '\t')
		(*i)++;
	start = *i;
	while (buf[*i] && buf[*i] != '\n')
		(*i)++;
	end = *i;
	while (end > start && (buf[end - 1] == ' ' || buf[end - 1] == '\t'))
		end--;
	if (start == end)
		return (NULL);
	return (ft_strndup(buf + start, end - start));
}

static int	parse_line(char *buf, int *i, t_list **head)
{
	int		k[2];
	char	*key;
	char	*val;

	while (buf[*i] == ' ' || buf[*i] == '\t' || buf[*i] == '\n')
		(*i)++;
	if (!buf[*i])
		return (1);
	k[0] = *i;
	while (buf[*i] >= '0' && buf[*i] <= '9')
		(*i)++;
	k[1] = *i;
	while (buf[*i] == ' ' || buf[*i] == '\t')
		(*i)++;
	if (k[0] == k[1] || buf[(*i)++] != ':')
		return (0);
	key = ft_strndup(buf + k[0], k[1] - k[0]);
	val = parse_val(buf, i);
	if (key && val)
		ft_lstadd_back(head, create_node(key, val));
	free(key);
	free(val);
	return (key && val != NULL);
}

t_list	*parse_dict(char *path)
{
	char	*buf;
	int		i;
	t_list	*head;

	buf = read_file(path);
	if (!buf)
		return (NULL);
	i = 0;
	head = NULL;
	while (buf[i])
	{
		if (!parse_line(buf, &i, &head))
		{
			free(buf);
			free_list(head);
			return (NULL);
		}
	}
	free(buf);
	return (head);
}
