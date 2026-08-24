/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_params.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/25 13:05:37 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/25 16:12:46 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	putstr(char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i])
	{
		write(1, &str[i], 1);
		i++;
	}
	return ;
}

int	ft_strcmp(char *s1, char *s2)
{
	unsigned int	i;
	int				var;

	i = 0;
	while (s1[i] != '\0' && s1[i] == s2[i])
	{
		i++;
	}
	var = ((unsigned char)s1[i]) - ((unsigned char)s2[i]);
	return (var);
}

int	main(int argc, char **argv)
{
	int		i;
	int		j;
	int		id;
	char	*t;

	i = 1;
	while (i < argc - 1)
	{
		id = i;
		j = i;
		while (++j < argc)
			if (ft_strcmp(argv[j], argv[id]) < 0)
				id = j;
		t = argv[i];
		argv[i] = argv[id];
		argv[id] = t;
		i++;
	}
	i = 0;
	while (++i < argc)
	{
		putstr(argv[i]);
		write(1, "\n", 1);
	}
	return (0);
}
