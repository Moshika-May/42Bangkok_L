/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_convert_base2.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hzheng2 <hzheng2@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/25 11:02:58 by hzheng2           #+#    #+#             */
/*   Updated: 2026/07/25 11:03:39 by hzheng2          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	get_size(char *arr)
{
	int	len;

	len = 0;
	while (arr[len] != '\0')
		len++;
	return (len);
}

int	get_idx(char c, char *arr)
{
	int	idx;

	idx = 0;
	while (arr[idx] != '\0')
	{
		if (arr[idx] == c)
			return (idx);
		idx++;
	}
	return (-1);
}

int	isbasevalid(char *base)
{
	int	idx;
	int	idx2;
	int	len;

	len = get_size(base);
	if (len < 2)
		return (0);
	idx = 0;
	while (base[idx] != '\0')
	{
		if (base[idx] == '+' || base[idx] == '-' || base[idx] == ' '
			|| (base[idx] >= 9 && base[idx] <= 13))
			return (0);
		idx2 = idx + 1;
		while (base[idx2] != '\0')
		{
			if (base[idx] == base[idx2])
				return (0);
			idx2++;
		}
		idx++;
	}
	return (1);
}
