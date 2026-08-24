/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   validation_func.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/18 16:24:03 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/19 23:32:44 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

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

int	is_str_under_lim(char *str, int n)
{
	unsigned int	i;
	char			limit_char;

	i = 0;
	limit_char = n + '0';
	while (str[i] != '\0')
	{
		if ((str[i] < '1' || str[i] > limit_char) && str[i] != ' ')
			return (1);
		i++;
	}
	return (0);
}

int	input_validation(char *str, int n)
{
	if (n < 4 || n > 9)
		return (1);
	if (format_validation(str) == 1)
		return (1);
	else if (is_str_under_lim(str, n) == 1)
		return (1);
	return (0);
}
