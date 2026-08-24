/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_convert_base2.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 13:26:19 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/28 22:49:03 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>
#include <stdlib.h>

int	base_check_n_len(char *base)
{
	unsigned int	i;
	unsigned int	j;

	i = 0;
	if (!base || !base[i] || !base[1])
		return (i);
	while (base[i])
	{
		if (base[i] == '+' || base[i] == '-' || base[i] == ' '
			|| (base[i] >= '\t' && base[i] <= '\r'))
			return (0);
		j = i + 1;
		while (base[j])
		{
			if (base[i] == base[j])
				return (0);
			j++;
		}
		i++;
	}
	return (i);
}

int	index_base(char c, char *base)
{
	unsigned int	i;

	i = 0;
	while (base[i])
	{
		if (base[i] == c)
			return (i);
		i++;
	}
	return (-1);
}

static int	get_num_len(long long nbr, int base_len)
{
	unsigned int	i;

	i = 0;
	if (nbr <= 0)
	{
		i++;
		nbr = -nbr;
	}
	while (nbr > 0)
	{
		nbr /= base_len;
		i++;
	}
	return (i);
}

char	*ft_itoa_base(long long nbr, char *base)
{
	long long		n;
	unsigned int	b_len;
	unsigned int	i;
	char			*arr;

	b_len = base_check_n_len(base);
	n = nbr;
	i = get_num_len(n, b_len);
	arr = (char *)malloc(sizeof(char) * (i + 1));
	if (!arr)
		return (NULL);
	arr[i] = '\0';
	if (n == 0)
		arr[0] = base[0];
	if (n < 0)
	{
		arr[0] = '-';
		n = -n;
	}
	while (n > 0)
	{
		arr[--i] = base[n % b_len];
		n /= b_len;
	}
	return (arr);
}
