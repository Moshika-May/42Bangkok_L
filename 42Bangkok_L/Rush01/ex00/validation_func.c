/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   validation_func.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/18 16:24:03 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/19 16:24:57 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

unsigned int	size_count(char *str);

int	format_validation(char *str)
{
	unsigned int	i;

	i = 0;
	if (str[i] == ' ')
		return (1);
	while (str[i] != '\0')
	{
		if (str[i] == ' ' && str[i + 1] == ' ')
			return (1);
		if (str[i] >= '0' && str[i] <= '9')
		{
			if (str[i + 1] >= '0' && str[i + 1] <= '9')
				return (1);
		}
		if (str[i] == ' ' && str[i + 1] == '\0')
			return (1);
		i++;
	}
	return (0);
}

int	is_str_numberic(char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i] != '\0')
	{
		if ((str[i] < '0' || str[i] > '9') && str[i] != ' ')
			return (1);
		i++;
	}
	return (0);
}

int	is_str_under_lim(char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i] != '\0')
	{
		if ((str[i] < '1' || str[i] > '4') && str[i] != ' ')
			return (1);
		i++;
	}
	return (0);
}

int	size_validation(char *str)
{
	unsigned int	i;
	unsigned int	j;
	unsigned char	k;

	i = 0;
	j = 0;
	k = size_count(str) + '0';
	while (str[i] != '\0')
	{
		if ((str[i] >= '1' || str[i] <= k) && str[i] != ' ')
			j++;
		i++;
	}
	if (size_count(str) < 4)
		return (1);
	if ((j % 4) != 0)
		return (1);
	return (0);
}

int	input_validation(char *str)
{
	if (format_validation(str) == 1)
		return (1);
	else if (is_str_numberic(str) == 1)
		return (1);
	else if (is_str_under_lim(str) == 1)
		return (1);
	else if (size_validation(str) == 1)
		return (1);
	else
		return (0);
}
